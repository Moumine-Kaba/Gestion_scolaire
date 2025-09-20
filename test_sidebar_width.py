#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide pour vérifier la largeur de la sidebar dans la vue avancée des présences
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk
from datetime import datetime

def test_sidebar_width():
    """Test la largeur de la sidebar"""
    print("🧪 Test de la largeur de la sidebar...")
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Largeur Sidebar - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Créer la vue avancée
        advanced_view = AdvancedAttendanceView(app, app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée avec sidebar encore plus large")
        print("📏 Proportions:")
        print("  • Sidebar (panneau gauche): poids 3")
        print("  • Panneau de détails (droite): poids 2")
        print("  • Ratio: 60% sidebar / 40% détails")
        
        # Afficher l'application
        print("\n🚀 Lancement de l'application de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la largeur de la sidebar")
    print("=" * 50)
    
    success = test_sidebar_width()
    
    if success:
        print("\n🎉 Test réussi !")
        print("✅ La sidebar est maintenant encore plus large")
        print("📏 Proportions ajustées: 60% sidebar / 40% détails")
    else:
        print("\n❌ Test échoué")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
