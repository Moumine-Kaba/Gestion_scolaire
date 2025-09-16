#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple du Système de Permissions
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test des imports"""
    print("🔍 Test des imports...")
    
    try:
        from models.permissions import PermissionManager
        print("✅ PermissionManager importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import PermissionManager: {e}")
        return False
    
    try:
        from models.role import RoleManager
        print("✅ RoleManager importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import RoleManager: {e}")
        return False
    
    return True

def test_initialization():
    """Test de l'initialisation"""
    print("\n🔧 Test de l'initialisation...")
    
    try:
        from models.permissions import PermissionManager
        from models.role import RoleManager
        
        db_path = "database/edumanager.db"
        
        # Initialiser les gestionnaires
        permission_manager = PermissionManager(db_path)
        print("✅ PermissionManager initialisé")
        
        role_manager = RoleManager(db_path)
        print("✅ RoleManager initialisé")
        
        return permission_manager, role_manager
        
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        return None, None

def test_roles(role_manager):
    """Test des rôles"""
    print("\n👥 Test des rôles...")
    
    if not role_manager:
        print("❌ RoleManager non disponible")
        return
    
    try:
        # Récupérer tous les rôles
        roles = role_manager.get_all_roles()
        print(f"✅ {len(roles)} rôles trouvés:")
        
        for role in roles:
            print(f"   - {role.nom}: {role.description}")
            print(f"     Permissions: {', '.join(role.permissions)}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des rôles: {e}")

def test_permissions(permission_manager):
    """Test des permissions"""
    print("\n🔑 Test des permissions...")
    
    if not permission_manager:
        print("❌ PermissionManager non disponible")
        return
    
    try:
        # Test avec un utilisateur fictif (ID 1)
        user_id = 1
        
        # Récupérer le rôle de l'utilisateur
        role_name = permission_manager.get_user_role_name(user_id)
        print(f"✅ Rôle de l'utilisateur {user_id}: {role_name}")
        
        # Récupérer les permissions de l'utilisateur
        permissions = permission_manager.get_user_view_permissions(user_id)
        print(f"✅ Permissions de l'utilisateur {user_id}:")
        
        for view_name, permission_level in permissions.items():
            print(f"   {view_name}: {permission_level}")
            
        # Vérifier l'accès à quelques vues
        test_views = ["dashboard", "eleves", "notes", "utilisateurs"]
        print(f"\n✅ Test d'accès aux vues:")
        
        for view in test_views:
            can_access = permission_manager.can_access_view(user_id, view)
            permission_level = permission_manager.get_view_permission_level(user_id, view)
            print(f"   {view}: {'✅' if can_access else '❌'} ({permission_level})")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des permissions: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test du Système de Permissions et Rôles")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Échec des imports, arrêt des tests")
        return
    
    # Test 2: Initialisation
    permission_manager, role_manager = test_initialization()
    
    # Test 3: Rôles
    test_roles(role_manager)
    
    # Test 4: Permissions
    test_permissions(permission_manager)
    
    print("\n🎉 Tests terminés!")

if __name__ == "__main__":
    main()

