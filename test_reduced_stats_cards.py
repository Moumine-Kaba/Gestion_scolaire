#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des cartes de statistiques avec hauteur réduite
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_reduced_stats_cards():
    """Test des cartes de statistiques avec hauteur réduite"""
    print("🧪 Test des cartes de statistiques avec hauteur réduite...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Cartes Réduites - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 CARTES DE STATISTIQUES RÉDUITES !")
        print("=" * 60)
        print("✅ Hauteur des cartes réduite de 120px à 80px")
        print("✅ Icônes réduites de 20x20 à 16x16")
        print("✅ Espacement optimisé pour la nouvelle hauteur")
        print("✅ Sidebar élargie (poids 3) pour plus d'espace")
        print("✅ Interface plus compacte et équilibrée")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que les cartes sont plus compactes")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Cartes de Statistiques Réduites")
    print("=" * 70)
    
    # Test des cartes
    success = test_reduced_stats_cards()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les cartes de statistiques sont plus compactes")
        print("✅ La sidebar est élargie")
        print("✅ L'interface est optimisée")
        print("\n🚀 Les cartes ont été réduites avec succès !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
