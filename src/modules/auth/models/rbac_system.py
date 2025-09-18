#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système RBAC (Role-Based Access Control) pour EduManager+
========================================================

Gère les rôles, permissions et contrôle d'accès des utilisateurs.
"""

from database.connection import get_db_connection
from src.utils.db_utils import fetch_one, execute_query
import os
from typing import Dict, List, Optional, Set
from datetime import datetime

class RBACSystem:
    """Système de contrôle d'accès basé sur les rôles"""
    
    def __init__(self, db_path: str = None, dev_mode: bool = False):
        self.db_path = db_path  # Non utilisé pour SQL Server
        self.dev_mode = dev_mode
        
        # Initialiser les tables RBAC
        self._init_rbac_tables()
        
        # Créer les rôles par défaut si nécessaire
        if dev_mode:
            self._create_default_roles()
    
    def _init_rbac_tables(self):
        """Initialise les tables RBAC"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            # Table des rôles
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='roles' AND xtype='U')
                CREATE TABLE roles (
                    id_role INT IDENTITY(1,1) PRIMARY KEY,
                    nom_role NVARCHAR(100) UNIQUE NOT NULL,
                    description NVARCHAR(500),
                    niveau_acces INT DEFAULT 1,
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Table des permissions
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='permissions' AND xtype='U')
                CREATE TABLE permissions (
                    id_permission INT IDENTITY(1,1) PRIMARY KEY,
                    nom_permission NVARCHAR(100) UNIQUE NOT NULL,
                    description NVARCHAR(500),
                    resource NVARCHAR(100),
                    action NVARCHAR(100),
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Table des permissions par rôle
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='role_permissions' AND xtype='U')
                CREATE TABLE role_permissions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    role_id INT NOT NULL,
                    permission_id INT NOT NULL,
                    granted INT DEFAULT 1,
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    FOREIGN KEY (permission_id) REFERENCES permissions (id_permission),
                    UNIQUE(role_id, permission_id)
                )
            ''')
            
            # Table des utilisateurs et leurs rôles
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='user_roles' AND xtype='U')
                CREATE TABLE user_roles (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    role_id INT NOT NULL,
                    assigned_at DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    UNIQUE(user_id, role_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tables RBAC initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation RBAC: {e}")
    
    def _create_default_roles(self):
        """Crée les rôles par défaut"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            # Rôles par défaut
            default_roles = [
                ("administrateur", "Administrateur système", 10),
                ("directeur", "Directeur d'établissement", 8),
                ("secretaire", "Secrétaire", 6),
                ("professeurs", "Professeur", 4),
                ("eleves", "Élève", 2),
                ("parent", "Parent d'élève", 1)
            ]
            
            for nom_role, description, niveau in default_roles:
                cursor.execute('''
                    INSERT OR IGNORE INTO roles (nom_role, description, niveau_acces)
                    VALUES (?, ?, ?)
                ''', (nom_role, description, niveau))
            
            conn.commit()
            conn.close()
            print("✅ Rôles par défaut créés")
            
        except Exception as e:
            print(f"❌ Erreur création rôles: {e}")
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Récupère le rôle principal d'un utilisateurs"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom_role 
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id_role
                WHERE ur.user_id = ?
                ORDER BY r.niveau_acces DESC
                OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else "utilisateurs"
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle: {e}")
            return "utilisateurs"
    
    def get_user_roles(self, user_id: int) -> List[str]:
        """Récupère tous les rôles d'un utilisateurs"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom_role 
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id_role
                WHERE ur.user_id = ?
                ORDER BY r.niveau_acces DESC
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [row[0] for row in results]
            
        except Exception as e:
            print(f"❌ Erreur récupération rôles: {e}")
            return ["utilisateurs"]
    
    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateurs"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            # Récupérer l'ID du rôle
            cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (role_name,))
            role_result = cursor.fetchone()
            
            if not role_result:
                print(f"❌ Rôle '{role_name}' non trouvé")
                conn.close()
                return False
            
            role_id = role_result[0]
            
            # Assigner le rôle
            cursor.execute('''
                INSERT OR IGNORE INTO user_roles (user_id, role_id)
                VALUES (?, ?)
            ''', (user_id, role_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Rôle '{role_name}' assigné à l'utilisateurs {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur assignation rôle: {e}")
            return False
    
    def has_permission(self, user_id: int, permission_name: str) -> bool:
        """Vérifie si un utilisateurs a une permissions spécifique"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM user_roles ur
                JOIN role_permissions rp ON ur.role_id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id_permission
                WHERE ur.user_id = ? AND p.nom_permission = ? AND rp.granted = 1
            ''', (user_id, permission_name))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] > 0 if result else False
            
        except Exception as e:
            print(f"❌ Erreur vérification permissions: {e}")
            return False
    
    def get_user_permissions(self, user_id: int) -> Set[str]:
        """Récupère toutes les permissions d'un utilisateurs"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT p.nom_permission
                FROM user_roles ur
                JOIN role_permissions rp ON ur.role_id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id_permission
                WHERE ur.user_id = ? AND rp.granted = 1
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return {row[0] for row in results}
            
        except Exception as e:
            print(f"❌ Erreur récupération permissions: {e}")
            return set()
    
    def create_permission(self, TABLE_NAME: str, description: str = "", resource: str = "", action: str = "") -> bool:
        """Crée une nouvelle permissions"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO permissions (nom_permission, description, resource, action)
                VALUES (?, ?, ?, ?)
            ''', (TABLE_NAME, description, resource, action))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{TABLE_NAME}' créée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création permissions: {e}")
            return False
    
    def grant_permission_to_role(self, role_name: str, permission_name: str) -> bool:
        """Accorde une permissions à un rôle"""
        try:
            conn = get_db_connection()
            if not conn:
                print("❌ Impossible de se connecter à la base de données")
                return
            
            cursor = conn.cursor()
            
            # Récupérer les IDs
            cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (role_name,))
            role_result = cursor.fetchone()
            
            cursor.execute('SELECT id_permission FROM permissions WHERE nom_permission = ?', (permission_name,))
            perm_result = cursor.fetchone()
            
            if not role_result or not perm_result:
                print(f"❌ Rôle ou permissions non trouvé")
                conn.close()
                return False
            
            role_id, perm_id = role_result[0], perm_result[0]
            
            # Accorder la permissions
            cursor.execute('''
                INSERT OR REPLACE INTO role_permissions (role_id, permission_id, granted)
                VALUES (?, ?, 1)
            ''', (role_id, perm_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{permission_name}' accordée au rôle '{role_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Erreur accord permissions: {e}")
            return False

