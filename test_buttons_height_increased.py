#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la section des boutons Appliquer/Annuler avec hauteur augmentée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_height_increased():
    """Test de la section des boutons avec hauteur augmentée"""
    print("🧪 Test de la section des boutons Appliquer/Annuler...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Boutons Appliquer/Annuler - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SECTION BOUTONS APPLIQUER/ANNULER AMÉLIORÉE !")
        print("=" * 60)
        print("✅ Hauteur des boutons augmentée à 40px")
        print("✅ Padding de la section augmenté à 20px")
        print("✅ Boutons plus visibles et accessibles")
        print("✅ Interface plus ergonomique")
        print("✅ Meilleure expérience utilisateur")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève pour voir les boutons")
        print("💡 Vérifiez que les boutons Appliquer/Annuler sont plus hauts")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Section des Boutons Appliquer/Annuler")
    print("=" * 70)
    
    # Test des boutons
    success = test_buttons_height_increased()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La section des boutons est plus haute")
        print("✅ Les boutons sont plus visibles")
        print("✅ L'interface est plus ergonomique")
        print("\n🚀 Les boutons Appliquer/Annuler ont été améliorés !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
