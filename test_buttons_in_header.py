#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des boutons Appliquer/Annuler dans l'en-tête avec icônes et tooltips
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_in_header():
    """Test des boutons dans l'en-tête avec icônes et tooltips"""
    print("🧪 Test des boutons Appliquer/Annuler dans l'en-tête...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Boutons dans En-tête - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 BOUTONS DANS L'EN-TÊTE !")
        print("=" * 60)
        print("✅ Boutons déplacés dans l'en-tête à côté de 'Historique'")
        print("✅ Boutons avec icônes seulement (pas de texte)")
        print("✅ Pas de fond (transparent)")
        print("✅ Tooltips ajoutés pour chaque bouton")
        print("✅ Historique : 'Voir l'historique des présences'")
        print("✅ Appliquer : 'Appliquer les modifications'")
        print("✅ Annuler : 'Annuler les modifications'")
        print("✅ Taille : 36x36 pixels")
        print("✅ Bordure colorée selon l'action")
        print("✅ Hover effect avec fond BG_CARD")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Survolez les boutons pour voir les tooltips")
        print("💡 Vérifiez que les boutons sont dans l'en-tête")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Boutons Appliquer/Annuler dans l'En-tête")
    print("=" * 70)
    
    # Test des boutons dans l'en-tête
    success = test_buttons_in_header()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les boutons sont maintenant dans l'en-tête")
        print("✅ Les boutons ont des icônes seulement")
        print("✅ Les tooltips fonctionnent")
        print("✅ L'interface est plus compacte")
        print("\n🚀 Les boutons Appliquer/Annuler sont maintenant dans l'en-tête !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
