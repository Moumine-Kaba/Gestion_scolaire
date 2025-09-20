#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de correction de l'erreur d'instanciation de la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_view_instantiation():
    """Test l'instanciation de la vue avancée"""
    print("🧪 Test de l'instanciation de la vue avancée des présences...")
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Instanciation - Vue Avancée des Présences")
        app.geometry("1200x800")
        app.configure(fg_color="#0A192F")
        
        # Test 1: Instanciation avec app_instance
        print("📦 Test 1: Instanciation avec app_instance...")
        try:
            advanced_view1 = AdvancedAttendanceView(app, app)
            print("✅ Instanciation avec app_instance réussie")
        except Exception as e:
            print(f"❌ Erreur instanciation avec app_instance: {e}")
            return False
        
        # Test 2: Instanciation sans app_instance (comme le système de vues)
        print("📦 Test 2: Instanciation sans app_instance...")
        try:
            advanced_view2 = AdvancedAttendanceView(app)
            print("✅ Instanciation sans app_instance réussie")
        except Exception as e:
            print(f"❌ Erreur instanciation sans app_instance: {e}")
            return False
        
        # Test 3: Vérification des composants
        print("📦 Test 3: Vérification des composants...")
        
        # Vérifier que les services sont initialisés
        services = [
            "attendance_service",
            "notification_service", 
            "export_service",
            "justification_service",
            "alert_service",
            "calendar_service"
        ]
        
        for service in services:
            if hasattr(advanced_view2, service):
                print(f"✅ Service {service} initialisé")
            else:
                print(f"❌ Service {service} manquant")
                return False
        
        # Vérifier que les composants UI sont présents
        ui_components = [
            "cb_class",
            "ent_date", 
            "list_wrap",
            "detail_panel",
            "search_var",
            "filter_var"
        ]
        
        for component in ui_components:
            if hasattr(advanced_view2, component):
                print(f"✅ Composant UI {component} présent")
            else:
                print(f"❌ Composant UI {component} manquant")
                return False
        
        print("\n🎉 Tous les tests d'instanciation réussis !")
        
        # Afficher l'application
        print("\n🚀 Lancement de l'application de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        advanced_view2.pack(fill="both", expand=True, padx=20, pady=20)
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_integration():
    """Test l'intégration dans le dashboard"""
    print("\n🧪 Test de l'intégration dans le dashboard...")
    
    try:
        # Test d'import du dashboard
        from src.modules.auth.views.dashboard_view import PresenceView
        
        if PresenceView:
            print(f"✅ PresenceView définie: {PresenceView.__name__}")
            
            # Test d'instanciation comme le dashboard le ferait
            app = ctk.CTk()
            app.title("Test Dashboard Integration")
            app.geometry("800x600")
            
            try:
                # Instanciation comme le dashboard (sans app_instance)
                presence_view = PresenceView(app)
                print("✅ Instanciation depuis le dashboard réussie")
                return True
            except Exception as e:
                print(f"❌ Erreur instanciation depuis dashboard: {e}")
                return False
        else:
            print("❌ PresenceView non définie")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test dashboard: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de correction de l'erreur d'instanciation")
    print("=" * 60)
    
    # Test 1: Instanciation de la vue
    success1 = test_view_instantiation()
    
    # Test 2: Intégration dashboard
    success2 = test_dashboard_integration()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    if success1:
        print("✅ Test d'instanciation: RÉUSSI")
    else:
        print("❌ Test d'instanciation: ÉCHEC")
    
    if success2:
        print("✅ Test d'intégration dashboard: RÉUSSI")
    else:
        print("❌ Test d'intégration dashboard: ÉCHEC")
    
    if success1 and success2:
        print("\n🎉 CORRECTION RÉUSSIE !")
        print("✅ L'erreur d'instanciation est corrigée")
        print("✅ La vue avancée fonctionne avec le système de vues existant")
        print("✅ L'intégration dans le dashboard est opérationnelle")
    else:
        print("\n⚠️ CORRECTION PARTIELLE")
        print("🔧 Certains tests ont échoué, vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
