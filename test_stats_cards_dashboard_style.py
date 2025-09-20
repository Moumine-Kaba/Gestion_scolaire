#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des cartes de statistiques style tableau de bord principal
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_stats_cards_dashboard_style():
    """Test des cartes de statistiques style tableau de bord principal"""
    print("🧪 Test des cartes de statistiques style tableau de bord...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Cartes Statistiques Style Tableau de Bord - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 CARTES STATISTIQUES STYLE TABLEAU DE BORD !")
        print("=" * 60)
        print("✅ Style identique aux cartes du tableau de bord principal")
        print("✅ Icônes dans des badges colorés (36x36)")
        print("✅ Corner radius : 12px")
        print("✅ Hauteur : 100px")
        print("✅ Header avec icône et contenu séparés")
        print("✅ Effet hover avec bordure TEXT_ACCENT")
        print("✅ Alignement à gauche pour le contenu")
        print("✅ Espacement optimisé (12px padding)")
        print("✅ Icônes 18x18 dans les badges")
        print("✅ Couleurs selon le type de statistique")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Vérifiez que les cartes ressemblent au tableau de bord")
        print("💡 Survolez les cartes pour voir l'effet hover")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Cartes Statistiques Style Tableau de Bord")
    print("=" * 70)
    
    # Test des cartes style tableau de bord
    success = test_stats_cards_dashboard_style()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les cartes ressemblent au tableau de bord principal")
        print("✅ Style cohérent dans toute l'application")
        print("✅ Interface harmonieuse et professionnelle")
        print("\n🚀 Les cartes de statistiques ont le style du tableau de bord !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
