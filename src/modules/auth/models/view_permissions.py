#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration des Permissions d'Accès aux Vues par Rôle
EduManager+ - Gestion Scolaire
"""

from typing import Dict, List, Set

class ViewPermissions:
    """Configuration des permissions d'accès aux vues par rôle"""
    
    # Mapping des vues accessibles par rôle
    ROLE_VIEWS = {
        "Super Administrateur": {
            "description": "Accès complet à tous les modules et fonctionnalités",
            "views": [
                "dashboard", "eleves", "profs", "classes", "salles",
                "enseignements", "matieres", "notes", "presences", "bulletins",
                "emplois", "paiements", "utilisateurs", "actualites", "annonces",
                "notifications", "taches", "biblio", "calendriers", "carrieres",
                "competences", "documents", "emplois", "maintenances", "messagerie",
                "objectifs", "personnel", "transfert", "settings"
            ]
        },
        
        "Administrateur": {
            "description": "Gestion complète de l'établissement",
            "views": [
                "dashboard", "eleves", "profs", "classes", "salles",
                "enseignements", "matieres", "notes", "presences", "bulletins",
                "emplois", "paiements", "utilisateurs", "actualites", "annonces",
                "notifications", "taches", "biblio", "calendriers", "carrieres",
                "competences", "documents", "emplois", "maintenances", "messagerie",
                "objectifs", "personnel", "transfert"
            ]
        },
        
        "Directeur": {
            "description": "Gestion des classes, élèves et professeurs",
            "views": [
                "dashboard", "eleves", "profs", "classes", "salles",
                "enseignements", "matieres", "notes", "presences", "bulletins",
                "emplois", "paiements", "actualites", "annonces", "notifications",
                "calendriers", "carrieres", "competences", "documents", "emplois",
                "messagerie", "objectifs", "personnel"
            ]
        },
        
        "Professeur": {
            "description": "Gestion des notes, présences et bulletins",
            "views": [
                "dashboard", "eleves", "classes", "matieres", "notes", 
                "presences", "bulletins", "emplois", "calendriers", "messagerie",
                "objectifs", "competences"
            ]
        },
        
        "Secrétaire": {
            "description": "Gestion administrative et inscriptions",
            "views": [
                "dashboard", "eleves", "profs", "classes", "salles",
                "enseignements", "matieres", "presences", "bulletins", "emplois",
                "paiements", "actualites", "annonces", "notifications", "calendriers",
                "carrieres", "documents", "messagerie", "personnel"
            ]
        },
        
        "Élève": {
            "description": "Consultation des notes et bulletins",
            "views": [
                "dashboard", "notes", "bulletins", "emplois", "calendriers",
                "messagerie", "objectifs", "competences"
            ]
        },
        
        "Parent": {
            "description": "Consultation des informations de l'élève",
            "views": [
                "dashboard", "notes", "bulletins", "emplois", "calendriers",
                "messagerie", "objectifs", "competences"
            ]
        }
    }
    
    # Mapping des sections de navigation par rôle
    ROLE_SECTIONS = {
        "Super Administrateur": {
            "SCOLARITÉ": ["dashboard", "eleves", "profs", "classes", "salles"],
            "PÉDAGOGIE": ["enseignements", "matieres", "notes", "presences", "bulletins", "emplois"],
            "FINANCES": ["paiements"],
            "ADMINISTRATION": ["utilisateurs", "actualites", "annonces", "notifications", "taches"],
            "OUTILS": ["biblio", "calendriers", "carrieres", "competences", "documents", "maintenances", "messagerie", "objectifs", "personnel", "transfert", "settings"]
        },
        
        "Administrateur": {
            "SCOLARITÉ": ["dashboard", "eleves", "profs", "classes", "salles"],
            "PÉDAGOGIE": ["enseignements", "matieres", "notes", "presences", "bulletins", "emplois"],
            "FINANCES": ["paiements"],
            "ADMINISTRATION": ["utilisateurs", "actualites", "annonces", "notifications", "taches"],
            "OUTILS": ["biblio", "calendriers", "carrieres", "competences", "documents", "maintenances", "messagerie", "objectifs", "personnel", "transfert"]
        },
        
        "Directeur": {
            "SCOLARITÉ": ["dashboard", "eleves", "profs", "classes", "salles"],
            "PÉDAGOGIE": ["enseignements", "matieres", "notes", "presences", "bulletins", "emplois"],
            "FINANCES": ["paiements"],
            "ADMINISTRATION": ["actualites", "annonces", "notifications"],
            "OUTILS": ["calendriers", "carrieres", "competences", "documents", "emplois", "messagerie", "objectifs", "personnel"]
        },
        
        "Professeur": {
            "SCOLARITÉ": ["dashboard", "eleves", "classes"],
            "PÉDAGOGIE": ["matieres", "notes", "presences", "bulletins", "emplois"],
            "OUTILS": ["calendriers", "messagerie", "objectifs", "competences"]
        },
        
        "Secrétaire": {
            "SCOLARITÉ": ["dashboard", "eleves", "profs", "classes", "salles"],
            "PÉDAGOGIE": ["enseignements", "matieres", "presences", "bulletins", "emplois"],
            "FINANCES": ["paiements"],
            "ADMINISTRATION": ["actualites", "annonces", "notifications"],
            "OUTILS": ["calendriers", "carrieres", "documents", "messagerie", "personnel"]
        },
        
        "Élève": {
            "SCOLARITÉ": ["dashboard"],
            "PÉDAGOGIE": ["notes", "bulletins", "emplois"],
            "OUTILS": ["calendriers", "messagerie", "objectifs", "competences"]
        },
        
        "Parent": {
            "SCOLARITÉ": ["dashboard"],
            "PÉDAGOGIE": ["notes", "bulletins", "emplois"],
            "OUTILS": ["calendriers", "messagerie", "objectifs", "competences"]
        }
    }
    
    @classmethod
    def get_views_for_role(cls, role_name: str) -> List[str]:
        """Retourne la liste des vues accessibles pour un rôle donné"""
        return cls.ROLE_VIEWS.get(role_name, {}).get("views", ["dashboard"])
    
    @classmethod
    def get_sections_for_role(cls, role_name: str) -> Dict[str, List[str]]:
        """Retourne les sections de navigation pour un rôle donné"""
        return cls.ROLE_SECTIONS.get(role_name, {"SCOLARITÉ": ["dashboard"]})
    
    @classmethod
    def can_access_view(cls, role_name: str, view_name: str) -> bool:
        """Vérifie si un rôle peut accéder à une vue spécifique"""
        views = cls.get_views_for_role(role_name)
        return view_name in views
    
    @classmethod
    def get_role_description(cls, role_name: str) -> str:
        """Retourne la description d'un rôle"""
        return cls.ROLE_VIEWS.get(role_name, {}).get("description", "Rôle non défini")
    
    @classmethod
    def get_all_roles(cls) -> List[str]:
        """Retourne la liste de tous les rôles disponibles"""
        return list(cls.ROLE_VIEWS.keys())
    
    @classmethod
    def get_available_views(cls) -> Set[str]:
        """Retourne l'ensemble de toutes les vues disponibles"""
        all_views = set()
        for role_data in cls.ROLE_VIEWS.values():
            all_views.update(role_data.get("views", []))
        return all_views

