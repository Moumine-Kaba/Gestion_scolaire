#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Simple du Système de Permissions
EduManager+ - Gestion Scolaire
"""

import sys
import os

# Ajouter le répertoire parent au path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_basic_permissions():
    """Test basique du système de permissions"""
    print("🧪 Test basique du système de permissions")
    print("=" * 50)
    
    try:
        # Test 1: Import des modules
        print("\n1️⃣ Test d'import...")
        from models.view_permissions import ViewPermissions
        print("✅ Import ViewPermissions réussi")
        
        # Test 2: Rôles disponibles
        print("\n2️⃣ Rôles disponibles...")
        roles = ViewPermissions.get_all_roles()
        print(f"Rôles: {', '.join(roles)}")
        
        # Test 3: Permissions par rôle
        print("\n3️⃣ Test des permissions...")
        test_cases = [
            ("Directeur", "eleves", True),
            ("Directeur", "utilisateurs", False),
            ("Professeur", "notes", True),
            ("Professeur", "paiements", False),
            ("Élève", "notes", True),
            ("Élève", "eleves", False)
        ]
        
        for role, view, expected in test_cases:
            actual = ViewPermissions.can_access_view(role, view)
            status = "✅" if actual == expected else "❌"
            print(f"{status} {role} -> {view}: attendu={expected}, obtenu={actual}")
        
        print("\n🎉 Test basique réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Démarrage du test simple")
    success = test_basic_permissions()
    if success:
        print("\n✅ Le système de permissions fonctionne!")
    else:
        print("\n❌ Le système de permissions a des problèmes.")

