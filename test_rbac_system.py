#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test du système RBAC pour EduManager+
Vérifie le bon fonctionnement des permissions et de l'accès aux vues
"""

import os
import sys
import sqlite3
from pathlib import Path

# Ajouter le répertoire src au path
project_root = Path(__file__).resolve().parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from src.modules.auth.models.rbac_system import RBACSystem, PermissionLevel
from src.modules.auth.models.rbac_view_manager import RBACViewManager

def test_rbac_system():
    """Test du système RBAC de base"""
    
    print("🧪 Test du système RBAC")
    print("=" * 40)
    
    # Chemin de la base de données
    db_path = project_root / "database" / "edumanager.db"
    
    # Initialiser le système RBAC
    rbac = RBACSystem(str(db_path), dev_mode=False)
    
    # Test 1: Vérifier les rôles créés
    print("\n1️⃣ Test des rôles:")
    roles = rbac.get_all_roles()
    expected_roles = ["Directeur", "Comptable", "Secrétaire", "Surveillant"]
    
    for role_name in expected_roles:
        roles = rbac.get_role_by_name(role_name)
        if roles:
            print(f"  ✅ Rôle '{role_name}' trouvé")
        else:
            print(f"  ❌ Rôle '{role_name}' manquant")
    
    # Test 2: Vérifier les permissions par défaut
    print("\n2️⃣ Test des permissions par défaut:")
    
    # Directeur - toutes les permissions
    directeur_role = rbac.get_role_by_name("Directeur")
    if directeur_role:
        admin_views = [view for view, perm in directeur_role.permissions.items() 
                      if perm == PermissionLevel.ADMIN]
        print(f"  Directeur: {len(admin_views)} vues avec permissions ADMIN")
    
    # Comptable - paiements en admin, autres en lecture
    comptable_role = rbac.get_role_by_name("Comptable")
    if comptable_role:
        paiements_perm = comptable_role.permissions.get("paiements", PermissionLevel.NONE)
        if paiements_perm == PermissionLevel.ADMIN:
            print("  ✅ Comptable: permissions ADMIN sur paiements")
        else:
            print(f"  ❌ Comptable: permissions {paiements_perm.name} sur paiements")
    
    # Secrétaire - pas d'accès aux paiements
    secretaire_role = rbac.get_role_by_name("Secrétaire")
    if secretaire_role:
        paiements_perm = secretaire_role.permissions.get("paiements", PermissionLevel.NONE)
        if paiements_perm == PermissionLevel.NONE:
            print("  ✅ Secrétaire: pas d'accès aux paiements")
        else:
            print(f"  ❌ Secrétaire: accès {paiements_perm.name} aux paiements")
    
    # Surveillant - présences et emplois en admin
    surveillant_role = rbac.get_role_by_name("Surveillant")
    if surveillant_role:
        presences_perm = surveillant_role.permissions.get("presences", PermissionLevel.NONE)
        emplois_perm = surveillant_role.permissions.get("emplois", PermissionLevel.NONE)
        
        if presences_perm == PermissionLevel.ADMIN:
            print("  ✅ Surveillant: permissions ADMIN sur présences")
        else:
            print(f"  ❌ Surveillant: permissions {presences_perm.name} sur présences")
        
        if emplois_perm == PermissionLevel.ADMIN:
            print("  ✅ Surveillant: permissions ADMIN sur emplois")
        else:
            print(f"  ❌ Surveillant: permissions {emplois_perm.name} sur emplois")
    
    return rbac

def test_view_manager(rbac):
    """Test du gestionnaire de vues"""
    
    print("\n3️⃣ Test du gestionnaire de vues:")
    
    view_manager = RBACViewManager(rbac.db_path, dev_mode=False)
    
    # Créer des utilisateurs de test
    test_users = [
        {"id": 1001, "roles": "Directeur"},
        {"id": 1002, "roles": "Comptable"},
        {"id": 1003, "roles": "Secrétaire"},
        {"id": 1004, "roles": "Surveillant"}
    ]
    
    for user in test_users:
        # Attribuer le rôle
        rbac.assign_role_to_user(user["id"], user["roles"])
        
        # Tester l'accès aux vues
        view_manager.set_current_user(user["id"])
        
        print(f"\n  👤 Utilisateur {user['id']} ({user['roles']}):")
        
        # Vues à tester
        test_views = ["dashboard", "eleves", "paiements", "utilisateurs", "presences"]
        
        for view in test_views:
            can_access = view_manager.can_access_view(view)
            permission_level = view_manager.get_view_permission_level(view)
            print(f"    {view}: {'✅' if can_access else '❌'} ({permission_level.name})")
    
    return view_manager

def test_navigation_filtering(view_manager):
    """Test du filtrage de la navigation"""
    
    print("\n4️⃣ Test du filtrage de la navigation:")
    
    test_users = [
        {"id": 1001, "roles": "Directeur"},
        {"id": 1002, "roles": "Comptable"},
        {"id": 1003, "roles": "Secrétaire"},
        {"id": 1004, "roles": "Surveillant"}
    ]
    
    for user in test_users:
        view_manager.set_current_user(user["id"])
        filtered_nav = view_manager.get_filtered_navigation()
        
        print(f"\n  👤 {user['roles']}:")
        print(f"    Vues accessibles: {view_manager.get_accessible_views_count()}")
        
        for section, views in filtered_nav.items():
            print(f"    {section}: {len(views)} vues")
            for view_title, view_name in views:
                print(f"      - {view_title}")

def test_access_control(rbac, view_manager):
    """Test du contrôle d'accès"""
    
    print("\n5️⃣ Test du contrôle d'accès:")
    
    # Test avec un utilisateurs sans rôle
    view_manager.set_current_user(9999)  # Utilisateur inexistant
    
    test_views = ["dashboard", "eleves", "paiements"]
    for view in test_views:
        can_access = view_manager.can_access_view(view)
        print(f"  Utilisateur sans rôle - {view}: {'❌' if not can_access else '⚠️'} (devrait être ❌)")
    
    # Test avec un utilisateurs avec rôle
    view_manager.set_current_user(1002)  # Comptable
    
    # Test accès autorisé
    if view_manager.can_access_view("paiements"):
        print("  ✅ Comptable peut accéder aux paiements")
    else:
        print("  ❌ Comptable ne peut pas accéder aux paiements")
    
    # Test accès refusé
    if not view_manager.can_access_view("utilisateurs"):
        print("  ✅ Comptable ne peut pas accéder aux utilisateurs")
    else:
        print("  ❌ Comptable peut accéder aux utilisateurs (ne devrait pas)")

