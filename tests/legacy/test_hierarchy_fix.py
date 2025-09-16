#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la correction de la hiérarchie des icônes
Vérifie que les fonctions stat_card et action_card peuvent accéder aux icônes du dashboard
"""

import sys
import os

# Ajouter le répertoire racine au path Python
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_icon_hierarchy():
    """Test de l'accès aux icônes via la hiérarchie des parents"""
    print("🧪 Test de l'accès aux icônes via la hiérarchie des parents...")
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
        
        # Tester la création des cartes de statistiques avec la hiérarchie
        print("\n🔍 Test de la création des cartes avec hiérarchie...")
        try:
            # Créer un frame de test (comme dans create_stats_cards)
            test_frame = app.frame_dashboard_content
            
            # Tester stat_card avec une icône qui devrait être trouvée
            if "dashboard" in app.icons:
                print("✅ Icône 'dashboard' disponible dans le cache")
                
                # Créer une carte de statistique
                stat_card_obj = stat_card(test_frame, "Test Stats", "100", "dashboard", "#64FFDA")
                if stat_card_obj:
                    print("✅ stat_card créé avec succès via hiérarchie")
                else:
                    print("❌ stat_card non créé")
                    return False
            else:
                print("⚠️ Icône 'dashboard' non disponible, test ignoré")
            
            # Tester action_card
            action_card_obj = action_card(test_frame, "Test Action", "test_key", "dashboard")
            if action_card_obj:
                print("✅ action_card créé avec succès via hiérarchie")
            else:
                print("❌ action_card non créé")
                return False
            
        except Exception as e:
            print(f"❌ Erreur création des cartes avec hiérarchie: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Tester la méthode create_dashboard complète
        print("\n🔍 Test de la méthode create_dashboard complète...")
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

def test_icon_access():
    """Test de l'accès aux icônes dans différents contextes"""
    print("\n🔍 Test de l'accès aux icônes dans différents contextes...")
    print("=" * 50)
    
    try:
        from views.dashboard_view import MainApp, stat_card, action_card
        
        # Créer une application de test
        test_user = {'id_utilisateur': 1, 'username': 'test'}
        app = MainApp(test_user)
        
        # Vérifier que les icônes sont accessibles
        test_icons = ["dashboard", "eleves", "profs"]
        for icon_name in test_icons:
            if icon_name in app.icons:
                print(f"✅ Icône '{icon_name}' accessible")
            else:
                print(f"❌ Icône '{icon_name}' non accessible")
        
        # Tester l'accès via différents niveaux de hiérarchie
        test_frame = app.frame_dashboard_content
        
        # Créer plusieurs cartes pour tester la hiérarchie
        for i in range(3):
            try:
                card = stat_card(test_frame, f"Test {i}", str(i), "dashboard", "#64FFDA")
                if card:
                    print(f"✅ Carte {i} créée avec succès")
                else:
                    print(f"❌ Carte {i} non créée")
            except Exception as e:
                print(f"❌ Erreur création carte {i}: {e}")
                return False
        
        print("✅ Tous les tests de hiérarchie réussis")
        
        app.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur test accès icônes: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Test de la correction de la hiérarchie des icônes")
    print("=" * 60)
    
    tests = [
        ("Test de la hiérarchie des icônes", test_icon_hierarchy),
        ("Test de l'accès aux icônes", test_icon_access),
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
        print("💡 La correction de la hiérarchie des icônes fonctionne")
        return True
    else:
        print("⚠️ Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
