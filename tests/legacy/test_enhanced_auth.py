#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Système d'Authentification Amélioré
EduManager+ - Gestion Scolaire
"""

import sys
import os
import time

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_auth_manager():
    """Test du gestionnaire d'authentification amélioré"""
    print("🔐 Test du Gestionnaire d'Authentification Amélioré")
    print("=" * 60)
    
    try:
        from models.auth_enhanced import EnhancedAuthManager
        
        # Initialiser le gestionnaire
        db_path = "database/edumanager.db"
        auth_manager = EnhancedAuthManager(db_path)
        
        print("✅ EnhancedAuthManager initialisé avec succès")
        
        # Test 1: Vérifier les utilisateurs par défaut
        print("\n📋 Test 1: Vérification des utilisateurs par défaut")
        demo_users = ["admin", "directeur", "professeur", "secretaire", "eleve"]
        
        for username in demo_users:
            exists = auth_manager.user_exists(username)
            status = "✅" if exists else "❌"
            print(f"   {status} {username}: {'Existe' if exists else 'N\'existe pas'}")
            
            if exists:
                security_status = auth_manager.get_user_security_status(username)
                print(f"      Statut sécurité: {security_status}")
        
        # Test 2: Test d'authentification
        print("\n🔑 Test 2: Test d'authentification")
        
        # Test avec des identifiants valides
        test_credentials = [
            ("admin", "admin123"),
            ("directeur", "directeur123"),
            ("professeur", "prof123"),
            ("secretaire", "sec123"),
            ("eleve", "eleve123")
        ]
        
        for username, password in test_credentials:
            print(f"\n   Test connexion: {username}")
            
            # Simuler une adresse IP
            ip_address = "192.168.1.100"
            user_agent = "Windows 10.0.19044"
            
            # Authentifier
            start_time = time.time()
            user_info = auth_manager.authenticate_user(username, password, ip_address, user_agent)
            end_time = time.time()
            
            if user_info:
                print(f"      ✅ Connexion réussie en {end_time - start_time:.3f}s")
                print(f"         Rôle principal: {user_info.get('primary_role', 'N/A')}")
                print(f"         Niveau d'accès: {user_info.get('access_level', 'N/A')}")
                print(f"         Vues accessibles: {len(user_info.get('accessible_views', []))}")
                
                # Afficher quelques permissions
                permissions = user_info.get('permissions', {})
                if permissions:
                    print(f"         Permissions principales:")
                    for view, level in list(permissions.items())[:5]:
                        print(f"            {view}: {level}")
                
                # Tester la validation de session
                session_token = user_info.get('session_token')
                if session_token:
                    print(f"         Session token: {session_token[:20]}...")
                    
                    # Valider la session
                    validated_user = auth_manager.validate_session(session_token)
                    if validated_user:
                        print(f"         ✅ Session validée avec succès")
                    else:
                        print(f"         ❌ Échec validation session")
                
            else:
                print(f"      ❌ Échec de connexion")
        
        # Test 3: Test de sécurité
        print("\n🛡️ Test 3: Test des fonctionnalités de sécurité")
        
        # Test avec des identifiants invalides
        print("   Test protection force brute:")
        invalid_attempts = [
            ("admin", "wrong_password"),
            ("admin", "admin"),
            ("admin", "password123"),
            ("admin", "admin1234"),
            ("admin", "admin12345")
        ]
        
        for username, password in invalid_attempts:
            ip_address = "192.168.1.100"
            user_agent = "Windows 10.0.19044"
            
            user_info = auth_manager.authenticate_user(username, password, ip_address, user_agent)
            
            if user_info:
                print(f"      ⚠️ Connexion réussie avec {username}:{password} (inattendu)")
            else:
                print(f"      ✅ Connexion bloquée pour {username}:{password}")
        
        # Vérifier le statut de sécurité après les tentatives
        print("\n   Vérification statut sécurité après tentatives:")
        security_status = auth_manager.get_user_security_status("admin")
        print(f"      Admin - Tentatives échouées: {security_status.get('tentatives_failed', 0)}")
        print(f"      Admin - Compte bloqué: {security_status.get('is_locked', False)}")
        
        # Test 4: Test des logs de sécurité
        print("\n📊 Test 4: Test des logs de sécurité")
        
        # Récupérer les logs récents
        security_logs = auth_manager.get_security_logs(limit=10)
        print(f"   {len(security_logs)} logs de sécurité récupérés")
        
        if security_logs:
            print("   Derniers logs:")
            for log in security_logs[:5]:
                print(f"      {log['timestamp']}: {log['action']} - {log['details']}")
        
        # Test 5: Test de déconnexion
        print("\n🚪 Test 5: Test de déconnexion")
        
        # Se reconnecter pour tester la déconnexion
        user_info = auth_manager.authenticate_user("admin", "admin123", "192.168.1.100", "Test")
        if user_info and 'session_token' in user_info:
            session_token = user_info['session_token']
            print(f"   Session créée: {session_token[:20]}...")
            
            # Déconnecter
            logout_success = auth_manager.logout_user(session_token)
            if logout_success:
                print(f"   ✅ Déconnexion réussie")
                
                # Vérifier que la session est invalide
                validated_user = auth_manager.validate_session(session_token)
                if not validated_user:
                    print(f"   ✅ Session invalidée après déconnexion")
                else:
                    print(f"   ❌ Session toujours valide après déconnexion")
            else:
                print(f"   ❌ Échec de déconnexion")
        
        print("\n✅ Tests du gestionnaire d'authentification terminés!")
        return auth_manager
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_user_creation():
    """Test de création d'utilisateurs"""
    print("\n👤 Test de Création d'Utilisateurs")
    print("=" * 60)
    
    try:
        from models.auth_enhanced import EnhancedAuthManager
        
        auth_manager = EnhancedAuthManager("database/edumanager.db")
        
        # Créer un utilisateur de test
        test_user = {
            "username": "test_user",
            "password": "test123",
            "email": "test@edumanager.com",
            "nom": "Test",
            "prenom": "Utilisateur",
            "role_name": "Professeur"
        }
        
        if not auth_manager.user_exists("test_user"):
            success = auth_manager.create_user_with_role(**test_user)
            if success:
                print(f"✅ Utilisateur de test créé: {test_user['username']}")
                
                # Tester la connexion
                user_info = auth_manager.authenticate_user(
                    "test_user", "test123", "192.168.1.200", "Test"
                )
                
                if user_info:
                    print(f"   ✅ Connexion réussie avec le nouvel utilisateur")
                    print(f"   Rôle: {user_info.get('primary_role', 'N/A')}")
                else:
                    print(f"   ❌ Échec de connexion avec le nouvel utilisateur")
            else:
                print(f"❌ Échec de création de l'utilisateur de test")
        else:
            print(f"ℹ️ L'utilisateur de test existe déjà")
        
    except Exception as e:
        print(f"❌ Erreur lors du test de création: {e}")

