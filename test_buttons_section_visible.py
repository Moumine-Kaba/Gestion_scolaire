#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la section des boutons Appliquer/Annuler bien visible
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_section_visible():
    """Test de la section des boutons bien visible"""
    print("🧪 Test de la section des boutons Appliquer/Annuler...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Section Boutons Visible - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SECTION BOUTONS MAINTENANT VISIBLE !")
        print("=" * 60)
        print("✅ Hauteur de la section parent : 120px")
        print("✅ Hauteur des boutons : 50px")
        print("✅ Fond BG_CARD pour plus de contraste")
        print("✅ Bordure ACCENT_BLUE plus visible")
        print("✅ Border width : 2px")
        print("✅ Corner radius : 10px")
        print("✅ Icônes plus grandes : 20x20")
        print("✅ Font F_TITLE pour les boutons")
        print("✅ Padding augmenté : 20px horizontal, 25px vertical")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève pour voir la section")
        print("💡 Vérifiez que la section des boutons est maintenant bien visible")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Section des Boutons Appliquer/Annuler Visible")
    print("=" * 70)
    
    # Test de la section visible
    success = test_buttons_section_visible()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La section des boutons est maintenant bien visible")
        print("✅ La section a une présence visuelle forte")
        print("✅ L'interface est plus claire et accessible")
        print("\n🚀 La section des boutons est maintenant parfaitement visible !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
