# -*- coding: utf-8 -*-
"""
Gestionnaire de permissions
"""

from typing import Dict, List, Optional
from .database_config import connect_db

class PermissionManager:
    """Gestionnaire de permissions pour l'application"""
    
    def __init__(self):
        self.roles_permissions = {
            "admin": [
                "dashboard", "eleves", "professeurs", "classes", "salles",
                "enseignements", "utilisateurs", "matieres", "notes", 
                "presences", "paiements", "bulletins", "emplois"
            ],
            "professeur": [
                "dashboard", "eleves", "classes", "notes", "presences", 
                "bulletins", "emplois"
            ],
            "secretaire": [
                "dashboard", "eleves", "classes", "paiements", "bulletins"
            ],
            "utilisateur": [
                "dashboard"
            ]
        }
    
    def get_user_role(self, user_id: int) -> str:
        """Récupère le rôle d'un utilisateur depuis la base de données"""
        try:
            conn = connect_db()
            if not conn:
                return "utilisateur"
            
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM utilisateurs WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return result[0].lower()
            return "utilisateur"
        except Exception as e:
            print(f"Erreur lors de la récupération du rôle: {e}")
            return "utilisateur"
    
    def can_access_view(self, user_id: int, view_key: str) -> bool:
        """Vérifie si un utilisateur peut accéder à une vue"""
        role = self.get_user_role(user_id)
        permissions = self.roles_permissions.get(role, [])
        return view_key in permissions
    
    def get_available_views_for_user(self, user_id: int) -> List[str]:
        """Retourne la liste des vues disponibles pour un utilisateur"""
        role = self.get_user_role(user_id)
        return self.roles_permissions.get(role, [])
    
    def filter_nav_sections(self, user_id: int, nav_sections: Dict) -> Dict:
        """Filtre les sections de navigation selon les permissions de l'utilisateur"""
        available_views = self.get_available_views_for_user(user_id)
        filtered_sections = {}
        
        for section_title, buttons in nav_sections.items():
            filtered_buttons = []
            for text, key in buttons:
                if key in available_views:
                    filtered_buttons.append((text, key))
            
            if filtered_buttons:
                filtered_sections[section_title] = filtered_buttons
        
        return filtered_sections
    
    def get_user_display_name(self, user_id: int) -> str:
        """Récupère le nom d'affichage d'un utilisateur"""
        try:
            conn = connect_db()
            if not conn:
                return "Utilisateur"
            
            cursor = conn.cursor()
            cursor.execute("SELECT prenom, nom, username FROM utilisateurs WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                prenom, nom, username = result
                if prenom and nom:
                    return f"{prenom} {nom}"
                elif prenom:
                    return prenom
                elif nom:
                    return nom
                else:
                    return username
            return "Utilisateur"
        except Exception as e:
            print(f"Erreur lors de la récupération du nom: {e}")
            return "Utilisateur"

# Instance globale du gestionnaire de permissions
permission_manager = PermissionManager()

