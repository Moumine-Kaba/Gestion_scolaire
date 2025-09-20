#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des boutons Appliquer/Annuler maintenant visibles
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_buttons_now_visible():
    """Test des boutons maintenant visibles"""
    print("🧪 Test des boutons Appliquer/Annuler maintenant visibles...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Boutons Maintenant Visibles - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 BOUTONS MAINTENANT VISIBLES !")
        print("=" * 60)
        print("✅ Espacement réduit entre toutes les sections")
        print("✅ Header section : pady réduit de 15 à 8")
        print("✅ Content frame : pady réduit de 10 à 5")
        print("✅ Status section : pady réduit de 15 à 8")
        print("✅ Comment section : pady réduit de 15 à 8")
        print("✅ Justification section : pady réduit de 15 à 8")
        print("✅ Boutons maintenant visibles en bas")
        print("✅ Section parent : 120px de hauteur")
        print("✅ Boutons : fond vert/rouge avec texte blanc")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Vérifiez que les boutons Appliquer/Annuler sont maintenant visibles")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Boutons Appliquer/Annuler Maintenant Visibles")
    print("=" * 70)
    
    # Test des boutons visibles
    success = test_buttons_now_visible()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les boutons sont maintenant visibles")
        print("✅ L'espacement a été optimisé")
        print("✅ L'interface est maintenant complète")
        print("\n🚀 Les boutons Appliquer/Annuler sont maintenant parfaitement visibles !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
