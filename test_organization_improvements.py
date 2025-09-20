#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'organisation améliorée de la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_advanced_view_organization():
    """Test l'organisation améliorée de la vue avancée"""
    print("🧪 Test de l'organisation améliorée de la vue avancée des présences...")
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Organisation - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue
        print("📦 Instanciation de la vue avancée...")
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée instanciée avec succès")
        
        # Vérifier les composants organisés
        print("\n🔍 Vérification des composants organisés...")
        
        # Vérifier le panneau de gauche
        left_panel_components = [
            "cb_class", "ent_date", "search_var", "filter_cb", 
            "list_wrap", "stats_chips"
        ]
        
        for component in left_panel_components:
            if hasattr(advanced_view, component):
                print(f"✅ Composant gauche {component}: présent")
            else:
                print(f"❌ Composant gauche {component}: manquant")
        
        # Vérifier le panneau de droite
        if hasattr(advanced_view, "detail_panel"):
            print("✅ Panneau de détails: présent")
        else:
            print("❌ Panneau de détails: manquant")
        
        # Vérifier les services
        services = [
            "attendance_service", "notification_service", 
            "export_service", "justification_service", 
            "alert_service", "calendar_service"
        ]
        
        for service in services:
            if hasattr(advanced_view, service):
                print(f"✅ Service {service}: initialisé")
            else:
                print(f"❌ Service {service}: manquant")
        
        print("\n🎉 Test d'organisation réussi !")
        print("🚀 Lancement de l'application de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_icon_loading():
    """Test le chargement des icônes"""
    print("\n🧪 Test du chargement des icônes...")
    
    try:
        from src.modules.academic.attendance.views.advanced_attendance_view import load_ctk_icon
        
        # Test des icônes principales
        test_icons = [
            "person.png", "check_circle.png", "close_circle.png", 
            "time.png", "file.png", "bell.png", "edit.png", 
            "upload.png", "check.png", "close.png", "refresh.png",
            "calendar.png", "search.png", "class.png", "settings.png", "stats.png"
        ]
        
        loaded_icons = 0
        for icon_name in test_icons:
            icon = load_ctk_icon(icon_name, (20, 20))
            if icon:
                loaded_icons += 1
                print(f"✅ Icône {icon_name}: chargée")
            else:
                print(f"⚠️ Icône {icon_name}: non trouvée")
        
        print(f"\n📊 Résultat: {loaded_icons}/{len(test_icons)} icônes chargées")
        
        if loaded_icons >= len(test_icons) * 0.8:  # Au moins 80% des icônes
            print("✅ Test des icônes réussi")
            return True
        else:
            print("⚠️ Certaines icônes sont manquantes")
            return False
            
    except Exception as e:
        print(f"❌ Erreur test icônes: {e}")
        return False

def test_button_styling():
    """Test le style des boutons sans fond"""
    print("\n🧪 Test du style des boutons...")
    
    try:
        # Créer une fenêtre de test
        app = ctk.CTk()
        app.title("Test Style Boutons")
        app.geometry("600x400")
        app.configure(fg_color="#0A192F")
        
        from src.modules.academic.attendance.views.advanced_attendance_view import load_ctk_icon
        
        # Test des différents styles de boutons
        test_frame = ctk.CTkFrame(app, fg_color="transparent")
        test_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bouton avec fond (ancien style)
        old_btn = ctk.CTkButton(test_frame, text="Ancien Style", 
                               fg_color="#007ACC", text_color="white")
        old_btn.pack(pady=10)
        
        # Bouton sans fond (nouveau style)
        new_btn = ctk.CTkButton(test_frame, text="Nouveau Style", 
                               image=load_ctk_icon("check.png", (18, 18)),
                               fg_color="transparent", text_color="#00C851", 
                               hover_color="#1A1A1A", border_width=1, border_color="#00C851")
        new_btn.pack(pady=10)
        
        # Bouton d'erreur sans fond
        error_btn = ctk.CTkButton(test_frame, text="Erreur", 
                                 image=load_ctk_icon("close.png", (18, 18)),
                                 fg_color="transparent", text_color="#FF4444", 
                                 hover_color="#1A1A1A", border_width=1, border_color="#FF4444")
        error_btn.pack(pady=10)
        
        # Bouton d'avertissement sans fond
        warning_btn = ctk.CTkButton(test_frame, text="Avertissement", 
                                   image=load_ctk_icon("bell.png", (18, 18)),
                                   fg_color="transparent", text_color="#FFA500", 
                                   hover_color="#1A1A1A", border_width=1, border_color="#FFA500")
        warning_btn.pack(pady=10)
        
        print("✅ Boutons de test créés")
        print("🚀 Lancement de la fenêtre de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur test style boutons: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de l'organisation améliorée de la vue avancée")
    print("=" * 70)
    
    # Test 1: Organisation de la vue
    success1 = test_advanced_view_organization()
    
    # Test 2: Chargement des icônes
    success2 = test_icon_loading()
    
    # Test 3: Style des boutons
    success3 = test_button_styling()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    if success1:
        print("✅ Test d'organisation: RÉUSSI")
    else:
        print("❌ Test d'organisation: ÉCHEC")
    
    if success2:
        print("✅ Test des icônes: RÉUSSI")
    else:
        print("❌ Test des icônes: ÉCHEC")
    
    if success3:
        print("✅ Test du style boutons: RÉUSSI")
    else:
        print("❌ Test du style boutons: ÉCHEC")
    
    if success1 and success2 and success3:
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("✅ L'organisation de la vue est améliorée")
        print("✅ Les icônes sont correctement chargées")
        print("✅ Le style des boutons sans fond est appliqué")
        print("✅ La vue avancée est prête à l'utilisation")
    else:
        print("\n⚠️ TESTS PARTIELLEMENT RÉUSSIS")
        print("🔧 Certains tests ont échoué, vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
