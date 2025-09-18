#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auth Module - Module d'Authentification
=======================================

Ce module gère l'authentification, les rôles et les permissions.
"""

# Module d'authentification - Version minimale pour éviter les imports circulaires

class AuthManager:
    """Gestionnaire d'authentification temporaire"""
    
    def __init__(self):
        self.current_user = None
        self.is_authenticated = False
    
    def login(self, username, password):
        """Authentification temporaire"""
        # Pour l'instant, accepter n'importe quelle connexion
        self.current_user = {"username": username, "id": 1, "roles": "admin"}
        self.is_authenticated = True
        return True
    
    def authenticate_user(self, username, password):
        """Authentification d'un utilisateurs (compatible avec le LoginView)"""
        # Pour l'instant, accepter n'importe quelle connexion
        user_info = {"username": username, "id": 1, "roles": "admin", "email": f"{username}@edumanager.com"}
        self.current_user = user_info
        self.is_authenticated = True
        return user_info
    
    def logout(self):
        """Déconnexion"""
        self.current_user = None
        self.is_authenticated = False
    
    def get_current_user(self):
        """Retourne l'utilisateurs connecté"""
        return self.current_user
    
    def is_user_authenticated(self):
        """Vérifie si un utilisateurs est connecté"""
        return self.is_authenticated

# Instance globale
auth_manager = AuthManager()

__all__ = ['AuthManager', 'auth_manager']

