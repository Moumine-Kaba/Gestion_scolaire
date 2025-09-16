#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lancement Principal de l'Application EduManager+ avec Authentification Améliorée
Gestion Scolaire avec Rôles et Permissions
"""

import sys
import os
import traceback
from tkinter import messagebox

# Ajouter le répertoire courant au path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def check_dependencies():
    """Vérifie que toutes les dépendances sont disponibles"""
    print("🔍 Vérification des dépendances...")
    
    required_modules = [
        'customtkinter',
        'PIL',
        'sqlite3',
        'hashlib',
        'secrets',
        'datetime'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"   ❌ {module}")
    
    if missing_modules:
        print(f"\n❌ Modules manquants: {', '.join(missing_modules)}")
        print("   Installez-les avec: pip install " + " ".join(missing_modules))
        return False
    
    print("✅ Toutes les dépendances sont disponibles")
    return True

def check_database():
    """Vérifie l'état de la base de données"""
    print("\n🗄️ Vérification de la base de données...")
    
    try:
        db_path = "database/edumanager.db"
        
        if not os.path.exists(db_path):
            print("   ⚠️ Base de données non trouvée, elle sera créée automatiquement")
            return True
        
        # Vérifier la taille de la base
        size_mb = os.path.getsize(db_path) / (1024 * 1024)
        print(f"   ✅ Base de données trouvée ({size_mb:.2f} MB)")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur vérification base: {e}")
        return False

def initialize_system():
    """Initialise le système complet"""
    print("\n🚀 Initialisation du système...")
    
    try:
        # Vérifier les gestionnaires
        from src.modules.auth_enhanced import EnhancedAuthManager
        from src.modules.role import RoleManager
        from src.modules.permissions import PermissionManager
        
        print("   ✅ Modules d'authentification importés")
        
        # Initialiser la base de données
        db_path = "database/edumanager.db"
        
        # Créer le dossier database s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les gestionnaires
        auth_manager = EnhancedAuthManager(db_path)
        role_manager = RoleManager(db_path)
        permission_manager = PermissionManager(db_path)
        
        print("   ✅ Gestionnaires initialisés")
        
        # Vérifier les rôles et permissions
        roles = role_manager.get_all_roles()
        print(f"   ✅ {len(roles)} rôles configurés")
        
        # Vérifier les utilisateurs par défaut
        demo_users = ["admin", "directeur", "professeur", "secretaire", "eleve"]
        existing_users = []
        
        for username in demo_users:
            if auth_manager.user_exists(username):
                existing_users.append(username)
        
        print(f"   ✅ {len(existing_users)}/{len(demo_users)} utilisateurs de démo créés")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur initialisation: {e}")
        traceback.print_exc()
        return False

def launch_login():
    """Lance l'interface de connexion"""
    print("\n🔐 Lancement de l'interface de connexion...")
    
    try:
        from src.modules.login_enhanced import EnhancedLoginView
        
        # Créer et lancer la vue de connexion
        login_app = EnhancedLoginView()
        login_app.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erreur import vue de connexion: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Erreur lancement connexion: {e}")
        traceback.print_exc()
        return False

def show_error_and_exit(error_msg):
    """Affiche une erreur et quitte l'application"""
    try:
        messagebox.showerror("Erreur Critique", error_msg)
    except:
        print(f"❌ ERREUR CRITIQUE: {error_msg}")
    
    print("\n🛑 Arrêt de l'application")
    sys.exit(1)

def main():
    """Fonction principale"""
    print("🎓 EduManager+ - Gestion Scolaire Intelligente")
    print("=" * 60)
    print("🚀 Démarrage avec authentification améliorée...")
    
    try:
        # Étape 1: Vérifier les dépendances
        if not check_dependencies():
            show_error_and_exit(
                "Certaines dépendances sont manquantes.\n"
                "Vérifiez que Python et les modules requis sont installés."
            )
        
        # Étape 2: Vérifier la base de données
        if not check_database():
            show_error_and_exit(
                "Impossible d'accéder à la base de données.\n"
                "Vérifiez les permissions et l'espace disque."
            )
        
        # Étape 3: Initialiser le système
        if not initialize_system():
            show_error_and_exit(
                "Erreur lors de l'initialisation du système.\n"
                "Vérifiez la configuration et les fichiers de base."
            )
        
        # Étape 4: Lancer l'interface de connexion
        if not launch_login():
            show_error_and_exit(
                "Impossible de lancer l'interface de connexion.\n"
                "Vérifiez l'installation de l'application."
            )
        
        print("\n✅ Application fermée normalement")
        
    except KeyboardInterrupt:
        print("\n⚠️ Application interrompue par l'utilisateur")
    except Exception as e:
        error_msg = f"Erreur inattendue: {str(e)}"
        print(f"\n❌ {error_msg}")
        traceback.print_exc()
        show_error_and_exit(error_msg)

if __name__ == "__main__":
    main()

