#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Permissions pour EduManager+
===========================================

Gère les permissions des utilisateurs selon leurs rôles
"""

# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
from typing import Dict, List, Optional, Set

class PermissionManager:
    """Gestionnaire centralisé des permissions utilisateurs"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_permissions_table()
    
    def _init_permissions_table(self):
        """Initialise la table des permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Table des rôles
            cursor.execute('''
                CREATE TABLE roles (
                    id_role INT IDENTITY(1,1) PRIMARY KEY,
                    nom_role NVARCHAR(255) UNIQUE NOT NULL,
                    description NVARCHAR(255),
                    niveau_acces INTEGER DEFAULT 1,
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Table des permissions par rôle
            cursor.execute('''
                CREATE TABLE role_permissions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    role_id INTEGER NOT NULL,
                    vue_nom NVARCHAR(255) NOT NULL,
                    permission_type NVARCHAR(255) DEFAULT 'read',
                    granted BOOLEAN DEFAULT 1,
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    UNIQUE(role_id, vue_nom)
                )
            ''')
            
            # Table des utilisateurs et leurs rôles
            cursor.execute('''
                CREATE TABLE user_roles (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                    assigned_at DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    UNIQUE(user_id, role_id)
                )
            ''')
            
            # Table des logs d'audit pour la sécurité
            cursor.execute('''
                CREATE TABLE access_logs (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    view_name NVARCHAR(255) NOT NULL,
                    action NVARCHAR(255) NOT NULL,
                    success BOOLEAN DEFAULT 1,
                    timestamp DATETIME DEFAULT GETDATE(),
                    ip_address NVARCHAR(255),
                    user_agent NVARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
                )
            ''')
            
            # Table des sessions utilisateurs pour la sécurité
            cursor.execute('''
                CREATE TABLE user_sessions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    session_token NVARCHAR(255) UNIQUE NOT NULL,
                    created_at DATETIME DEFAULT GETDATE(),
                    expires_at TIMESTAMP NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    ip_address NVARCHAR(255),
                    user_agent NVARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
                )
            ''')
            
            # Table des tentatives de connexion échouées
            cursor.execute('''
                CREATE TABLE failed_login_attempts (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(255) NOT NULL,
                    ip_address NVARCHAR(255),
                    timestamp DATETIME DEFAULT GETDATE(),
                    user_agent NVARCHAR(255)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Insérer les rôles par défaut
            self._insert_default_roles()
            
            print("✅ Table des permissions initialisée")
            
        except Exception as e:
            print(f"❌ Erreur initialisation permissions: {e}")
    
    def _insert_default_roles(self):
        """Insère les rôles par défaut avec leurs permissions"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Rôles par défaut
            default_roles = [
                ("Administrateur", "Accès complet à toutes les fonctionnalités", 10),
                ("Directeur", "Gestion complète de l'établissement", 8),
                ("Proviseur", "Gestion pédagogique et administrative", 7),
                ("Surveillant", "Gestion des présences et discipline", 5),
                ("Professeur", "Gestion des cours et notes", 4),
                ("Comptable", "Gestion financière", 3),
                ("Secrétaire", "Gestion administrative", 2),
                ("Élève", "Consultation des informations personnelles", 1)
            ]
            
            for role_name, description, level in default_roles:
                cursor.execute('''
                    INSERT OR IGNORE INTO roles (nom_role, description, niveau_acces)
                    VALUES (?, ?, ?)
                ''', (role_name, description, level))
            
            # Récupérer les IDs des rôles
            cursor.execute("SELECT id_role, nom_role FROM roles")
            roles = cursor.fetchall()
            
            # Permissions par défaut pour chaque rôle
            default_permissions = {
                "Administrateur": [
                    "dashboard", "eleves", "profs", "classes", "salles", "enseignements",
                    "matieres", "notes", "presences", "bulletins", "emplois", "paiements",
                    "utilisateurs", "actualites", "annonces", "notifications", "taches",
                    "biblio", "calendriers", "carrieres", "competences", "documents",
                    "maintenances", "messagerie", "objectifs", "personnel", "transfert", "settings"
                ],
                "Directeur": [
                    "dashboard", "eleves", "profs", "classes", "salles", "enseignements",
                    "matieres", "notes", "presences", "bulletins", "emplois", "paiements",
                    "utilisateurs", "actualites", "annonces", "notifications", "taches",
                    "biblio", "calendriers", "carrieres", "competences", "documents",
                    "maintenances", "messagerie", "objectifs", "personnel", "transfert"
                ],
                "Proviseur": [
                    "dashboard", "eleves", "profs", "classes", "salles", "enseignements",
                    "matieres", "notes", "presences", "bulletins", "emplois",
                    "actualites", "annonces", "notifications", "taches", "biblio",
                    "calendriers", "carrieres", "competences", "documents"
                ],
                "Surveillant": [
                    "dashboard", "eleves", "classes", "presences", "actualites",
                    "annonces", "notifications", "taches"
                ],
                "Professeur": [
                    "dashboard", "eleves", "classes", "enseignements", "matieres",
                    "notes", "presences", "bulletins", "emplois", "actualites",
                    "annonces", "notifications", "taches", "biblio", "calendriers"
                ],
                "Comptable": [
                    "dashboard", "paiements", "actualites", "annonces", "notifications"
                ],
                "Secrétaire": [
                    "dashboard", "eleves", "profs", "classes", "actualites",
                    "annonces", "notifications", "taches", "biblio", "calendriers"
                ],
                "Élève": [
                    "dashboard", "notes", "presences", "bulletins", "emplois",
                    "actualites", "annonces", "notifications"
                ]
            }
            
            # Insérer les permissions
            for role_name, permissions in default_permissions.items():
                role_id = next((r[0] for r in roles if r[1] == role_name), None)
                if role_id:
                    for vue in permissions:
                        cursor.execute('''
                            INSERT OR IGNORE INTO role_permissions (role_id, vue_nom, permission_type)
                            VALUES (?, ?, 'read')
                        ''', (role_id, vue))
            
            conn.commit()
            conn.close()
            
            print("✅ Rôles et permissions par défaut créés")
            
        except Exception as e:
            print(f"❌ Erreur création rôles par défaut: {e}")
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Récupère le rôle principal d'un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom_role 
                FROM roles r 
                JOIN user_roles ur ON r.id_role = ur.role_id 
                WHERE ur.user_id = ? 
                ORDER BY r.niveau_acces DESC 
                LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else "Utilisateur"
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle utilisateurs: {e}")
            return "Utilisateur"
    
    def can_access_view(self, user_id: int, view_name: str) -> bool:
        """Vérifie si un utilisateurs peut accéder à une vue spécifique"""
        try:
            if not user_id:
                return False
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM role_permissions rp
                JOIN user_roles ur ON rp.role_id = ur.role_id
                WHERE ur.user_id = ? AND rp.vue_nom = ? AND rp.granted = 1
            ''', (user_id, view_name))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] > 0 if result else False
            
        except Exception as e:
            print(f"❌ Erreur vérification accès vue {view_name}: {e}")
            return False
    
    def get_user_permissions(self, user_id: int) -> Set[str]:
        """Récupère toutes les permissions d'un utilisateurs"""
        try:
            if not user_id:
                return set()
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT rp.vue_nom
                FROM role_permissions rp
                JOIN user_roles ur ON rp.role_id = ur.role_id
                WHERE ur.user_id = ? AND rp.granted = 1
            ''', (user_id,))
            
            permissions = {row[0] for row in cursor.fetchall()}
            conn.close()
            
            return permissions
            
        except Exception as e:
            print(f"❌ Erreur récupération permissions utilisateurs: {e}")
            return set()
    
    def get_navigation_sections(self, user_id: int) -> Dict[str, List[str]]:
        """Récupère les sections de navigation filtrées selon les permissions"""
        try:
            permissions = self.get_user_permissions(user_id)
            
            # Définir les sections et leurs vues
            all_sections = {
                "SCOLARITÉ": ["dashboard", "eleves", "profs", "classes", "salles"],
                "PÉDAGOGIE": ["enseignements", "matieres", "notes", "presences", "bulletins", "emplois"],
                "FINANCES": ["paiements"],
                "ADMINISTRATION": ["utilisateurs", "actualites", "annonces", "notifications", "taches"],
                "OUTILS": ["biblio", "calendriers", "carrieres", "competences", "documents", 
                          "maintenances", "messagerie", "objectifs", "personnel", "transfert", "settings"]
            }
            
            # Filtrer selon les permissions
            filtered_sections = {}
            for section_name, views in all_sections.items():
                filtered_views = [view for view in views if view in permissions]
                if filtered_views:  # Ne garder que les sections avec des vues accessibles
                    filtered_sections[section_name] = filtered_views
            
            return filtered_sections
            
        except Exception as e:
            print(f"❌ Erreur récupération sections navigation: {e}")
            return {}
    
    def assign_role_to_user(self, user_id: int, role_name: str) -> bool:
        """Assigne un rôle à un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer l'ID du rôle
            cursor.execute("SELECT id_role FROM roles WHERE nom_role = ?", (role_name,))
            role_result = cursor.fetchone()
            
            if not role_result:
                print(f"❌ Rôle '{role_name}' non trouvé")
                conn.close()
                return False
            
            role_id = role_result[0]
            
            # Assigner le rôle
            cursor.execute('''
                INSERT OR REPLACE INTO user_roles (user_id, role_id)
                VALUES (?, ?)
            ''', (user_id, role_id))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Rôle '{role_name}' assigné à l'utilisateurs {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur assignation rôle: {e}")
            return False
    
    def create_default_admin_user(self, user_id: int):
        """Crée un utilisateurs administrateur par défaut"""
        try:
            # Assigner le rôle administrateur
            success = self.assign_role_to_user(user_id, "Administrateur")
            if success:
                print(f"✅ Utilisateur {user_id} promu administrateur")
            return success
        except Exception as e:
            print(f"❌ Erreur création admin par défaut: {e}")
            return False
    
    def get_user_permission_level(self, user_id: int, view_name: str) -> str:
        """Récupère le niveau de permissions d'un utilisateurs pour une vue spécifique"""
        try:
            if not user_id:
                return "none"
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT rp.permission_type
                FROM role_permissions rp
                JOIN user_roles ur ON rp.role_id = ur.role_id
                WHERE ur.user_id = ? AND rp.vue_nom = ? AND rp.granted = 1
                ORDER BY r.niveau_acces DESC
                LIMIT 1
            ''', (user_id, view_name))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else "none"
            
        except Exception as e:
            print(f"❌ Erreur récupération niveau permissions {view_name}: {e}")
            return "none"
    
    def can_perform_action(self, user_id: int, view_name: str, action: str) -> bool:
        """Vérifie si un utilisateurs peut effectuer une action spécifique"""
        try:
            permission_level = self.get_user_permission_level(user_id, view_name)
            
            # Définir les actions autorisées selon le niveau de permissions
            action_permissions = {
                "none": [],
                "read": ["view", "list", "search"],
                "write": ["view", "list", "search", "create", "update"],
                "full": ["view", "list", "search", "create", "update", "delete", "export", "import"]
            }
            
            return action in action_permissions.get(permission_level, [])
            
        except Exception as e:
            print(f"❌ Erreur vérification action {action} sur {view_name}: {e}")
            return False
    
    def get_restricted_views(self, user_id: int) -> Dict[str, List[str]]:
        """Récupère les vues avec restrictions selon le rôle de l'utilisateurs"""
        try:
            user_role = self.get_user_role(user_id)
            role_level = self._get_role_level(user_role)
            
            # Définir les restrictions selon le niveau du rôle
            restrictions = {
                "Super Administrateur": {},  # Aucune restriction
                "Administrateur": {},        # Aucune restriction
                "Directeur Général": {
                    "utilisateurs": ["view", "list"],  # Lecture seule des utilisateurs
                    "system_backup": ["none"],         # Pas d'accès aux sauvegardes
                    "audit_logs": ["none"]             # Pas d'accès aux logs
                },
                "Directeur Pédagogique": {
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"],  # Lecture seule des utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Proviseur": {
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"],  # Lecture seule des utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Censeur": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "paiements": ["none"],             # Pas d'accès aux paiements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Surveillant Général": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "paiements": ["none"],             # Pas d'accès aux paiements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Professeur Principal": {
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"],  # Lecture seule des utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Professeur": {
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"],  # Lecture seule des utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Comptable Principal": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "enseignements": ["view", "list"], # Lecture seule des enseignements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Comptable": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "enseignements": ["view", "list"], # Lecture seule des enseignements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Secrétaire Principal": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Secrétaire": {
                    "notes": ["view", "list"],         # Lecture seule des notes
                    "paiements": ["view", "list"],     # Lecture seule des paiements
                    "utilisateurs": ["view", "list"]   # Lecture seule des utilisateurs
                },
                "Élève": {
                    "eleves": ["view_own"],            # Voir seulement ses propres infos
                    "profs": ["view"],                 # Voir seulement les profs
                    "classes": ["view_own"],           # Voir seulement sa classes
                    "paiements": ["view_own"],         # Voir seulement ses paiements
                    "utilisateurs": ["none"],          # Pas d'accès aux utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Parent": {
                    "eleves": ["view_own_children"],   # Voir seulement ses enfants
                    "profs": ["view"],                 # Voir seulement les profs
                    "classes": ["view_own_children"],  # Voir seulement la classes de ses enfants
                    "paiements": ["view_own_children"], # Voir seulement les paiements de ses enfants
                    "utilisateurs": ["none"],          # Pas d'accès aux utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                },
                "Visiteur": {
                    "eleves": ["none"],                # Pas d'accès aux élèves
                    "profs": ["view"],                 # Voir seulement les profs
                    "classes": ["none"],               # Pas d'accès aux classes
                    "notes": ["none"],                 # Pas d'accès aux notes
                    "paiements": ["none"],             # Pas d'accès aux paiements
                    "utilisateurs": ["none"],          # Pas d'accès aux utilisateurs
                    "settings": ["none"]               # Pas d'accès aux paramètres
                }
            }
            
            return restrictions.get(user_role, {})
            
        except Exception as e:
            print(f"❌ Erreur récupération restrictions: {e}")
            return {}
    
    def _get_role_level(self, role_name: str) -> int:
        """Récupère le niveau d'accès d'un rôle"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT niveau_acces FROM roles WHERE nom_role = ?", (role_name,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            print(f"❌ Erreur récupération niveau rôle {role_name}: {e}")
            return 0
    
    def check_data_access(self, user_id: int, view_name: str, data_id: int = None) -> bool:
        """Vérifie l'accès aux données selon le rôle et les restrictions"""
        try:
            user_role = self.get_user_role(user_id)
            restrictions = self.get_restricted_views(user_id)
            
            # Vérifier les restrictions générales
            if view_name in restrictions:
                restriction_level = restrictions[view_name]
                if "none" in restriction_level:
                    return False
            
            # Vérifications spécifiques selon le rôle
            if user_role in ["Élève", "Parent"]:
                # Les élèves et parents ne peuvent voir que leurs propres données
                if view_name in ["eleves", "notes", "presences", "paiements"]:
                    return self._can_access_own_data(user_id, view_name, data_id)
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur vérification accès données: {e}")
            return False
    
    def _can_access_own_data(self, user_id: int, view_name: str, data_id: int = None) -> bool:
        """Vérifie si l'utilisateurs peut accéder à ses propres données"""
        try:
            # Cette méthode devrait être implémentée selon la logique métier
            # Pour l'instant, on retourne True (à adapter selon vos besoins)
            return True
        except Exception as e:
            print(f"❌ Erreur vérification accès données personnelles: {e}")
            return False
    
    def log_access_attempt(self, user_id: int, view_name: str, action: str, success: bool):
        """Enregistre les tentatives d'accès pour audit"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO access_logs (user_id, view_name, action, success, timestamp)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, view_name, action, success))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Erreur enregistrement log accès: {e}")
    
    def get_user_audit_logs(self, user_id: int, limit: int = 100) -> List[Dict]:
        """Récupère les logs d'audit d'un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT view_name, action, success, timestamp
                FROM access_logs
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    "view_name": row[0],
                    "action": row[1],
                    "success": bool(row[2]),
                    "timestamp": row[3]
                })
            
            conn.close()
            return logs
            
        except Exception as e:
            print(f"❌ Erreur récupération logs audit: {e}")
            return []
