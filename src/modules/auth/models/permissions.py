#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Système de Gestion des Permissions et Vues
EduManager+ - Gestion Scolaire
"""

import sqlite3
import os
from typing import List, Dict, Optional, Set
from enum import Enum

class ViewType(Enum):
    """Types de vues disponibles dans l'application"""
    DASHBOARD = "dashboard"
    NOTES = "notes"
    PRESENCES = "presences"
    BULLETINS = "bulletins"
    ELEVES = "eleves"
    PROFESSEURS = "professeurs"
    CLASSES = "classes"
    MATIERES = "matieres"
    UTILISATEURS = "utilisateurs"
    ROLES = "roles"
    PARAMETRES = "parametres"
    RAPPORTS = "rapports"
    FINANCE = "finance"
    BIBLIOTHEQUE = "bibliotheque"
    CALENDRIER = "calendrier"
    SALES = "salles"
    ENSEIGNEMENTS = "enseignements"
    EMPLOIS = "emplois"
    PAIEMENTS = "paiements"

class PermissionLevel(Enum):
    """Niveaux de permission pour les vues"""
    NONE = "none"           # Pas d'accès
    READ = "read"           # Lecture seule
    WRITE = "write"         # Lecture + Écriture
    DELETE = "delete"       # Lecture + Écriture + Suppression
    ADMIN = "admin"         # Tous les droits

class ModulePermission(Enum):
    """Permissions spécifiques par module"""
    # Permissions générales
    VIEW_DASHBOARD = "view_dashboard"
    VIEW_STATS = "view_stats"
    VIEW_REPORTS = "view_reports"
    
    # Permissions élèves
    VIEW_ELEVES = "view_eleves"
    CREATE_ELEVES = "create_eleves"
    EDIT_ELEVES = "edit_eleves"
    DELETE_ELEVES = "delete_eleves"
    EXPORT_ELEVES = "export_eleves"
    
    # Permissions professeurs
    VIEW_PROFESSEURS = "view_professeurs"
    CREATE_PROFESSEURS = "create_professeurs"
    EDIT_PROFESSEURS = "edit_professeurs"
    DELETE_PROFESSEURS = "delete_professeurs"
    
    # Permissions classes
    VIEW_CLASSES = "view_classes"
    CREATE_CLASSES = "create_classes"
    EDIT_CLASSES = "edit_classes"
    DELETE_CLASSES = "delete_classes"
    
    # Permissions matières
    VIEW_MATIERES = "view_matieres"
    CREATE_MATIERES = "create_matieres"
    EDIT_MATIERES = "edit_matieres"
    DELETE_MATIERES = "delete_matieres"
    
    # Permissions notes
    VIEW_NOTES = "view_notes"
    CREATE_NOTES = "create_notes"
    EDIT_NOTES = "edit_notes"
    DELETE_NOTES = "delete_notes"
    VALIDATE_NOTES = "validate_notes"
    
    # Permissions présences
    VIEW_PRESENCES = "view_presences"
    CREATE_PRESENCES = "create_presences"
    EDIT_PRESENCES = "edit_presences"
    DELETE_PRESENCES = "delete_presences"
    
    # Permissions bulletins
    VIEW_BULLETINS = "view_bulletins"
    CREATE_BULLETINS = "create_bulletins"
    EDIT_BULLETINS = "edit_bulletins"
    DELETE_BULLETINS = "delete_bulletins"
    PRINT_BULLETINS = "print_bulletins"
    
    # Permissions utilisateurs
    VIEW_UTILISATEURS = "view_utilisateurs"
    CREATE_UTILISATEURS = "create_utilisateurs"
    EDIT_UTILISATEURS = "edit_utilisateurs"
    DELETE_UTILISATEURS = "delete_utilisateurs"
    MANAGE_ROLES = "manage_roles"
    
    # Permissions finances
    VIEW_FINANCE = "view_finance"
    CREATE_PAIEMENTS = "create_paiements"
    EDIT_PAIEMENTS = "edit_paiements"
    DELETE_PAIEMENTS = "delete_paiements"
    VIEW_RAPPORTS_FINANCE = "view_rapports_finance"
    
    # Permissions administration
    VIEW_PARAMETRES = "view_parametres"
    EDIT_PARAMETRES = "edit_parametres"
    VIEW_LOGS = "view_logs"
    SYSTEM_MAINTENANCE = "system_maintenance"

