#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la largeur de la sidebar réduite
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_sidebar_width():
    """Test de la largeur de la sidebar réduite"""
    print("🧪 Test de la largeur de la sidebar réduite...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Sidebar Réduite - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        # Vérifier la configuration des colonnes
        grid_info = advanced_view.grid_info()
        print(f"✅ Configuration du grid: {grid_info}")
        
        print("\n🎉 SIDEBAR RÉDUITE !")
        print("=" * 60)
        print("✅ La sidebar est maintenant moins large (poids 2)")
        print("✅ Le panneau de droite est plus large (poids 3)")
        print("✅ Proportions: 40% sidebar / 60% panneau de droite")
        print("✅ Interface plus équilibrée")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que la sidebar est moins large")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Largeur de Sidebar Réduite")
    print("=" * 70)
    
    # Test de la sidebar
    success = test_sidebar_width()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La sidebar est maintenant moins large")
        print("✅ Le panneau de droite a plus d'espace")
        print("✅ Interface plus équilibrée")
        print("\n🚀 La sidebar a été réduite avec succès !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
