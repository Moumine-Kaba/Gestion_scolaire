#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation des utilisateurs de test
===============================================

Ce script crée des utilisateurs de test avec différents rôles
pour tester le système d'authentification et de rôles.
"""

import os
import sys

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.auth import AuthManager

def create_test_users():
    """Crée des utilisateurs de test avec différents rôles"""
    
    print("🚀 Création des utilisateurs de test...")
    
    # Initialiser le gestionnaire d'authentification
    auth_manager = AuthManager("database/edumanager.db")
    
    # Liste des utilisateurs de test
    test_users = [
        {
            "username": "directeur",
            "password": "directeur123",
            "email": "directeur@ecole.com",
            "nom": "Martin",
            "prenom": "Jean",
            "role_name": "Directeur"
        },
        {
            "username": "professeur1",
            "password": "prof123",
            "email": "prof1@ecole.com",
            "nom": "Dubois",
            "prenom": "Marie",
            "role_name": "Professeur"
        },
        {
            "username": "professeur2",
            "password": "prof123",
            "email": "prof2@ecole.com",
            "nom": "Leroy",
            "prenom": "Pierre",
            "role_name": "Professeur"
        },
        {
            "username": "secretaire",
            "password": "sec123",
            "email": "secretaire@ecole.com",
            "nom": "Moreau",
            "prenom": "Sophie",
            "role_name": "Secrétaire"
        },
        {
            "username": "eleve1",
            "password": "eleve123",
            "email": "eleve1@ecole.com",
            "nom": "Petit",
            "prenom": "Lucas",
            "role_name": "Élève"
        },
        {
            "username": "parent1",
            "password": "parent123",
            "email": "parent1@email.com",
            "nom": "Petit",
            "prenom": "Claire",
            "role_name": "Parent"
        }
    ]
    
    # Créer chaque utilisateur
    for user_data in test_users:
        print(f"\n👤 Création de {user_data['username']}...")
        
        success = auth_manager.create_user(
            username=user_data["username"],
            password=user_data["password"],
            email=user_data["email"],
            nom=user_data["nom"],
            prenom=user_data["prenom"],
            role_name=user_data["role_name"]
        )
        
        if success:
            print(f"✅ {user_data['username']} créé avec succès")
        else:
            print(f"❌ Échec création de {user_data['username']}")
    
    print("\n🎉 Initialisation des utilisateurs terminée!")
    print("\n📋 Récapitulatif des comptes de test:")
    print("=" * 50)
    
    for user_data in test_users:
        print(f"👤 {user_data['username']:<15} | {user_data['password']:<12} | {user_data['role_name']}")
    
    print("\n🔑 Compte administrateur par défaut:")
    print("   Username: admin")
    print("   Password: admin123")
    print("   Rôle: Super Administrateur")
    
    print("\n💡 Vous pouvez maintenant vous connecter avec n'importe lequel de ces comptes!")

def main():
    """Fonction principale"""
    try:
        create_test_users()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
