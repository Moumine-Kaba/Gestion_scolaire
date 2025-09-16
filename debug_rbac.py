#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de debug pour le système RBAC
Vérifie pourquoi le comptable voit toutes les vues
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

def debug_rbac_system():
    """Debug du système RBAC"""
    print("🔍 DEBUG DU SYSTÈME RBAC")
    print("=" * 50)
    
    try:
        from src.modules.auth.models.rbac_system import RBACSystem
        from src.modules.auth.models.rbac_view_manager import RBACViewManager
        
        db_path = project_root / "database" / "edumanager.db"
        print(f"📁 Base de données: {db_path}")
        
        # 1. Vérifier la base de données
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        
        # Vérifier les tables RBAC
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'rbac_%'")
        rbac_tables = cursor.fetchall()
        print(f"📋 Tables RBAC: {[t[0] for t in rbac_tables]}")
        
        # Vérifier les rôles
        cursor.execute("SELECT * FROM rbac_roles")
        roles = cursor.fetchall()
        print(f"👥 Rôles disponibles: {len(roles)}")
        for role in roles:
            print(f"  - {role[1]} (ID: {role[0]})")
        
        # Vérifier les utilisateurs
        cursor.execute("SELECT id_utilisateur, nom_utilisateur, nom, prenom FROM utilisateurs")
        users = cursor.fetchall()
        print(f"👤 Utilisateurs: {len(users)}")
        for user in users:
            print(f"  - {user[1]} ({user[2]} {user[3]}) - ID: {user[0]}")
        
        # Vérifier les attributions de rôles
        cursor.execute("SELECT user_id, role_id FROM rbac_user_roles")
        assignments = cursor.fetchall()
        print(f"🔗 Attributions de rôles: {len(assignments)}")
        for assignment in assignments:
            print(f"  - Utilisateur {assignment[0]} → Rôle {assignment[1]}")
        
        conn.close()
        
        # 2. Tester le système RBAC
        print("\n🧪 TEST DU SYSTÈME RBAC")
        rbac = RBACSystem(str(db_path), dev_mode=False)
        
        # Tester avec le comptable (ID 2)
        comptable_id = 2
        print(f"\n👤 Test avec le comptable (ID: {comptable_id})")
        
        user_role = rbac.get_user_role(comptable_id)
        print(f"Rôle récupéré: {user_role.name if user_role else 'Aucun'}")
        
        # Tester les permissions pour quelques vues
        test_views = ["dashboard", "eleves", "paiements", "utilisateurs", "presences"]
        for view in test_views:
            can_access = rbac.can_access_view(comptable_id, view)
            permission = rbac.get_view_permission_level(comptable_id, view)
            print(f"  {view}: Accès={can_access}, Permission={permission.name}")
        
        # 3. Tester le RBACViewManager
        print("\n🎯 TEST DU RBACViewManager")
        view_manager = RBACViewManager(str(db_path), dev_mode=False)
        view_manager.set_current_user(comptable_id)
        
        print(f"Utilisateur actuel: {view_manager.current_user_id}")
        print(f"Rôle actuel: {view_manager.current_user_role.name if view_manager.current_user_role else 'Aucun'}")
        
        # Tester la navigation filtrée
        filtered_nav = view_manager.get_filtered_navigation()
        print(f"\n📋 Navigation filtrée pour le comptable:")
        for section, views in filtered_nav.items():
            print(f"  {section}: {len(views)} vues")
            for view_title, view_name in views:
                print(f"    - {view_title} ({view_name})")
        
        # 4. Vérifier les permissions du rôle Comptable
        print(f"\n🔍 PERMISSIONS DU RÔLE COMPTABLE")
        if user_role:
            print(f"Permissions du rôle '{user_role.name}':")
            for view, permission in user_role.permissions.items():
                print(f"  {view}: {permission.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_rbac_system()
