#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'Accès aux Vues basé sur les Rôles
EduManager+ - Gestion Scolaire
"""

import sqlite3
import os
from typing import Dict, List, Optional, Set
from src.modules.view_permissions import ViewPermissions

class ViewAccessManager:
    """Gestionnaire d'accès aux vues basé sur les rôles utilisateur"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Créer le dossier database s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_view_access_table()
    
    def _init_view_access_table(self):
        """Initialise la table de contrôle d'accès aux vues"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table de contrôle d'accès aux vues par utilisateur
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_view_access (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    view_name TEXT NOT NULL,
                    access_level TEXT DEFAULT 'read',
                    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    granted_by INTEGER,
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                    FOREIGN KEY (granted_by) REFERENCES utilisateurs (id_utilisateur),
                    UNIQUE(user_id, view_name)
                )
            ''')
            
            # Table des vues disponibles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS available_views (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    view_name TEXT UNIQUE NOT NULL,
                    view_title TEXT NOT NULL,
                    view_description TEXT,
                    module TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Insérer les vues disponibles par défaut
            self._insert_default_views()
            
            print("✅ Table de contrôle d'accès aux vues initialisée")
            
        except Exception as e:
            print(f"❌ Erreur initialisation table accès vues: {e}")
    
    def _insert_default_views(self):
        """Insère les vues disponibles par défaut"""
        try:
            default_views = [
                ("dashboard", "Tableau de bord", "Vue principale de l'application", "SCOLARITÉ"),
                ("eleves", "Élèves", "Gestion des élèves", "SCOLARITÉ"),
                ("profs", "Professeurs", "Gestion des professeurs", "SCOLARITÉ"),
                ("classes", "Classes", "Gestion des classes", "SCOLARITÉ"),
                ("salles", "Salles", "Gestion des salles", "SCOLARITÉ"),
                ("enseignements", "Enseignements", "Gestion des enseignements", "PÉDAGOGIE"),
                ("matieres", "Matières", "Gestion des matières", "PÉDAGOGIE"),
                ("notes", "Notes", "Gestion des notes", "PÉDAGOGIE"),
                ("presences", "Présences", "Gestion des présences", "PÉDAGOGIE"),
                ("bulletins", "Bulletins", "Gestion des bulletins", "PÉDAGOGIE"),
                ("emplois", "Emplois du temps", "Gestion des emplois du temps", "PÉDAGOGIE"),
                ("paiements", "Paiements", "Gestion des paiements", "FINANCES"),
                ("utilisateurs", "Utilisateurs", "Gestion des utilisateurs", "ADMINISTRATION"),
                ("actualites", "Actualités", "Gestion des actualités", "ADMINISTRATION"),
                ("annonces", "Annonces", "Gestion des annonces", "ADMINISTRATION"),
                ("notifications", "Notifications", "Gestion des notifications", "ADMINISTRATION"),
                ("taches", "Tâches", "Gestion des tâches", "ADMINISTRATION"),
                ("biblio", "Bibliothèque", "Gestion de la bibliothèque", "OUTILS"),
                ("calendriers", "Calendriers", "Gestion des calendriers", "OUTILS"),
                ("carrieres", "Carrières", "Gestion des carrières", "OUTILS"),
                ("competences", "Compétences", "Gestion des compétences", "OUTILS"),
                ("documents", "Documents", "Gestion des documents", "OUTILS"),
                ("maintenances", "Maintenance", "Gestion de la maintenance", "OUTILS"),
                ("messagerie", "Messagerie", "Gestion de la messagerie", "OUTILS"),
                ("objectifs", "Objectifs", "Gestion des objectifs", "OUTILS"),
                ("personnel", "Personnel", "Gestion du personnel", "OUTILS"),
                ("transfert", "Transfert", "Gestion des transferts", "OUTILS"),
                ("settings", "Paramètres", "Paramètres du système", "OUTILS")
            ]
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for view_name, view_title, view_description, module in default_views:
                cursor.execute('''
                    INSERT OR IGNORE INTO available_views (view_name, view_title, view_description, module)
                    VALUES (?, ?, ?, ?)
                ''', (view_name, view_title, view_description, module))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Erreur insertion vues par défaut: {e}")
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Récupère le rôle principal d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom FROM roles r
                JOIN user_roles ur ON r.id_role = ur.role_id
                WHERE ur.user_id = ?
                ORDER BY r.niveau DESC
                LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            print(f"⚠️ Erreur récupération rôle utilisateur {user_id}: {e}")
            return None
    
    def get_user_roles(self, user_id: int) -> List[str]:
        """Récupère tous les rôles d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom FROM roles r
                JOIN user_roles ur ON r.id_role = ur.role_id
                WHERE ur.user_id = ?
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [row[0] for row in results]
            
        except Exception as e:
            print(f"⚠️ Erreur récupération rôles utilisateur {user_id}: {e}")
            return []
    
    def can_access_view(self, user_id: int, view_name: str) -> bool:
        """Vérifie si un utilisateur peut accéder à une vue spécifique"""
        try:
            # Récupérer le rôle principal de l'utilisateur
            user_role = self.get_user_role(user_id)
            if not user_role:
                return False
            
            # Vérifier les permissions basées sur le rôle
            if ViewPermissions.can_access_view(user_role, view_name):
                return True
            
            # Vérifier les permissions personnalisées dans la base de données
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT access_level FROM user_view_access
                WHERE user_id = ? AND view_name = ?
            ''', (user_id, view_name))
            
            result = cursor.fetchone()
            conn.close()
            
            # Si l'utilisateur a des permissions personnalisées
            if result:
                return result[0] in ['read', 'write', 'delete', 'admin']
            
            return False
            
        except Exception as e:
            print(f"⚠️ Erreur vérification accès vue {view_name} pour utilisateur {user_id}: {e}")
            return False
    
    def get_accessible_views(self, user_id: int) -> List[str]:
        """Récupère la liste des vues accessibles pour un utilisateur"""
        try:
            user_role = self.get_user_role(user_id)
            if not user_role:
                return ["dashboard"]
            
            # Récupérer les vues basées sur le rôle
            role_views = ViewPermissions.get_views_for_role(user_role)
            
            # Récupérer les vues personnalisées
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT view_name FROM user_view_access
                WHERE user_id = ? AND access_level IN ('read', 'write', 'delete', 'admin')
            ''', (user_id,))
            
            custom_views = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            # Combiner et dédupliquer
            all_views = list(set(role_views + custom_views))
            
            # S'assurer que le dashboard est toujours accessible
            if "dashboard" not in all_views:
                all_views.insert(0, "dashboard")
            
            return all_views
            
        except Exception as e:
            print(f"⚠️ Erreur récupération vues accessibles pour utilisateur {user_id}: {e}")
            return ["dashboard"]
    
    def get_navigation_sections(self, user_id: int) -> Dict[str, List[str]]:
        """Récupère les sections de navigation pour un utilisateur"""
        try:
            user_role = self.get_user_role(user_id)
            if not user_role:
                return {"SCOLARITÉ": ["dashboard"]}
            
            # Récupérer les sections basées sur le rôle
            role_sections = ViewPermissions.get_sections_for_role(user_role)
            
            # Filtrer les sections pour ne garder que les vues accessibles
            accessible_views = self.get_accessible_views(user_id)
            filtered_sections = {}
            
            for section_name, views in role_sections.items():
                filtered_views = [view for view in views if view in accessible_views]
                if filtered_views:
                    filtered_sections[section_name] = filtered_views
            
            return filtered_sections
            
        except Exception as e:
            print(f"⚠️ Erreur récupération sections navigation pour utilisateur {user_id}: {e}")
            return {"SCOLARITÉ": ["dashboard"]}
    
    def grant_view_access(self, user_id: int, view_name: str, access_level: str = "read", granted_by: int = None) -> bool:
        """Accorde l'accès à une vue pour un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_view_access (user_id, view_name, access_level, granted_by)
                VALUES (?, ?, ?, ?)
            ''', (user_id, view_name, access_level, granted_by))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Accès à la vue '{view_name}' accordé à l'utilisateur {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur attribution accès vue {view_name} à utilisateur {user_id}: {e}")
            return False
    
    def revoke_view_access(self, user_id: int, view_name: str) -> bool:
        """Révoque l'accès à une vue pour un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM user_view_access
                WHERE user_id = ? AND view_name = ?
            ''', (user_id, view_name))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Accès à la vue '{view_name}' révoqué pour l'utilisateur {user_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur révocation accès vue {view_name} pour utilisateur {user_id}: {e}")
            return False
    
    def get_user_view_permissions(self, user_id: int) -> Dict[str, str]:
        """Récupère toutes les permissions de vues d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT view_name, access_level FROM user_view_access
                WHERE user_id = ?
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            return {row[0]: row[1] for row in results}
            
        except Exception as e:
            print(f"⚠️ Erreur récupération permissions vues utilisateur {user_id}: {e}")
            return {}