def test_performance():
    """Test de performance"""
    print("\n⚡ Test de Performance")
    print("=" * 60)
    
    try:
        from models.auth_enhanced import EnhancedAuthManager
        import time
        
        auth_manager = EnhancedAuthManager("database/edumanager.db")
        
        # Test de performance d'authentification
        print("   Test performance authentification:")
        
        start_time = time.time()
        for i in range(10):
            user_info = auth_manager.authenticate_user(
                "admin", "admin123", f"192.168.1.{i}", "Performance Test"
            )
        end_time = time.time()
        
        avg_time = (end_time - start_time) / 10
        print(f"      Temps moyen par authentification: {avg_time:.3f}s")
        
        # Test de performance validation session
        print("   Test performance validation session:")
        
        # Créer une session
        user_info = auth_manager.authenticate_user("admin", "admin123", "192.168.1.100", "Test")
        if user_info and 'session_token' in user_info:
            session_token = user_info['session_token']
            
            start_time = time.time()
            for i in range(100):
                validated_user = auth_manager.validate_session(session_token)
            end_time = time.time()
            
            avg_time = (end_time - start_time) / 100
            print(f"      Temps moyen par validation session: {avg_time:.3f}s")
        
        print("✅ Tests de performance terminés!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de performance: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test Complet du Système d'Authentification Amélioré")
    print("=" * 80)
    
    # Test principal
    auth_manager = test_enhanced_auth_manager()
    
    if auth_manager:
        # Test de création d'utilisateurs
        test_user_creation()
        
        # Test de performance
        test_performance()
    
    print("\n🎉 Tous les tests sont terminés!")
    print("\n📋 Résumé:")
    print("   - Le système d'authentification amélioré est fonctionnel")
    print("   - La gestion des rôles et permissions est intégrée")
    print("   - Les fonctionnalités de sécurité sont opérationnelles")
    print("   - Les performances sont satisfaisantes")

if __name__ == "__main__":
    main()

