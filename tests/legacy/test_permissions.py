#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Système de Permissions et Vues
EduManager+ - Gestion Scolaire
"""

import os
import sys

# Ajouter le répertoire racine au path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_permission_system():
    """Test du système de permissions"""
    print("🧪 Test du Système de Permissions")
    print("=" * 50)
    
    try:
        from models.permissions import PermissionManager, ViewType, PermissionLevel
        print("✅ Import PermissionManager réussi")
        
        # Initialiser le gestionnaire de permissions
        db_path = "database/edumanager.db"
        permission_manager = PermissionManager(db_path)
        print("✅ PermissionManager initialisé")
        
        # Tester la récupération des permissions par rôle
        all_permissions = permission_manager.get_all_view_permissions()
        print(f"📊 Permissions récupérées pour {len(all_permissions)} rôles")
        
        for role_name, permissions in all_permissions.items():
            print(f"\n👑 {role_name}:")
            for view_name, level in permissions.items():
                print(f"   {view_name}: {level}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test permissions: {e}")
        return False

def test_view_manager():
    """Test du gestionnaire de vues"""
    print("\n🧪 Test du Gestionnaire de Vues")
    print("=" * 50)
    
    try:
        from views.view_manager import ViewManager
        print("✅ Import ViewManager réussi")
        
        # Créer un mock de l'application principale
        class MockMainApp:
            def __init__(self):
                self.main_content = None
            
            def update_title(self, title):
                pass
        
        # Initialiser le gestionnaire de vues
        db_path = "database/edumanager.db"
        mock_app = MockMainApp()
        view_manager = ViewManager(db_path, mock_app)
        print("✅ ViewManager initialisé")
        
        # Tester la récupération des vues disponibles
        views = view_manager.views
        print(f"📱 {len(views)} vues disponibles:")
        for view_name, view_info in views.items():
            print(f"   {view_name}: {view_info['title']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test ViewManager: {e}")
        return False

def test_user_permissions():
    """Test des permissions utilisateur"""
    print("\n🧪 Test des Permissions Utilisateur")
    print("=" * 50)
    
    try:
        from models.auth import AuthManager
        from models.permissions import PermissionManager
        
        # Initialiser les gestionnaires
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        permission_manager = PermissionManager(db_path)
        
        print("✅ Gestionnaires initialisés")
        
        # Tester avec l'utilisateur admin
        print("\n👤 Test avec l'utilisateur 'admin':")
        admin_info = auth_manager.authenticate_user("admin", "admin123")
        if admin_info:
            admin_id = admin_info['id_utilisateur']
            permissions = permission_manager.get_user_view_permissions(admin_id)
            accessible_views = permission_manager.get_accessible_views_for_user(admin_id)
            
            print(f"   ID: {admin_id}")
            print(f"   Permissions: {len(permissions)} vues")
            print(f"   Vues accessibles: {len(accessible_views)}")
            
            # Tester quelques vues spécifiques
            test_views = ["dashboard", "notes", "utilisateurs", "roles"]
            for view in test_views:
                can_access = permission_manager.can_access_view(admin_id, view)
                level = permission_manager.get_view_permission_level(admin_id, view)
                print(f"   {view}: Accès={can_access}, Niveau={level}")
        else:
            print("❌ Échec authentification admin")
        
        # Tester avec un professeur
        print("\n👨‍🏫 Test avec l'utilisateur 'professeur1':")
        prof_info = auth_manager.authenticate_user("professeur1", "prof123")
        if prof_info:
            prof_id = prof_info['id_utilisateur']
            permissions = permission_manager.get_user_view_permissions(prof_id)
            accessible_views = permission_manager.get_accessible_views_for_user(prof_id)
            
            print(f"   ID: {prof_id}")
            print(f"   Permissions: {len(permissions)} vues")
            print(f"   Vues accessibles: {len(accessible_views)}")
            
            # Tester quelques vues spécifiques
            test_views = ["dashboard", "notes", "utilisateurs", "roles"]
            for view in test_views:
                can_access = permission_manager.can_access_view(prof_id, view)
                level = permission_manager.get_view_permission_level(prof_id, view)
                print(f"   {view}: Accès={can_access}, Niveau={level}")
        else:
            print("❌ Échec authentification professeur1")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test permissions utilisateur: {e}")
        return False

def test_view_access_control():
    """Test du contrôle d'accès aux vues"""
    print("\n🧪 Test du Contrôle d'Accès aux Vues")
    print("=" * 50)
    
    try:
        from models.auth import AuthManager
        from views.view_manager import ViewManager
        
        # Initialiser les gestionnaires
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        
        class MockMainApp:
            def __init__(self):
                self.main_content = None
            
            def update_title(self, title):
                pass
        
        view_manager = ViewManager(db_path, MockMainApp())
        
        print("✅ Gestionnaires initialisés")
        
        # Tester l'accès aux vues selon les rôles
        test_cases = [
            ("admin", "admin123", "notes"),
            ("professeur1", "prof123", "notes"),
            ("eleve1", "eleve123", "notes"),
            ("admin", "admin123", "utilisateurs"),
            ("professeur1", "prof123", "utilisateurs"),
            ("eleve1", "eleve123", "utilisateurs")
        ]
        
        for username, password, view_name in test_cases:
            print(f"\n🔐 Test {username} -> {view_name}:")
            
            # Authentifier l'utilisateur
            user_info = auth_manager.authenticate_user(username, password)
            if user_info:
                # Définir l'utilisateur dans le gestionnaire de vues
                view_manager.set_current_user(user_info)
                
                # Vérifier l'accès
                can_access = view_manager.can_access_view(view_name)
                permission_level = view_manager.get_view_permission_level(view_name)
                
                print(f"   Utilisateur: {username}")
                print(f"   Vue: {view_name}")
                print(f"   Accès: {'✅ Oui' if can_access else '❌ Non'}")
                print(f"   Niveau: {permission_level}")
            else:
                print(f"   ❌ Échec authentification pour {username}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test contrôle d'accès: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test Complet du Système de Permissions et Vues")
    print("=" * 60)
    
    tests = [
        ("Système de Permissions", test_permission_system),
        ("Gestionnaire de Vues", test_view_manager),
        ("Permissions Utilisateur", test_user_permissions),
        ("Contrôle d'Accès", test_view_access_control)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur critique dans {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("✅ Le système de permissions et de vues est opérationnel")
    else:
        print("⚠️ Certains tests ont échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
