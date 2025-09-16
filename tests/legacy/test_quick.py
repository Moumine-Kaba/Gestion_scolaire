#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Rapide du Système - EduManager+
Vérifie les composants essentiels sans lancer l'interface
"""
import os
import sys
import sqlite3

def test_database():
    """Test de la base de données"""
    print("🔍 Test de la base de données...")
    
    db_path = "database/edumanager.db"
    if not os.path.exists(db_path):
        print("❌ Base de données introuvable")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables essentielles
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        essential_tables = ['utilisateurs', 'roles', 'user_roles', 'role_view_permissions']
        missing_tables = [table for table in essential_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Tables manquantes: {', '.join(missing_tables)}")
            conn.close()
            return False
        
        print(f"✅ Tables trouvées: {len(tables)}")
        print(f"   Tables essentielles: {', '.join(essential_tables)}")
        
        # Vérifier les utilisateurs
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        user_count = cursor.fetchone()[0]
        print(f"✅ Utilisateurs: {user_count}")
        
        # Vérifier les rôles
        cursor.execute("SELECT COUNT(*) FROM roles")
        role_count = cursor.fetchone()[0]
        print(f"✅ Rôles: {role_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def test_imports():
    """Test des imports des modules"""
    print("\n🔍 Test des imports...")
    
    modules_to_test = [
        ('models.auth', 'AuthManager'),
        ('models.role', 'RoleManager'),
        ('models.permissions', 'PermissionManager'),
        ('views.view_manager', 'ViewManager'),
        ('views.dashboard_view', 'MainApp')
    ]
    
    all_ok = True
    for module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            class_obj = getattr(module, class_name)
            print(f"✅ {module_path}.{class_name}")
        except Exception as e:
            print(f"❌ {module_path}.{class_name}: {e}")
            all_ok = False
    
    return all_ok

def test_view_creation():
    """Test de la création des vues"""
    print("\n🔍 Test de la création des vues...")
    
    try:
        from views.dashboard_view import VIEW_MAP, PlaceholderView
        
        # Créer un parent factice pour les tests
        class MockParent:
            def pack_forget(self): pass
            def pack(self, **kwargs): pass
        
        mock_parent = MockParent()
        
        all_ok = True
        for view_name, view_class in VIEW_MAP.items():
            try:
                # Essayer de créer la vue
                if view_name == "dashboard":
                    continue  # Skip dashboard
                
                try:
                    # Essayer avec 2 arguments
                    view = view_class(mock_parent, {})
                    print(f"✅ {view_name} (2 args)")
                except TypeError:
                    try:
                        # Essayer avec 1 argument
                        view = view_class(mock_parent)
                        print(f"✅ {view_name} (1 arg)")
                    except Exception as e:
                        print(f"❌ {view_name}: {e}")
                        all_ok = False
                        
            except Exception as e:
                print(f"❌ {view_name}: {e}")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Erreur test vues: {e}")
        return False

def test_permissions():
    """Test du système de permissions"""
    print("\n🔍 Test du système de permissions...")
    
    try:
        from models.permissions import PermissionManager
        from models.auth import AuthManager
        
        db_path = "database/edumanager.db"
        
        # Test PermissionManager
        pm = PermissionManager(db_path)
        print("✅ PermissionManager créé")
        
        # Test AuthManager
        am = AuthManager(db_path)
        print("✅ AuthManager créé")
        
        # Test de connexion
        user_info = am.authenticate_user("admin", "admin123")
        if user_info:
            print(f"✅ Connexion admin réussie: {user_info.get('username')}")
            
            # Test des permissions
            permissions = pm.get_user_view_permissions(user_info['id_utilisateur'])
            print(f"✅ Permissions récupérées: {len(permissions)} vues")
            
            return True
        else:
            print("❌ Connexion admin échouée")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test permissions: {e}")
        return False

def main():
    """Test principal"""
    print("🧪 TEST RAPIDE DU SYSTÈME EDUMANAGER+")
    print("=" * 50)
    
    tests = [
        ("Base de données", test_database),
        ("Imports des modules", test_imports),
        ("Création des vues", test_view_creation),
        ("Système de permissions", test_permissions)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DES TESTS")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{len(results)} tests réussis")
    
    if passed == len(results):
        print("🎉 Tous les tests sont passés ! Le système est prêt.")
        print("💡 Vous pouvez maintenant lancer l'application avec: python main.py")
    else:
        print("⚠️  Certains tests ont échoué.")
        print("💡 Utilisez python repair_system.py pour corriger les problèmes")
    
    return passed == len(results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
