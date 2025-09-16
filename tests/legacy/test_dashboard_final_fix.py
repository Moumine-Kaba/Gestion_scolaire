#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test final de correction des erreurs d'images dans le dashboard
Vérifie que toutes les erreurs 'pyimage3 doesn't exist' sont corrigées
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_dashboard_creation():
    """Test de la création complète du dashboard sans erreur d'image"""
    print("🧪 Test de la création complète du dashboard...")
    print("=" * 50)
    
    try:
        # Importer le dashboard
        from views.dashboard_view import MainApp, stat_card, action_card
        
        print("✅ Import du dashboard réussi")
        
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
        
        # Vérifier que les icônes sont chargées
        if hasattr(app, 'icons') and len(app.icons) > 0:
            print(f"✅ {len(app.icons)} icônes chargées")
        else:
            print("❌ Aucune icône chargée")
            return False
        
        # Vérifier que les références d'images sont stockées
        if hasattr(app, '_img_refs') and len(app._img_refs) > 0:
            print(f"✅ {len(app._img_refs)} références d'images stockées")
        else:
            print("❌ Aucune référence d'image stockée")
            return False
        
        # Tester la création des cartes de statistiques
        print("\n🔍 Test de la création des cartes de statistiques...")
        try:
            # Créer un frame de test
            test_frame = app.frame_dashboard_content
            
            # Tester stat_card
            stat_card_obj = stat_card(test_frame, "Test", "100", "dashboard", "#64FFDA")
            if stat_card_obj:
                print("✅ stat_card créé avec succès")
            else:
                print("❌ stat_card non créé")
                return False
            
            # Tester action_card
            action_card_obj = action_card(test_frame, "Test Action", "test_key", "dashboard")
            if action_card_obj:
                print("✅ action_card créé avec succès")
            else:
                print("❌ action_card non créé")
                return False
            
        except Exception as e:
            print(f"❌ Erreur création des cartes: {e}")
            return False
        
        # Tester la méthode create_dashboard
        print("\n🔍 Test de la méthode create_dashboard...")
        try:
            # Sauvegarder l'état actuel
            original_children = len(app.frame_dashboard_content.winfo_children())
            
            # Appeler create_dashboard
            app.create_dashboard()
            
            # Vérifier que des éléments ont été ajoutés
            new_children = len(app.frame_dashboard_content.winfo_children())
            if new_children > original_children:
                print("✅ create_dashboard exécuté avec succès")
            else:
                print("⚠️ create_dashboard n'a pas ajouté d'éléments")
            
        except Exception as e:
            print(f"❌ Erreur dans create_dashboard: {e}")
            import traceback
            traceback.print_exc()
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

def test_icon_reuse():
    """Test de la réutilisation des icônes déjà chargées"""
    print("\n🔄 Test de la réutilisation des icônes...")
    print("=" * 50)
    
    try:
        from views.dashboard_view import MainApp, stat_card, action_card
        
        # Créer une application de test
        test_user = {'id_utilisateur': 1, 'username': 'test'}
        app = MainApp(test_user)
        
        # Vérifier que les icônes sont dans le cache
        if "dashboard" in app.icons:
            print("✅ Icône 'dashboard' dans le cache")
        else:
            print("❌ Icône 'dashboard' manquante du cache")
            return False
        
        # Tester la réutilisation
        test_frame = app.frame_dashboard_content
        
        # Créer plusieurs cartes avec la même icône
        for i in range(3):
            card = stat_card(test_frame, f"Test {i}", str(i), "dashboard", "#64FFDA")
            if not card:
                print(f"❌ Carte {i} non créée")
                return False
        
        print("✅ Réutilisation des icônes fonctionne")
        
        app.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur test réutilisation: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test final de correction des erreurs d'images dans le dashboard")
    print("=" * 60)
    
    tests = [
        ("Test de création complète du dashboard", test_dashboard_creation),
        ("Test de réutilisation des icônes", test_icon_reuse),
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
        print("💡 L'erreur 'pyimage3 doesn't exist' devrait être complètement corrigée")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
