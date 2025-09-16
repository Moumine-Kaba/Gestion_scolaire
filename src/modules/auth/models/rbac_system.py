#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système RBAC (Role-Based Access Control) pour EduManager+
========================================================

Gère les rôles, permissions et contrôle d'accès des utilisateurs.
"""

import sqlite3
import os
from typing import Dict, List, Optional, Set
from datetime import datetime

class RBACSystem:
    """Système de contrôle d'accès basé sur les rôles"""
    
    def __init__(self, db_path: str, dev_mode: bool = False):
        self.db_path = db_path
        self.dev_mode = dev_mode
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les tables RBAC
        self._init_rbac_tables()
        
        # Créer les rôles par défaut si nécessaire
        if dev_mode:
            self._create_default_roles()
    
    def _init_rbac_tables(self):
        """Initialise les tables RBAC"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table des rôles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS roles (
                    id_role INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_role TEXT UNIQUE NOT NULL,
                    description TEXT,
                    niveau_acces INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des permissions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS permissions (
                    id_permission INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_permission TEXT UNIQUE NOT NULL,
                    description TEXT,
                    resource TEXT,
                    action TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des permissions par rôle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS role_permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_id INTEGER NOT NULL,
                    permission_id INTEGER NOT NULL,
                    granted BOOLEAN DEFAULT 1,
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    FOREIGN KEY (permission_id) REFERENCES permissions (id_permission),
                    UNIQUE(role_id, permission_id)
                )
            ''')
            
            # Table des utilisateurs et leurs rôles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_roles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Rôles par défaut
            default_roles = [
                ("administrateur", "Administrateur système", 10),
                ("directeur", "Directeur d'établissement", 8),
                ("secretaire", "Secrétaire", 6),
                ("professeur", "Professeur", 4),
                ("eleve", "Élève", 2),
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
        """Récupère le rôle principal d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom_role 
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id_role
                WHERE ur.user_id = ?
                ORDER BY r.niveau_acces DESC
                LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else "utilisateur"
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle: {e}")
            return "utilisateur"
    
    def get_user_roles(self, user_id: int) -> List[str]:
        """Récupère tous les rôles d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
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
            return ["utilisateur"]
    
    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
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
            print(f"✅ Rôle '{role_name}' assigné à l'utilisateur {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur assignation rôle: {e}")
            return False
    
    def has_permission(self, user_id: int, permission_name: str) -> bool:
        """Vérifie si un utilisateur a une permission spécifique"""
        try:
            conn = sqlite3.connect(self.db_path)
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
            print(f"❌ Erreur vérification permission: {e}")
            return False
    
    def get_user_permissions(self, user_id: int) -> Set[str]:
        """Récupère toutes les permissions d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
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
    
    def create_permission(self, name: str, description: str = "", resource: str = "", action: str = "") -> bool:
        """Crée une nouvelle permission"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO permissions (nom_permission, description, resource, action)
                VALUES (?, ?, ?, ?)
            ''', (name, description, resource, action))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{name}' créée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création permission: {e}")
            return False
    
    def grant_permission_to_role(self, role_name: str, permission_name: str) -> bool:
        """Accorde une permission à un rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les IDs
            cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (role_name,))
            role_result = cursor.fetchone()
            
            cursor.execute('SELECT id_permission FROM permissions WHERE nom_permission = ?', (permission_name,))
            perm_result = cursor.fetchone()
            
            if not role_result or not perm_result:
                print(f"❌ Rôle ou permission non trouvé")
                conn.close()
                return False
            
            role_id, perm_id = role_result[0], perm_result[0]
            
            # Accorder la permission
            cursor.execute('''
                INSERT OR REPLACE INTO role_permissions (role_id, permission_id, granted)
                VALUES (?, ?, 1)
            ''', (role_id, perm_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{permission_name}' accordée au rôle '{role_name}'")
            return True
            
        except Exception as e:
            print(f"❌ Erreur accord permission: {e}")
            return False

