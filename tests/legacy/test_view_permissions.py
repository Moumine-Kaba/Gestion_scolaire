#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du Système de Permissions des Vues
EduManager+ - Gestion Scolaire
"""

import sys
import os

# Ajouter le répertoire parent au path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_view_permissions():
    """Test du système de permissions des vues"""
    print("🧪 Test du système de permissions des vues")
    print("=" * 50)
    
    try:
        # Test 1: Import des modules
        print("\n1️⃣ Test d'import des modules...")
        from models.view_permissions import ViewPermissions
        from models.view_access_manager import ViewAccessManager
        print("✅ Import réussi")
        
        # Test 2: Vérification des rôles disponibles
        print("\n2️⃣ Test des rôles disponibles...")
        roles = ViewPermissions.get_all_roles()
        print(f"Rôles disponibles: {', '.join(roles)}")
        
        # Test 3: Test des permissions par rôle
        print("\n3️⃣ Test des permissions par rôle...")
        test_roles = ["Directeur", "Professeur", "Élève"]
        
        for role in test_roles:
            print(f"\n--- Rôle: {role} ---")
            views = ViewPermissions.get_views_for_role(role)
            print(f"Vues accessibles: {len(views)}")
            print(f"Exemples: {', '.join(views[:5])}")
            
            # Test d'accès à des vues spécifiques
            test_views = ["dashboard", "eleves", "utilisateurs", "settings"]
            for view in test_views:
                can_access = ViewPermissions.can_access_view(role, view)
                status = "✅" if can_access else "❌"
                print(f"  {status} {view}: {can_access}")
        
        # Test 4: Test des sections de navigation
        print("\n4️⃣ Test des sections de navigation...")
        for role in test_roles:
            print(f"\n--- Sections pour {role} ---")
            sections = ViewPermissions.get_sections_for_role(role)
            for section_name, views in sections.items():
                print(f"  {section_name}: {len(views)} vues")
        
        # Test 5: Test du gestionnaire d'accès
        print("\n5️⃣ Test du gestionnaire d'accès...")
        db_path = "database/edumanager.db"
        if os.path.exists(db_path):
            view_manager = ViewAccessManager(db_path)
            print("✅ Gestionnaire d'accès initialisé")
            
            # Test avec un utilisateur fictif
            test_user_id = 1
            role = view_manager.get_user_role(test_user_id)
            print(f"Rôle de l'utilisateur {test_user_id}: {role}")
            
            if role:
                accessible_views = view_manager.get_accessible_views(test_user_id)
                print(f"Vues accessibles: {len(accessible_views)}")
                print(f"Exemples: {', '.join(accessible_views[:5])}")
                
                nav_sections = view_manager.get_navigation_sections(test_user_id)
                print(f"Sections de navigation: {len(nav_sections)}")
                for section_name, views in nav_sections.items():
                    print(f"  {section_name}: {len(views)} vues")
            else:
                print("⚠️ Aucun rôle trouvé pour cet utilisateur")
        else:
            print("⚠️ Base de données non trouvée, test limité")
        
        print("\n🎉 Tests terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        import traceback
        traceback.print_exc()

def test_role_specific_access():
    """Test d'accès spécifique par rôle"""
    print("\n🔐 Test d'accès spécifique par rôle")
    print("=" * 50)
    
    try:
        from models.view_permissions import ViewPermissions
        
        # Test des restrictions par rôle
        test_cases = [
            ("Directeur", "utilisateurs", True),      # Directeur peut voir les utilisateurs
            ("Professeur", "utilisateurs", False),    # Professeur ne peut pas voir les utilisateurs
            ("Élève", "notes", True),                # Élève peut voir ses notes
            ("Élève", "eleves", False),              # Élève ne peut pas gérer les élèves
            ("Professeur", "notes", True),           # Professeur peut gérer les notes
            ("Professeur", "paiements", False),      # Professeur ne peut pas gérer les paiements
        ]
        
        for role, view, expected in test_cases:
            actual = ViewPermissions.can_access_view(role, view)
            status = "✅" if actual == expected else "❌"
            print(f"{status} {role} -> {view}: attendu={expected}, obtenu={actual}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test d'accès: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du système de permissions")
    print("=" * 60)
    
    test_view_permissions()
    test_role_specific_access()
    
    print("\n" + "=" * 60)
    print("🏁 Tests terminés")