class ViewPermission:
    """Classe représentant une permission de vue"""
    def __init__(self, view_name: str, permission_level: PermissionLevel):
        self.view_name = view_name
        self.permission_level = permission_level

class PermissionManager:
    """Gestionnaire des permissions et accès aux vues"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        try:
            self._init_permissions_table()
            self._create_default_view_permissions()
            print("✅ Gestionnaire de permissions initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation permissions: {e}")

    def _init_permissions_table(self):
        """Initialise la table des permissions de vues"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table des permissions de vues par rôle
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS role_view_permissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role_id INTEGER NOT NULL,
                        view_name TEXT NOT NULL,
                        permission_level TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (role_id) REFERENCES roles (id_role) ON DELETE CASCADE,
                        UNIQUE(role_id, view_name)
                    )
                ''')
                
                # Table des permissions détaillées par module
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS role_module_permissions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role_id INTEGER NOT NULL,
                        module TEXT NOT NULL,
                        permission TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (role_id) REFERENCES roles (id_role) ON DELETE CASCADE,
                        UNIQUE(role_id, module, permission)
                    )
                ''')
                
                conn.commit()
                print("✅ Tables des permissions créées")
        except Exception as e:
            print(f"❌ Erreur création tables permissions: {e}")

    def _create_default_view_permissions(self):
        """Crée les permissions par défaut pour chaque rôle"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Récupérer tous les rôles
                cursor.execute("SELECT id_role, nom FROM roles")
                roles = cursor.fetchall()
                
                # Récupérer toutes les vues
                views = [view.value for view in ViewType]
                
                # Permissions par défaut pour chaque rôle
                default_permissions = {
                    "Super Administrateur": {view: PermissionLevel.ADMIN.value for view in views},
                    "Administrateur": {view: PermissionLevel.ADMIN.value for view in views},
                    "Directeur": {
                        ViewType.DASHBOARD.value: PermissionLevel.ADMIN.value,
                        ViewType.NOTES.value: PermissionLevel.READ.value,
                        ViewType.PRESENCES.value: PermissionLevel.READ.value,
                        ViewType.BULLETINS.value: PermissionLevel.READ.value,
                        ViewType.ELEVES.value: PermissionLevel.WRITE.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.WRITE.value,
                        ViewType.CLASSES.value: PermissionLevel.WRITE.value,
                        ViewType.MATIERES.value: PermissionLevel.WRITE.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.READ.value,
                        ViewType.ROLES.value: PermissionLevel.READ.value,
                        ViewType.PARAMETRES.value: PermissionLevel.WRITE.value,
                        ViewType.RAPPORTS.value: PermissionLevel.ADMIN.value,
                        ViewType.FINANCE.value: PermissionLevel.ADMIN.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.WRITE.value,
                        ViewType.SALES.value: PermissionLevel.WRITE.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.WRITE.value,
                        ViewType.EMPLOIS.value: PermissionLevel.WRITE.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.ADMIN.value
                    },
                    "Professeur": {
                        ViewType.DASHBOARD.value: PermissionLevel.READ.value,
                        ViewType.NOTES.value: PermissionLevel.WRITE.value,
                        ViewType.PRESENCES.value: PermissionLevel.WRITE.value,
                        ViewType.BULLETINS.value: PermissionLevel.WRITE.value,
                        ViewType.ELEVES.value: PermissionLevel.READ.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.READ.value,
                        ViewType.CLASSES.value: PermissionLevel.READ.value,
                        ViewType.MATIERES.value: PermissionLevel.READ.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.NONE.value,
                        ViewType.ROLES.value: PermissionLevel.NONE.value,
                        ViewType.PARAMETRES.value: PermissionLevel.NONE.value,
                        ViewType.RAPPORTS.value: PermissionLevel.READ.value,
                        ViewType.FINANCE.value: PermissionLevel.NONE.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.READ.value,
                        ViewType.SALES.value: PermissionLevel.READ.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.READ.value,
                        ViewType.EMPLOIS.value: PermissionLevel.READ.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.NONE.value
                    },
                    "Élève": {
                        ViewType.DASHBOARD.value: PermissionLevel.READ.value,
                        ViewType.NOTES.value: PermissionLevel.READ.value,
                        ViewType.PRESENCES.value: PermissionLevel.READ.value,
                        ViewType.BULLETINS.value: PermissionLevel.READ.value,
                        ViewType.ELEVES.value: PermissionLevel.NONE.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.READ.value,
                        ViewType.CLASSES.value: PermissionLevel.READ.value,
                        ViewType.MATIERES.value: PermissionLevel.READ.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.NONE.value,
                        ViewType.ROLES.value: PermissionLevel.NONE.value,
                        ViewType.PARAMETRES.value: PermissionLevel.NONE.value,
                        ViewType.RAPPORTS.value: PermissionLevel.NONE.value,
                        ViewType.FINANCE.value: PermissionLevel.NONE.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.READ.value,
                        ViewType.SALES.value: PermissionLevel.READ.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.READ.value,
                        ViewType.EMPLOIS.value: PermissionLevel.READ.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.NONE.value
                    },
                    "Parent": {
                        ViewType.DASHBOARD.value: PermissionLevel.READ.value,
                        ViewType.NOTES.value: PermissionLevel.READ.value,
                        ViewType.PRESENCES.value: PermissionLevel.READ.value,
                        ViewType.BULLETINS.value: PermissionLevel.READ.value,
                        ViewType.ELEVES.value: PermissionLevel.NONE.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.READ.value,
                        ViewType.CLASSES.value: PermissionLevel.READ.value,
                        ViewType.MATIERES.value: PermissionLevel.READ.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.NONE.value,
                        ViewType.ROLES.value: PermissionLevel.NONE.value,
                        ViewType.PARAMETRES.value: PermissionLevel.NONE.value,
                        ViewType.RAPPORTS.value: PermissionLevel.NONE.value,
                        ViewType.FINANCE.value: PermissionLevel.NONE.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.READ.value,
                        ViewType.SALES.value: PermissionLevel.READ.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.READ.value,
                        ViewType.EMPLOIS.value: PermissionLevel.READ.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.NONE.value
                    },
                    "Secrétaire": {
                        ViewType.DASHBOARD.value: PermissionLevel.READ.value,
                        ViewType.NOTES.value: PermissionLevel.READ.value,
                        ViewType.PRESENCES.value: PermissionLevel.READ.value,
                        ViewType.BULLETINS.value: PermissionLevel.READ.value,
                        ViewType.ELEVES.value: PermissionLevel.WRITE.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.READ.value,
                        ViewType.CLASSES.value: PermissionLevel.READ.value,
                        ViewType.MATIERES.value: PermissionLevel.READ.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.READ.value,
                        ViewType.ROLES.value: PermissionLevel.NONE.value,
                        ViewType.PARAMETRES.value: PermissionLevel.READ.value,
                        ViewType.RAPPORTS.value: PermissionLevel.READ.value,
                        ViewType.FINANCE.value: PermissionLevel.READ.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.WRITE.value,
                        ViewType.SALES.value: PermissionLevel.READ.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.READ.value,
                        ViewType.EMPLOIS.value: PermissionLevel.READ.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.READ.value
                    },
                    "Surveillant": {
                        ViewType.DASHBOARD.value: PermissionLevel.READ.value,
                        ViewType.NOTES.value: PermissionLevel.NONE.value,
                        ViewType.PRESENCES.value: PermissionLevel.WRITE.value,
                        ViewType.BULLETINS.value: PermissionLevel.NONE.value,
                        ViewType.ELEVES.value: PermissionLevel.READ.value,
                        ViewType.PROFESSEURS.value: PermissionLevel.READ.value,
                        ViewType.CLASSES.value: PermissionLevel.READ.value,
                        ViewType.MATIERES.value: PermissionLevel.NONE.value,
                        ViewType.UTILISATEURS.value: PermissionLevel.NONE.value,
                        ViewType.ROLES.value: PermissionLevel.NONE.value,
                        ViewType.PARAMETRES.value: PermissionLevel.NONE.value,
                        ViewType.RAPPORTS.value: PermissionLevel.READ.value,
                        ViewType.FINANCE.value: PermissionLevel.NONE.value,
                        ViewType.BIBLIOTHEQUE.value: PermissionLevel.READ.value,
                        ViewType.CALENDRIER.value: PermissionLevel.READ.value,
                        ViewType.SALES.value: PermissionLevel.READ.value,
                        ViewType.ENSEIGNEMENTS.value: PermissionLevel.NONE.value,
                        ViewType.EMPLOIS.value: PermissionLevel.READ.value,
                        ViewType.PAIEMENTS.value: PermissionLevel.NONE.value
                    }
                }
                
                # Insérer les permissions par défaut
                for role_id, role_name in roles:
                    if role_name in default_permissions:
                        for view_name, permission_level in default_permissions[role_name].items():
                            try:
                                cursor.execute('''
                                    INSERT OR REPLACE INTO role_view_permissions 
                                    (role_id, view_name, permission_level) 
                                    VALUES (?, ?, ?)
                                ''', (role_id, view_name, permission_level))
                            except Exception as e:
                                print(f"⚠️ Erreur permission {role_name} -> {view_name}: {e}")
                
                conn.commit()
                print("✅ Permissions par défaut créées")
        except Exception as e:
            print(f"❌ Erreur création permissions par défaut: {e}")

    def get_user_view_permissions(self, user_id: int) -> Dict[str, str]:
        """Récupère les permissions de vues d'un utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Récupérer les rôles de l'utilisateur et leurs permissions
                cursor.execute('''
                    SELECT DISTINCT vp.view_name, vp.permission_level
                    FROM role_view_permissions vp
                    JOIN user_roles ur ON vp.role_id = ur.role_id
                    WHERE ur.user_id = ?
                    ORDER BY vp.view_name
                ''', (user_id,))
                
                permissions = {}
                for view_name, permission_level in cursor.fetchall():
                    # Si l'utilisateur a plusieurs rôles, prendre le plus élevé
                    if view_name not in permissions or self._is_higher_permission(permission_level, permissions[view_name]):
                        permissions[view_name] = permission_level
                
                return permissions
        except Exception as e:
            print(f"❌ Erreur récupération permissions utilisateur: {e}")
            return {}

    def _is_higher_permission(self, perm1: str, perm2: str) -> bool:
        """Vérifie si perm1 est plus élevée que perm2"""
        levels = {
            PermissionLevel.NONE.value: 0,
            PermissionLevel.READ.value: 1,
            PermissionLevel.WRITE.value: 2,
            PermissionLevel.DELETE.value: 3,
            PermissionLevel.ADMIN.value: 4
        }
        return levels.get(perm1, 0) > levels.get(perm2, 0)

    def can_access_view(self, user_id: int, view_name: str) -> bool:
        """Vérifie si un utilisateur peut accéder à une vue"""
        try:
            permissions = self.get_user_view_permissions(user_id)
            return permissions.get(view_name, PermissionLevel.NONE.value) != PermissionLevel.NONE.value
        except Exception as e:
            print(f"❌ Erreur vérification accès vue: {e}")
            return False

    def get_view_permission_level(self, user_id: int, view_name: str) -> str:
        """Récupère le niveau de permission d'un utilisateur pour une vue"""
        try:
            permissions = self.get_user_view_permissions(user_id)
            return permissions.get(view_name, PermissionLevel.NONE.value)
        except Exception as e:
            print(f"❌ Erreur récupération niveau permission: {e}")
            return PermissionLevel.NONE.value

    def can_perform_action(self, user_id: int, view_name: str, action: str) -> bool:
        """Vérifie si un utilisateur peut effectuer une action spécifique"""
        try:
            permission_level = self.get_view_permission_level(user_id, view_name)
            
            if action == "view":
                return permission_level != PermissionLevel.NONE.value
            elif action == "create" or action == "edit":
                return permission_level in [PermissionLevel.WRITE.value, PermissionLevel.DELETE.value, PermissionLevel.ADMIN.value]
            elif action == "delete":
                return permission_level in [PermissionLevel.DELETE.value, PermissionLevel.ADMIN.value]
            elif action == "admin":
                return permission_level == PermissionLevel.ADMIN.value
            
            return False
        except Exception as e:
            print(f"❌ Erreur vérification action: {e}")
            return False

    def get_user_role_name(self, user_id: int) -> str:
        """Récupère le nom du rôle principal d'un utilisateur"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT r.nom FROM roles r
                    JOIN user_roles ur ON r.id_role = ur.role_id
                    WHERE ur.user_id = ?
                    LIMIT 1
                ''', (user_id,))
                result = cursor.fetchone()
                return result[0] if result else "Utilisateur"
        except Exception as e:
            print(f"❌ Erreur récupération rôle utilisateur: {e}")
            return "Utilisateur"

    def get_accessible_views_for_user(self, user_id: int) -> List[str]:
        """Récupère la liste des vues accessibles pour un utilisateur"""
        try:
            permissions = self.get_user_view_permissions(user_id)
            return [view for view, level in permissions.items() if level != PermissionLevel.NONE.value]
        except Exception as e:
            print(f"❌ Erreur récupération vues accessibles: {e}")
            return []

    def get_views_with_permission_level(self, user_id: int, min_level: str) -> List[str]:
        """Récupère les vues où l'utilisateur a au moins le niveau de permission spécifié"""
        try:
            permissions = self.get_user_view_permissions(user_id)
            min_level_value = {
                PermissionLevel.NONE.value: 0,
                PermissionLevel.READ.value: 1,
                PermissionLevel.WRITE.value: 2,
                PermissionLevel.DELETE.value: 3,
                PermissionLevel.ADMIN.value: 4
            }.get(min_level, 0)
            
            return [
                view for view, level in permissions.items()
                if {
                    PermissionLevel.NONE.value: 0,
                    PermissionLevel.READ.value: 1,
                    PermissionLevel.WRITE.value: 2,
                    PermissionLevel.DELETE.value: 3,
                    PermissionLevel.ADMIN.value: 4
                }.get(level, 0) >= min_level_value
            ]
        except Exception as e:
            print(f"❌ Erreur récupération vues avec niveau minimum: {e}")
            return []

    def get_user_permissions_summary(self, user_id: int) -> Dict[str, any]:
        """Récupère un résumé complet des permissions d'un utilisateur"""
        try:
            permissions = self.get_user_view_permissions(user_id)
            role_name = self.get_user_role_name(user_id)
            accessible_views = self.get_accessible_views_for_user(user_id)
            
            return {
                "role": role_name,
                "total_views": len(permissions),
                "accessible_views": len(accessible_views),
                "permissions": permissions,
                "can_admin": any(level == PermissionLevel.ADMIN.value for level in permissions.values()),
                "can_write": any(level in [PermissionLevel.WRITE.value, PermissionLevel.DELETE.value, PermissionLevel.ADMIN.value] for level in permissions.values())
            }
        except Exception as e:
            print(f"❌ Erreur résumé permissions: {e}")
            return {}
