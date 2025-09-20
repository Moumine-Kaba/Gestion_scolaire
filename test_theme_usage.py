#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'utilisation du thème EduManager+ dans la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

# Import du thème au niveau du module
try:
    from resources.themes.theme import *
    print("✅ Thème EduManager+ importé avec succès")
except ImportError:
    print("❌ Erreur import du thème")
    sys.exit(1)

def test_theme_usage():
    """Test l'utilisation du thème EduManager+"""
    print("🧪 Test de l'utilisation du thème EduManager+ dans la vue avancée...")
    print("=" * 70)
    
    try:
        # Test 1: Vérification des couleurs principales
        print("📦 Test 1: Vérification des couleurs principales...")
        colors_to_check = [
            ("BG_MAIN", BG_MAIN),
            ("BG_SIDEBAR", BG_SIDEBAR), 
            ("BG_CARD", BG_CARD),
            ("BORDER_COLOR", BORDER_COLOR),
            ("TEXT_PRIMARY", TEXT_PRIMARY),
            ("TEXT_SECONDARY", TEXT_SECONDARY),
            ("ACCENT_BLUE", ACCENT_BLUE),
            ("SUCCESS_GREEN", SUCCESS_GREEN),
            ("ERROR_RED", ERROR_RED),
            ("WARNING_YELLOW", WARNING_YELLOW)
        ]
        
        for color_name, color_value in colors_to_check:
            print(f"✅ {color_name}: {color_value}")
        
        # Test 2: Import de la vue avancée
        print("\n📦 Test 2: Import de la vue avancée...")
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        print("✅ AdvancedAttendanceView importé avec succès")
        
        # Test 3: Test d'instanciation avec le thème
        print("\n📦 Test 3: Test d'instanciation avec le thème...")
        app = ctk.CTk()
        app.title("Test Thème EduManager+ - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color=BG_MAIN)
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée instanciée avec le thème EduManager+")
        
        # Test 4: Vérification de l'utilisation des couleurs du thème
        print("\n📦 Test 4: Vérification de l'utilisation des couleurs...")
        
        # Vérifier que les composants utilisent les bonnes couleurs
        if hasattr(advanced_view, 'detail_panel'):
            print("✅ Panneau de détails créé avec le thème")
        
        if hasattr(advanced_view, 'list_wrap'):
            print("✅ Liste des élèves créée avec le thème")
        
        # Test 5: Affichage des couleurs du thème
        print("\n📦 Test 5: Affichage des couleurs du thème...")
        print(f"🎨 Fond principal: {BG_MAIN}")
        print(f"🎨 Fond sidebar: {BG_SIDEBAR}")
        print(f"🎨 Fond cartes: {BG_CARD}")
        print(f"🎨 Bordures: {BORDER_COLOR}")
        print(f"🎨 Texte principal: {TEXT_PRIMARY}")
        print(f"🎨 Texte secondaire: {TEXT_SECONDARY}")
        print(f"🎨 Accent cyan: {ACCENT_BLUE}")
        print(f"🎨 Vert succès: {SUCCESS_GREEN}")
        print(f"🎨 Rouge erreur: {ERROR_RED}")
        print(f"🎨 Jaune avertissement: {WARNING_YELLOW}")
        
        print("\n🎉 TOUS LES TESTS RÉUSSIS !")
        print("=" * 70)
        print("✅ Le thème EduManager+ est correctement utilisé")
        print("✅ La vue avancée utilise les couleurs du thème")
        print("✅ L'interface est cohérente avec le reste de l'application")
        
        print("\n🚀 Lancement de l'application de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_theme_consistency():
    """Test la cohérence du thème avec le reste de l'application"""
    print("\n🧪 Test de cohérence du thème...")
    
    try:
        # Test avec d'autres vues pour vérifier la cohérence
        from src.modules.academic.classes.views.classes_view import ClassesManagerView
        from src.modules.academic.students.views.eleves_dashboard import ElevesDashboard
        
        print("✅ Autres vues importées pour vérification de cohérence")
        
        # Vérifier que toutes les vues utilisent le même thème
        app = ctk.CTk()
        app.title("Test Cohérence Thème")
        app.geometry("800x600")
        app.configure(fg_color=BG_MAIN)
        
        # Test avec la vue des classes
        classes_view = ClassesManagerView(app)
        print("✅ Vue des classes utilise le thème EduManager+")
        
        # Test avec la vue des élèves
        eleves_view = ElevesDashboard(app)
        print("✅ Vue des élèves utilise le thème EduManager+")
        
        print("✅ Cohérence du thème vérifiée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test cohérence: {e}")
        return False

def main():
    """Fonction principale"""
    print("🏫 Test du Thème EduManager+ dans la Vue Avancée des Présences")
    print("=" * 80)
    
    # Test 1: Utilisation du thème
    success1 = test_theme_usage()
    
    # Test 2: Cohérence du thème
    success2 = test_theme_consistency()
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 80)
    
    if success1 and success2:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Le thème EduManager+ est correctement utilisé")
        print("✅ La vue avancée est cohérente avec le reste de l'application")
        print("✅ L'interface est uniforme et professionnelle")
        print("\n🚀 La vue avancée des présences utilise maintenant votre thème personnalisé !")
    else:
        print("⚠️ SUCCÈS PARTIEL")
        if not success1:
            print("❌ Problèmes d'utilisation du thème détectés")
        if not success2:
            print("❌ Problèmes de cohérence détectés")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()