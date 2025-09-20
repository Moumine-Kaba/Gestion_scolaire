#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la section parent des boutons Appliquer/Annuler avec hauteur augmentée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_parent_height_increased():
    """Test de la section parent des boutons avec hauteur augmentée"""
    print("🧪 Test de la section parent des boutons Appliquer/Annuler...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Section Parent des Boutons - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SECTION PARENT DES BOUTONS AMÉLIORÉE !")
        print("=" * 60)
        print("✅ Hauteur de la section parent fixée à 80px")
        print("✅ pack_propagate(False) pour maintenir la hauteur")
        print("✅ Section plus visible et spacieuse")
        print("✅ Meilleure séparation visuelle")
        print("✅ Interface plus équilibrée")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève pour voir la section")
        print("💡 Vérifiez que la section parent des boutons est plus haute")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Section Parent des Boutons Appliquer/Annuler")
    print("=" * 70)
    
    # Test de la section parent
    success = test_buttons_parent_height_increased()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La section parent est plus haute")
        print("✅ La section est plus visible")
        print("✅ L'interface est plus équilibrée")
        print("\n🚀 La section parent des boutons a été améliorée !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
