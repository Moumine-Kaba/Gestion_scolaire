#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Système de Permissions et Rôles
EduManager+ - Gestion Scolaire
"""

import sqlite3
import os
import sys

# Ajouter le répertoire parent au path pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_permissions_system():
    """Test complet du système de permissions"""
    print("🔐 Test du Système de Permissions et Rôles")
    print("=" * 50)
    
    try:
        # Importer les modules nécessaires
        from models.permissions import PermissionManager
        from models.role import RoleManager
        
        # Initialiser les gestionnaires
        db_path = "database/edumanager.db"
        permission_manager = PermissionManager(db_path)
        role_manager = RoleManager(db_path)
        
        print("✅ Gestionnaires initialisés")
        
        # Test 1: Vérifier les rôles existants
        print("\n📋 Test 1: Vérification des rôles existants")
        roles = role_manager.get_all_roles()
        for role in roles:
            print(f"   - {role.nom}: {role.description}")
            print(f"     Permissions: {', '.join(role.permissions)}")
        
        # Test 2: Vérifier les permissions par défaut
        print("\n🔑 Test 2: Vérification des permissions par défaut")
        all_permissions = permission_manager.get_all_view_permissions()
        for role_name, view_permissions in all_permissions.items():
            print(f"   Rôle: {role_name}")
            for view_name, permission_level in view_permissions.items():
                print(f"     {view_name}: {permission_level}")
        
        # Test 3: Simuler un utilisateur avec différents rôles
        print("\n👤 Test 3: Simulation d'utilisateurs avec différents rôles")
        
        # Créer des utilisateurs de test
        test_users = [
            {"id": 1, "username": "admin", "role": "Super Administrateur"},
            {"id": 2, "username": "directeur", "role": "Directeur"},
            {"id": 3, "username": "professeur", "role": "Professeur"},
            {"id": 4, "username": "eleve", "role": "Élève"},
            {"id": 5, "username": "secretaire", "role": "Secrétaire"}
        ]
        
        for user in test_users:
            print(f"\n   Utilisateur: {user['username']} ({user['role']})")
            
            # Récupérer le rôle de l'utilisateur
            user_roles = role_manager.get_user_roles(user['id'])
            if user_roles:
                role = user_roles[0]
                print(f"     Rôle actuel: {role.nom}")
                
                # Récupérer les permissions de l'utilisateur
                permissions = permission_manager.get_user_view_permissions(user['id'])
                accessible_views = permission_manager.get_accessible_views_for_user(user['id'])
                
                print(f"     Vues accessibles: {len(accessible_views)}")
                print(f"     Permissions détaillées:")
                for view_name, permission_level in permissions.items():
                    print(f"       {view_name}: {permission_level}")
            else:
                print(f"     Aucun rôle assigné")
        
        # Test 4: Vérifier les restrictions d'accès
        print("\n🚫 Test 4: Vérification des restrictions d'accès")
        
        test_views = ["eleves", "notes", "utilisateurs", "finance", "parametres"]
        
        for user in test_users:
            print(f"\n   {user['username']} ({user['role']}):")
            for view in test_views:
                can_access = permission_manager.can_access_view(user['id'], view)
                permission_level = permission_manager.get_view_permission_level(user['id'], view)
                print(f"     {view}: {'✅' if can_access else '❌'} ({permission_level})")
        
        # Test 5: Vérifier les actions autorisées
        print("\n⚡ Test 5: Vérification des actions autorisées")
        
        for user in test_users:
            print(f"\n   {user['username']} ({user['role']}):")
            for view in test_views:
                can_view = permission_manager.can_perform_action(user['id'], view, "view")
                can_edit = permission_manager.can_perform_action(user['id'], view, "edit")
                can_delete = permission_manager.can_perform_action(user['id'], view, "delete")
                can_admin = permission_manager.can_perform_action(user['id'], view, "admin")
                
                print(f"     {view}:")
                print(f"       Voir: {'✅' if can_view else '❌'}")
                print(f"       Éditer: {'✅' if can_edit else '❌'}")
                print(f"       Supprimer: {'✅' if can_delete else '❌'}")
                print(f"       Admin: {'✅' if can_admin else '❌'}")
        
        print("\n✅ Tests terminés avec succès!")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

def test_role_creation():
    """Test de création de rôles personnalisés"""
    print("\n🔧 Test de Création de Rôles Personnalisés")
    print("=" * 50)
    
    try:
        from models.role import RoleManager
        
        db_path = "database/edumanager.db"
        role_manager = RoleManager(db_path)
        
        # Créer un rôle personnalisé
        custom_role_name = "Assistant Pédagogique"
        custom_role_description = "Assistant pour les tâches pédagogiques"
        custom_permissions = ["read", "write"]
        
        if not role_manager.role_exists(custom_role_name):
            success = role_manager.create_role(custom_role_name, custom_role_description, custom_permissions)
            if success:
                print(f"✅ Rôle '{custom_role_name}' créé avec succès")
            else:
                print(f"❌ Échec de création du rôle '{custom_role_name}'")
        else:
            print(f"ℹ️ Le rôle '{custom_role_name}' existe déjà")
        
        # Vérifier le rôle créé
        role = role_manager.get_role_by_name(custom_role_name)
        if role:
            print(f"   Rôle trouvé: {role.nom}")
            print(f"   Description: {role.description}")
            print(f"   Permissions: {', '.join(role.permissions)}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test de création de rôles: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du système de permissions...")
    
    # Test principal
    test_permissions_system()
    
    # Test de création de rôles
    test_role_creation()
    
    print("\n🎉 Tous les tests sont terminés!")

