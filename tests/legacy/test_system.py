#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test du système d'authentification et de rôles
======================================================

Ce script teste toutes les fonctionnalités du système pour s'assurer
qu'il fonctionne correctement.
"""

import os
import sys
import sqlite3

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_database_creation():
    """Teste la création de la base de données"""
    print("🔍 Test de création de la base de données...")
    
    try:
        # Supprimer la base de données existante pour tester la création
        db_path = "database/edumanager.db"
        if os.path.exists(db_path):
            os.remove(db_path)
            print("✅ Base de données existante supprimée")
        
        # Créer le dossier database
        os.makedirs("database", exist_ok=True)
        
        # Créer une base de données vide
        conn = sqlite3.connect(db_path)
        conn.close()
        
        print("✅ Base de données créée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création base de données: {e}")
        return False

def test_role_system():
    """Teste le système de rôles"""
    print("\n🔍 Test du système de rôles...")
    
    try:
        from models.role import RoleManager, Role
        
        # Initialiser le gestionnaire de rôles
        role_manager = RoleManager("database/edumanager.db")
        
        # Vérifier que les rôles par défaut sont créés
        roles = role_manager.get_all_roles()
        print(f"✅ {len(roles)} rôles créés")
        
        for role in roles:
            print(f"   - {role.nom}: {', '.join(role.permissions)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur système de rôles: {e}")
        return False

def test_auth_system():
    """Teste le système d'authentification"""
    print("\n🔍 Test du système d'authentification...")
    
    try:
        from models.auth import AuthManager
        
        # Initialiser le gestionnaire d'authentification
        auth_manager = AuthManager("database/edumanager.db")
        
        # Vérifier que l'admin est créé
        if auth_manager.user_exists("admin"):
            print("✅ Utilisateur admin créé")
        else:
            print("❌ Utilisateur admin non créé")
            return False
        
        # Tester la connexion
        user_info = auth_manager.authenticate_user("admin", "admin123")
        if user_info:
            print("✅ Connexion admin réussie")
            print(f"   Rôles: {user_info['roles']}")
            print(f"   Permissions: {user_info['permissions']}")
        else:
            print("❌ Échec connexion admin")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur système d'authentification: {e}")
        return False

def test_user_creation():
    """Teste la création d'utilisateurs"""
    print("\n🔍 Test de création d'utilisateurs...")
    
    try:
        from models.auth import AuthManager
        
        auth_manager = AuthManager("database/edumanager.db")
        
        # Créer un utilisateur de test
        test_user = {
            "username": "test_user",
            "password": "test123",
            "email": "test@example.com",
            "nom": "Test",
            "prenom": "User",
            "role_name": "Professeur"
        }
        
        success = auth_manager.create_user(**test_user)
        if success:
            print("✅ Utilisateur de test créé")
            
            # Tester la connexion
            user_info = auth_manager.authenticate_user("test_user", "test123")
            if user_info:
                print("✅ Connexion utilisateur de test réussie")
                print(f"   Rôles: {user_info['roles']}")
            else:
                print("❌ Échec connexion utilisateur de test")
                return False
        else:
            print("❌ Échec création utilisateur de test")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création utilisateur: {e}")
        return False

def test_database_structure():
    """Teste la structure de la base de données"""
    print("\n🔍 Test de la structure de la base de données...")
    
    try:
        conn = sqlite3.connect("database/edumanager.db")
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = [
            "utilisateurs",
            "roles", 
            "role_permissions",
            "user_roles",
            "sessions",
            "login_attempts"
        ]
        
        print("📋 Tables trouvées:")
        for table in tables:
            print(f"   ✅ {table}")
        
        # Vérifier que toutes les tables attendues existent
        missing_tables = set(expected_tables) - set(tables)
        if missing_tables:
            print(f"❌ Tables manquantes: {missing_tables}")
            return False
        
        # Vérifier la structure de la table utilisateurs
        cursor.execute("PRAGMA table_info(utilisateurs)")
        columns = [row[1] for row in cursor.fetchall()]
        
        expected_columns = [
            "id_utilisateur", "username", "email", "password_hash", "salt",
            "nom", "prenom", "telephone", "date_naissance", "adresse",
            "statut", "derniere_connexion", "created_at", "updated_at"
        ]
        
        print("📋 Colonnes de la table utilisateurs:")
        for col in columns:
            print(f"   ✅ {col}")
        
        missing_columns = set(expected_columns) - set(columns)
        if missing_columns:
            print(f"❌ Colonnes manquantes: {missing_columns}")
            return False
        
        conn.close()
        print("✅ Structure de la base de données correcte")
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification structure: {e}")
        return False

def test_permissions():
    """Teste le système de permissions"""
    print("\n🔍 Test du système de permissions...")
    
    try:
        from models.role import RoleManager
        from models.auth import AuthManager
        
        role_manager = RoleManager("database/edumanager.db")
        auth_manager = AuthManager("database/edumanager.db")
        
        # Tester les permissions d'un rôle
        admin_role = role_manager.get_role_by_name("Super Administrateur")
        if admin_role:
            print(f"✅ Rôle Super Administrateur trouvé")
            print(f"   Permissions: {admin_role.permissions}")
            
            # Vérifier les permissions
            if admin_role.is_admin():
                print("   ✅ Permission admin OK")
            else:
                print("   ❌ Permission admin manquante")
                return False
                
            if admin_role.can_read():
                print("   ✅ Permission read OK")
            else:
                print("   ❌ Permission read manquante")
                return False
        else:
            print("❌ Rôle Super Administrateur non trouvé")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test permissions: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests du système...")
    print("=" * 50)
    
    tests = [
        ("Création de la base de données", test_database_creation),
        ("Système de rôles", test_role_system),
        ("Système d'authentification", test_auth_system),
        ("Création d'utilisateurs", test_user_creation),
        ("Structure de la base de données", test_database_structure),
        ("Système de permissions", test_permissions)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Test: {test_name}")
            result = test_func()
            results.append((test_name, result))
            
            if result:
                print(f"✅ {test_name}: SUCCÈS")
            else:
                print(f"❌ {test_name}: ÉCHEC")
                
        except Exception as e:
            print(f"❌ {test_name}: ERREUR - {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    success_count = sum(1 for _, result in results if result)
    total_count = len(results)
    
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{test_name:<30} {status}")
    
    print(f"\n🎯 Résultat global: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont passés avec succès!")
        print("✅ Le système est prêt à être utilisé!")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return success_count == total_count

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🚀 Vous pouvez maintenant lancer l'application avec: python main.py")
        else:
            print("\n❌ Des problèmes ont été détectés. Corrigez-les avant de lancer l'application.")
    except Exception as e:
        print(f"❌ Erreur critique lors des tests: {e}")
        import traceback
        traceback.print_exc()
