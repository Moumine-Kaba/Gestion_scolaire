#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des rôles pour EduManager+
============================================

Gère les rôles et leurs permissions dans le système RBAC.
"""

import sqlite3
import os
from typing import Dict, List, Optional, Set
from enum import Enum
from datetime import datetime

class PermissionLevel(Enum):
    """Niveaux de permission"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class Role:
    """Représente un rôle dans le système"""
    
    def __init__(self, id_role: int, nom_role: str, description: str = "", niveau_acces: int = 1):
        self.id_role = id_role
        self.nom_role = nom_role
        self.description = description
        self.niveau_acces = niveau_acces
        self.permissions = set()
    
    def add_permission(self, permission: str):
        """Ajoute une permission au rôle"""
        self.permissions.add(permission)
    
    def remove_permission(self, permission: str):
        """Retire une permission du rôle"""
        self.permissions.discard(permission)
    
    def has_permission(self, permission: str) -> bool:
        """Vérifie si le rôle a une permission"""
        return permission in self.permissions
    
    def is_admin(self) -> bool:
        """Vérifie si le rôle est administrateur"""
        return self.has_permission(PermissionLevel.ADMIN.value)

class RoleManager:
    """Gestionnaire des rôles"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les tables
        self._init_role_tables()
        
        # Créer les rôles par défaut
        self._create_default_roles()
    
    def _init_role_tables(self):
        """Initialise les tables des rôles"""
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
            
            conn.commit()
            conn.close()
            print("✅ Tables des rôles initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation tables rôles: {e}")
    
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
            print(f"❌ Erreur création rôles par défaut: {e}")
    
    def get_role_by_name(self, nom_role: str) -> Optional[Role]:
        """Récupère un rôle par son nom"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_role, nom_role, description, niveau_acces
                FROM roles
                WHERE nom_role = ?
            ''', (nom_role,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                role = Role(result[0], result[1], result[2], result[3])
                # Charger les permissions du rôle
                role.permissions = self.get_role_permissions(result[0])
                return role
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle: {e}")
            return None
    
    def get_role_permissions(self, role_id: int) -> Set[str]:
        """Récupère les permissions d'un rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT p.nom_permission
                FROM role_permissions rp
                JOIN permissions p ON rp.permission_id = p.id_permission
                WHERE rp.role_id = ? AND rp.granted = 1
            ''', (role_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return {row[0] for row in results}
            
        except Exception as e:
            print(f"❌ Erreur récupération permissions rôle: {e}")
            return set()
    
    def get_all_roles(self) -> List[Role]:
        """Récupère tous les rôles"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_role, nom_role, description, niveau_acces
                FROM roles
                ORDER BY niveau_acces DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            roles = []
            for row in results:
                role = Role(row[0], row[1], row[2], row[3])
                role.permissions = self.get_role_permissions(row[0])
                roles.append(role)
            
            return roles
            
        except Exception as e:
            print(f"❌ Erreur récupération tous rôles: {e}")
            return []
    
    def create_role(self, nom_role: str, description: str = "", niveau_acces: int = 1) -> bool:
        """Crée un nouveau rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO roles (nom_role, description, niveau_acces)
                VALUES (?, ?, ?)
            ''', (nom_role, description, niveau_acces))
            
            conn.commit()
            conn.close()
            print(f"✅ Rôle '{nom_role}' créé")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création rôle: {e}")
            return False
    
    def delete_role(self, nom_role: str) -> bool:
        """Supprime un rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si le rôle est utilisé
            cursor.execute('SELECT COUNT(*) FROM user_roles WHERE role_id = (SELECT id_role FROM roles WHERE nom_role = ?)', (nom_role,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"❌ Impossible de supprimer le rôle '{nom_role}' car il est utilisé par {count} utilisateur(s)")
                conn.close()
                return False
            
            cursor.execute('DELETE FROM roles WHERE nom_role = ?', (nom_role,))
            conn.commit()
            conn.close()
            print(f"✅ Rôle '{nom_role}' supprimé")
            return True
            
        except Exception as e:
            print(f"❌ Erreur suppression rôle: {e}")
            return False
    
    def assign_permission_to_role(self, nom_role: str, nom_permission: str) -> bool:
        """Assigne une permission à un rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les IDs
            cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (nom_role,))
            role_result = cursor.fetchone()
            
            cursor.execute('SELECT id_permission FROM permissions WHERE nom_permission = ?', (nom_permission,))
            perm_result = cursor.fetchone()
            
            if not role_result or not perm_result:
                print(f"❌ Rôle ou permission non trouvé")
                conn.close()
                return False
            
            role_id, perm_id = role_result[0], perm_result[0]
            
            # Assigner la permission
            cursor.execute('''
                INSERT OR REPLACE INTO role_permissions (role_id, permission_id, granted)
                VALUES (?, ?, 1)
            ''', (role_id, perm_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{nom_permission}' assignée au rôle '{nom_role}'")
            return True
            
        except Exception as e:
            print(f"❌ Erreur assignation permission: {e}")
            return False
    
    def revoke_permission_from_role(self, nom_role: str, nom_permission: str) -> bool:
        """Retire une permission d'un rôle"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer les IDs
            cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (nom_role,))
            role_result = cursor.fetchone()
            
            cursor.execute('SELECT id_permission FROM permissions WHERE nom_permission = ?', (nom_permission,))
            perm_result = cursor.fetchone()
            
            if not role_result or not perm_result:
                print(f"❌ Rôle ou permission non trouvé")
                conn.close()
                return False
            
            role_id, perm_id = role_result[0], perm_result[0]
            
            # Retirer la permission
            cursor.execute('''
                UPDATE role_permissions 
                SET granted = 0
                WHERE role_id = ? AND permission_id = ?
            ''', (role_id, perm_id))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{nom_permission}' retirée du rôle '{nom_role}'")
            return True
            
        except Exception as e:
            print(f"❌ Erreur retrait permission: {e}")
            return False

