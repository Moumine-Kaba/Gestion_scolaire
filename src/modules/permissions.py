#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de gestion des permissions pour EduManager+
=================================================

Gère les permissions et leur attribution aux rôles.
"""

# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
from typing import Dict, List, Optional, Set
from datetime import datetime

class Permission:
    """Représente une permissions dans le système"""
    
    def __init__(self, id_permission: int, nom_permission: str, description: str = "", 
                 resource: str = "", action: str = ""):
        self.id_permission = id_permission
        self.nom_permission = nom_permission
        self.description = description
        self.resource = resource
        self.action = action
    
    def __str__(self):
        return f"{self.nom_permission} ({self.resource}:{self.action})"

class PermissionManager:
    """Gestionnaire des permissions"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les tables
        self._init_permission_tables()
        
        # Créer les permissions par défaut
        self._create_default_permissions()
    
    def _init_permission_tables(self):
        """Initialise les tables des permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
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
            
            conn.commit()
            conn.close()
            print("✅ Tables des permissions initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation tables permissions: {e}")
    
    def _create_default_permissions(self):
        """Crée les permissions par défaut"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Permissions par défaut
            default_permissions = [
                # Permissions générales
                ("system.admin", "Administration système", "system", "admin"),
                ("system.read", "Lecture système", "system", "read"),
                ("system.write", "Écriture système", "system", "write"),
                ("system.delete", "Suppression système", "system", "delete"),
                
                # Permissions utilisateurs
                ("users.read", "Lecture utilisateurs", "users", "read"),
                ("users.write", "Écriture utilisateurs", "users", "write"),
                ("users.delete", "Suppression utilisateurs", "users", "delete"),
                ("users.create", "Création utilisateurs", "users", "create"),
                
                # Permissions élèves
                ("eleves.read", "Lecture élèves", "eleves", "read"),
                ("eleves.write", "Écriture élèves", "eleves", "write"),
                ("eleves.delete", "Suppression élèves", "eleves", "delete"),
                ("eleves.create", "Création élèves", "eleves", "create"),
                
                # Permissions professeurs
                ("professeurs.read", "Lecture professeurs", "professeurs", "read"),
                ("professeurs.write", "Écriture professeurs", "professeurs", "write"),
                ("professeurs.delete", "Suppression professeurs", "professeurs", "delete"),
                ("professeurs.create", "Création professeurs", "professeurs", "create"),
                
                # Permissions classes
                ("classes.read", "Lecture classes", "classes", "read"),
                ("classes.write", "Écriture classes", "classes", "write"),
                ("classes.delete", "Suppression classes", "classes", "delete"),
                ("classes.create", "Création classes", "classes", "create"),
                
                # Permissions notes
                ("notes.read", "Lecture notes", "notes", "read"),
                ("notes.write", "Écriture notes", "notes", "write"),
                ("notes.delete", "Suppression notes", "notes", "delete"),
                ("notes.create", "Création notes", "notes", "create"),
                
                # Permissions présences
                ("presences.read", "Lecture présences", "presences", "read"),
                ("presences.write", "Écriture présences", "presences", "write"),
                ("presences.delete", "Suppression présences", "presences", "delete"),
                ("presences.create", "Création présences", "presences", "create"),
                
                # Permissions bulletins
                ("bulletins.read", "Lecture bulletins", "bulletins", "read"),
                ("bulletins.write", "Écriture bulletins", "bulletins", "write"),
                ("bulletins.delete", "Suppression bulletins", "bulletins", "delete"),
                ("bulletins.create", "Création bulletins", "bulletins", "create"),
                
                # Permissions paiements
                ("paiements.read", "Lecture paiements", "paiements", "read"),
                ("paiements.write", "Écriture paiements", "paiements", "write"),
                ("paiements.delete", "Suppression paiements", "paiements", "delete"),
                ("paiements.create", "Création paiements", "paiements", "create"),
            ]
            
            for nom_perm, description, resource, action in default_permissions:
                cursor.execute('''
                    INSERT OR IGNORE INTO permissions (nom_permission, description, resource, action)
                    VALUES (?, ?, ?, ?)
                ''', (nom_perm, description, resource, action))
            
            conn.commit()
            conn.close()
            print("✅ Permissions par défaut créées")
            
        except Exception as e:
            print(f"❌ Erreur création permissions par défaut: {e}")
    
    def get_permission_by_name(self, nom_permission: str) -> Optional[Permission]:
        """Récupère une permissions par son nom"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_permission, nom_permission, description, resource, action
                FROM permissions
                WHERE nom_permission = ?
            ''', (nom_permission,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return Permission(result[0], result[1], result[2], result[3], result[4])
            
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération permissions: {e}")
            return None
    
    def get_all_permissions(self) -> List[Permission]:
        """Récupère toutes les permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_permission, nom_permission, description, resource, action
                FROM permissions
                ORDER BY resource, action
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            permissions = []
            for row in results:
                permissions.append(Permission(row[0], row[1], row[2], row[3], row[4]))
            
            return permissions
            
        except Exception as e:
            print(f"❌ Erreur récupération toutes permissions: {e}")
            return []
    
    def get_permissions_by_resource(self, resource: str) -> List[Permission]:
        """Récupère les permissions pour une ressource donnée"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_permission, nom_permission, description, resource, action
                FROM permissions
                WHERE resource = ?
                ORDER BY action
            ''', (resource,))
            
            results = cursor.fetchall()
            conn.close()
            
            permissions = []
            for row in results:
                permissions.append(Permission(row[0], row[1], row[2], row[3], row[4]))
            
            return permissions
            
        except Exception as e:
            print(f"❌ Erreur récupération permissions ressource: {e}")
            return []
    
    def create_permission(self, nom_permission: str, description: str = "", 
                         resource: str = "", action: str = "") -> bool:
        """Crée une nouvelle permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO permissions (nom_permission, description, resource, action)
                VALUES (?, ?, ?, ?)
            ''', (nom_permission, description, resource, action))
            
            conn.commit()
            conn.close()
            print(f"✅ Permission '{nom_permission}' créée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création permissions: {e}")
            return False
    
    def delete_permission(self, nom_permission: str) -> bool:
        """Supprime une permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Vérifier si la permissions est utilisée
            cursor.execute('''
                SELECT COUNT(*) FROM role_permissions 
                WHERE permission_id = (SELECT id_permission FROM permissions WHERE nom_permission = ?)
            ''', (nom_permission,))
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"❌ Impossible de supprimer la permissions '{nom_permission}' car elle est utilisée par {count} rôle(s)")
                conn.close()
                return False
            
            cursor.execute('DELETE FROM permissions WHERE nom_permission = ?', (nom_permission,))
            conn.commit()
            conn.close()
            print(f"✅ Permission '{nom_permission}' supprimée")
            return True
            
        except Exception as e:
            print(f"❌ Erreur suppression permissions: {e}")
            return False
    
    def update_permission(self, nom_permission: str, description: str = None, 
                         resource: str = None, action: str = None) -> bool:
        """Met à jour une permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Construire la requête de mise à jour dynamiquement
            updates = []
            params = []
            
            if description is not None:
                updates.append("description = ?")
                params.append(description)
            
            if resource is not None:
                updates.append("resource = ?")
                params.append(resource)
            
            if action is not None:
                updates.append("action = ?")
                params.append(action)
            
            if not updates:
                print("❌ Aucune mise à jour spécifiée")
                conn.close()
                return False
            
            params.append(nom_permission)
            query = f"UPDATE permissions SET {', '.join(updates)} WHERE nom_permission = ?"
            
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            print(f"✅ Permission '{nom_permission}' mise à jour")
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour permissions: {e}")
            return False

