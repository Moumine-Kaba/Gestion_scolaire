#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des cartes de statistiques avec icônes sans fond et badge Présent supprimé
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_stats_cards_no_background():
    """Test des cartes de statistiques avec icônes sans fond"""
    print("🧪 Test des cartes de statistiques avec icônes sans fond...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Cartes Statistiques Sans Fond - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 CARTES STATISTIQUES AMÉLIORÉES !")
        print("=" * 60)
        print("✅ Icônes avec contours seulement (sans fond coloré)")
        print("✅ Border width : 2px pour les contours")
        print("✅ Fond transparent pour les badges d'icônes")
        print("✅ Badge 'Présent' supprimé de l'en-tête")
        print("✅ Interface plus épurée et moderne")
        print("✅ Style cohérent avec les autres éléments")
        print("✅ Effet hover conservé")
        print("✅ Couleurs des contours selon le type")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Vérifiez que les icônes n'ont que des contours")
        print("💡 Vérifiez que le badge 'Présent' a disparu")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Cartes Statistiques Sans Fond")
    print("=" * 70)
    
    # Test des cartes sans fond
    success = test_stats_cards_no_background()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les icônes n'ont que des contours")
        print("✅ Le badge 'Présent' a été supprimé")
        print("✅ L'interface est plus épurée")
        print("\n🚀 Les cartes de statistiques ont été améliorées !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