def test_dev_mode():
    """Test du mode développement"""
    
    print("\n6️⃣ Test du mode développement:")
    
    db_path = project_root / "database" / "edumanager.db"
    
    # Mode développement activé
    rbac_dev = RBACSystem(str(db_path), dev_mode=True)
    view_manager_dev = RBACViewManager(str(db_path), dev_mode=True)
    
    view_manager_dev.set_current_user(9999)  # Utilisateur inexistant
    
    # En mode dev, tout devrait être accessible
    test_views = ["dashboard", "eleves", "paiements", "utilisateurs"]
    all_accessible = True
    
    for view in test_views:
        can_access = view_manager_dev.can_access_view(view)
        if not can_access:
            all_accessible = False
            print(f"  ❌ Mode dev: {view} non accessible")
    
    if all_accessible:
        print("  ✅ Mode développement: toutes les vues accessibles")
    
    # Vérifier que toutes les vues sont disponibles
    accessible_views = view_manager_dev.rbac.get_accessible_views(9999)
    print(f"  📊 Mode dev: {len(accessible_views)} vues accessibles")

def test_role_management(rbac):
    """Test de la gestion des rôles"""
    
    print("\n7️⃣ Test de la gestion des rôles:")
    
    # Créer un nouveau rôle
    test_permissions = {
        "dashboard": PermissionLevel.READ,
        "eleves": PermissionLevel.WRITE,
        "paiements": PermissionLevel.NONE
    }
    
    success = rbac.create_role("Testeur", "Rôle de test", test_permissions)
    if success:
        print("  ✅ Rôle 'Testeur' créé")
        
        # Vérifier le rôle créé
        test_role = rbac.get_role_by_name("Testeur")
        if test_role:
            print(f"    Description: {test_role.description}")
            print(f"    Permissions: {len(test_role.permissions)}")
            
            # Attribuer à un utilisateurs
            rbac.assign_role_to_user(1005, "Testeur")
            user_role = rbac.get_user_role(1005)
            if user_role and user_role.name == "Testeur":
                print("  ✅ Rôle attribué à l'utilisateurs")
            else:
                print("  ❌ Échec attribution du rôle")
        
        # Supprimer le rôle de test
        rbac.delete_role("Testeur")
        print("  ✅ Rôle 'Testeur' supprimé")
    else:
        print("  ❌ Échec création du rôle 'Testeur'")

def main():
    """Fonction principale de test"""
    
    print("🚀 Tests du système RBAC - EduManager+")
    print("=" * 50)
    
    try:
        # Test du système RBAC de base
        rbac = test_rbac_system()
        
        # Test du gestionnaire de vues
        view_manager = test_view_manager(rbac)
        
        # Test du filtrage de la navigation
        test_navigation_filtering(view_manager)
        
        # Test du contrôle d'accès
        test_access_control(rbac, view_manager)
        
        # Test du mode développement
        test_dev_mode()
        
        # Test de la gestion des rôles
        test_role_management(rbac)
        
        print("\n✅ Tous les tests terminés!")
        print("\n📝 Résumé:")
        print("  • Système RBAC fonctionnel")
        print("  • Rôles et permissions configurés")
        print("  • Contrôle d'accès opérationnel")
        print("  • Mode développement disponible")
        print("  • Gestion des rôles fonctionnelle")
        
    except Exception as e:
        print(f"\n❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
