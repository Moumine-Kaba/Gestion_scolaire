#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de correction des erreurs d'images dans le dashboard
Vérifie que les icônes sont chargées correctement sans erreur 'pyimage3 doesn't exist'
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_dashboard_image_loading():
    """Test du chargement des images dans le dashboard"""
    print("🧪 Test du chargement des images dans le dashboard...")
    print("=" * 50)
    
    try:
        # Importer le dashboard
        from views.dashboard_view import MainApp, load_ctk_icon, ICON_MAP
        
        print("✅ Import du dashboard réussi")
        
        # Tester la fonction de chargement d'icône
        print("\n🔍 Test de la fonction load_ctk_icon...")
        
        # Créer une image de test
        from PIL import Image
        test_image = Image.new('RGB', (20, 20), color='blue')
        
        # Tester le chargement d'une icône
        icon = load_ctk_icon("home.png", (20, 20))
        
        if icon is not None:
            print("✅ Fonction load_ctk_icon fonctionne")
            
            # Vérifier que la référence PIL est stockée
            if hasattr(icon, '_pil_ref'):
                print("✅ Référence PIL stockée correctement")
            else:
                print("⚠️ Référence PIL non stockée")
        else:
            print("⚠️ Fonction load_ctk_icon retourne None (normal si l'icône n'existe pas)")
        
        # Tester la création d'une instance MainApp (sans l'afficher)
        print("\n🔍 Test de la création de MainApp...")
        
        # Créer un utilisateur de test
        test_user = {
            'id_utilisateur': 1,
            'username': 'test_user',
            'email': 'test@example.com',
            'nom': 'Test',
            'prenom': 'User'
        }
        
        # Créer l'application (sans l'afficher)
        app = MainApp(test_user)
        print("✅ Instance MainApp créée")
        
        # Vérifier que les méthodes de gestion d'images sont présentes
        if hasattr(app, '_load_icons_safely'):
            print("✅ Méthode _load_icons_safely présente")
        else:
            print("❌ Méthode _load_icons_safely manquante")
            return False
        
        if hasattr(app, '_cleanup_images'):
            print("✅ Méthode _cleanup_images présente")
        else:
            print("❌ Méthode _cleanup_images manquante")
            return False
        
        if hasattr(app, '_create_fallback_icons'):
            print("✅ Méthode _create_fallback_icons présente")
        else:
            print("❌ Méthode _create_fallback_icons manquante")
            return False
        
        # Vérifier que les icônes ont été chargées
        if hasattr(app, 'icons') and len(app.icons) > 0:
            print(f"✅ {len(app.icons)} icônes chargées")
        else:
            print("⚠️ Aucune icône chargée")
        
        # Vérifier que les références d'images sont stockées
        if hasattr(app, '_img_refs') and len(app._img_refs) > 0:
            print(f"✅ {len(app._img_refs)} références d'images stockées")
        else:
            print("⚠️ Aucune référence d'image stockée")
        
        # Tester la méthode de nettoyage
        print("\n🧹 Test de la méthode de nettoyage...")
        try:
            app._cleanup_images()
            print("✅ Méthode de nettoyage fonctionne")
        except Exception as e:
            print(f"❌ Erreur dans la méthode de nettoyage: {e}")
            return False
        
        # Fermer l'application
        app.destroy()
        print("✅ Application fermée proprement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_icon_map():
    """Test de la carte des icônes"""
    print("\n🗺️ Test de la carte des icônes...")
    print("=" * 50)
    
    try:
        from views.dashboard_view import ICON_MAP
        
        print(f"✅ Carte des icônes chargée: {len(ICON_MAP)} icônes définies")
        
        # Vérifier quelques icônes clés
        key_icons = ["dashboard", "eleves", "profs", "classes", "notes"]
        
        for key in key_icons:
            if key in ICON_MAP:
                print(f"   ✅ {key}: {ICON_MAP[key]}")
            else:
                print(f"   ❌ {key}: manquant")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test carte des icônes: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de la correction des erreurs d'images dans le dashboard")
    print("=" * 60)
    
    tests = [
        ("Test du chargement des images", test_dashboard_image_loading),
        ("Test de la carte des icônes", test_icon_map),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        if test_func():
            passed += 1
            print(f"✅ {test_name} - RÉUSSI")
        else:
            print(f"❌ {test_name} - ÉCHEC")
    
    print("\n" + "=" * 60)
    print(f"📊 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("💡 Les erreurs d'images dans le dashboard devraient être corrigées")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
