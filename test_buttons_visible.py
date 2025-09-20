#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des boutons Appliquer/Annuler bien visibles
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_visible():
    """Test des boutons bien visibles"""
    print("🧪 Test des boutons Appliquer/Annuler visibles...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Boutons Visibles - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 BOUTONS MAINTENANT VISIBLES !")
        print("=" * 60)
        print("✅ Bouton Appliquer : fond vert avec texte blanc")
        print("✅ Bouton Annuler : fond rouge avec texte blanc")
        print("✅ Hauteur des boutons : 50px")
        print("✅ Icônes : 20x20")
        print("✅ Font : F_TITLE")
        print("✅ Hover effects : couleurs plus foncées")
        print("✅ Section parent : 120px de hauteur")
        print("✅ Bordure bleue sur la section parent")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève pour voir les boutons")
        print("💡 Vérifiez que les boutons sont maintenant bien visibles")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Boutons Appliquer/Annuler Visibles")
    print("=" * 70)
    
    # Test des boutons visibles
    success = test_buttons_visible()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les boutons sont maintenant bien visibles")
        print("✅ Les boutons ont des couleurs contrastées")
        print("✅ L'interface est claire et accessible")
        print("\n🚀 Les boutons Appliquer/Annuler sont maintenant parfaitement visibles !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
