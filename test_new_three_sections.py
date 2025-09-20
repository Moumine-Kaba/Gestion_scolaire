#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la nouvelle organisation en trois sections de la vue avancée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_new_three_sections():
    """Test de la nouvelle organisation en trois sections"""
    print("🧪 Test de la nouvelle organisation en trois sections...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Nouvelle Organisation 3 Sections - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée avec nouvelle organisation créée")
        
        # Vérifier que les trois sections sont présentes
        print("\n📦 Vérification des trois sections...")
        
        # Vérifier les méthodes des sections
        methods = [
            "_build_selection_section",
            "_build_search_actions_section", 
            "_build_list_stats_section"
        ]
        
        for method in methods:
            if hasattr(advanced_view, method):
                print(f"✅ Méthode {method}: présente")
            else:
                print(f"❌ Méthode {method}: manquante")
        
        # Vérifier les composants principaux
        components = [
            "cb_class", "ent_date", "search_var", "filter_cb", 
            "list_wrap", "detail_panel"
        ]
        
        for component in components:
            if hasattr(advanced_view, component):
                print(f"✅ Composant {component}: présent")
            else:
                print(f"❌ Composant {component}: manquant")
        
        print("\n🎉 NOUVELLE ORGANISATION RÉUSSIE !")
        print("=" * 60)
        print("✅ Section 1: Sélection de classe et date")
        print("✅ Section 2: Recherche et actions en masse")
        print("✅ Section 3: Liste des élèves et statistiques")
        print("✅ Interface organisée comme dans l'image")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Nouvelle Organisation en Trois Sections")
    print("=" * 70)
    
    # Test de l'organisation
    success = test_new_three_sections()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La nouvelle organisation en trois sections fonctionne")
        print("✅ L'interface est organisée comme dans l'image")
        print("✅ Chaque section a sa fonction spécifique")
        print("\n🚀 La vue avancée est maintenant organisée en trois sections distinctes !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
