#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la vue d'inscription
EduManager+ - Gestion Scolaire
"""

import os
import sys
import sqlite3

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_register_view():
    """Teste la vue d'inscription"""
    print("🧪 Test de la vue d'inscription")
    print("=" * 50)
    
    try:
        # Importer la vue d'inscription
        from views.register_view import RegisterView
        
        print("✅ RegisterView importée avec succès")
        
        # Créer un AuthManager factice pour les tests
        class MockAuthManager:
            def __init__(self):
                self.users_created = []
            
            def create_user_simple(self, **kwargs):
                print(f"🔑 Création utilisateur: {kwargs}")
                self.users_created.append(kwargs)
                return True
        
        # Créer la vue d'inscription
        auth_manager = MockAuthManager()
        register_view = RegisterView(auth_manager)
        
        print("✅ RegisterView créée avec succès")
        print(f"   - Titre: {register_view.title()}")
        print(f"   - Géométrie: {register_view.geometry()}")
        print(f"   - AuthManager: {type(auth_manager).__name__}")
        
        # Simuler la création d'un utilisateur
        print(f"\n🧪 Test de création d'utilisateur...")
        
        # Remplir les champs
        register_view.username_var.set("testuser")
        register_view.email_var.set("test@example.com")
        register_view.password_var.set("testpass123")
        register_view.confirm_password_var.set("testpass123")
        register_view.nom_var.set("Test")
        register_view.prenom_var.set("User")
        register_view.telephone_var.set("0123456789")
        
        print("✅ Champs remplis avec succès")
        
        # Tester la validation
        if register_view.validate_form():
            print("✅ Validation du formulaire réussie")
        else:
            print("❌ Échec de la validation du formulaire")
            return False
        
        # Tester la création
        register_view.register()
        
        if len(auth_manager.users_created) > 0:
            print("✅ Utilisateur créé avec succès")
            user = auth_manager.users_created[0]
            print(f"   - Username: {user.get('username')}")
            print(f"   - Email: {user.get('email')}")
            print(f"   - Nom: {user.get('nom')} {user.get('prenom')}")
        else:
            print("❌ Échec de la création de l'utilisateur")
            return False
        
        # Fermer la vue
        register_view.destroy()
        
        print(f"\n🎉 Test de la vue d'inscription réussi!")
        return True
        
    except ImportError as e:
        print(f"❌ Impossible d'importer RegisterView: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_auth_manager_integration():
    """Teste l'intégration avec AuthManager réel"""
    print(f"\n🔐 Test d'intégration avec AuthManager")
    print("=" * 50)
    
    try:
        # Importer AuthManager
        from models.auth import AuthManager
        
        print("✅ AuthManager importé avec succès")
        
        # Initialiser avec la base de données
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        
        print("✅ AuthManager initialisé avec succès")
        
        # Tester la création d'un utilisateur de test
        test_username = "test_integration"
        test_email = "test.integration@example.com"
        
        # Vérifier si l'utilisateur existe déjà
        if auth_manager.user_exists(test_username):
            print(f"⚠️ L'utilisateur {test_username} existe déjà")
            return True
        
        # Créer l'utilisateur
        success = auth_manager.create_user_simple(
            username=test_username,
            password="testpass123",
            email=test_email,
            nom="Test",
            prenom="Integration"
        )
        
        if success:
            print("✅ Utilisateur de test créé avec succès")
            
            # Tester l'authentification
            user_info = auth_manager.authenticate_user(test_username, "testpass123")
            
            if user_info:
                print("✅ Authentification réussie")
                print(f"   - ID: {user_info['id_utilisateur']}")
                print(f"   - Username: {user_info['username']}")
                print(f"   - Rôles: {user_info['roles']}")
            else:
                print("❌ Échec de l'authentification")
                return False
        else:
            print("❌ Échec de la création de l'utilisateur")
            return False
        
        print(f"\n🎉 Test d'intégration réussi!")
        return True
        
    except ImportError as e:
        print(f"❌ Impossible d'importer AuthManager: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de la vue d'inscription")
    print("=" * 60)
    
    # Test de la vue d'inscription
    view_success = test_register_view()
    
    # Test d'intégration avec AuthManager
    integration_success = test_auth_manager_integration()
    
    # Résumé
    print(f"\n📊 Résumé des tests:")
    print(f"  - Vue d'inscription: {'✅ Réussi' if view_success else '❌ Échoué'}")
    print(f"  - Intégration AuthManager: {'✅ Réussi' if integration_success else '❌ Échoué'}")
    
    if view_success and integration_success:
        print(f"\n🎉 Tous les tests sont passés avec succès!")
        print(f"   La vue d'inscription est prête à être utilisée")
    else:
        print(f"\n⚠️ Certains tests ont échoué")
        print(f"   Vérifiez la configuration et les dépendances")
    
    print(f"\n💡 Prochaines étapes:")
    print(f"   1. Lancer l'application: python main.py")
    print(f"   2. Cliquer sur 'Créer un compte' dans la vue de login")
    print(f"   3. Tester la création d'un nouveau compte")

if __name__ == "__main__":
    main()

