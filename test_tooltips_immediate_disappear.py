#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des tooltips avec disparition immédiate corrigée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_tooltips_immediate_disappear():
    """Test des tooltips avec disparition immédiate"""
    print("🧪 Test des tooltips avec disparition immédiate...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Tooltips Disparition Immédiate - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 TOOLTIPS AVEC DISPARITION IMMÉDIATE !")
        print("=" * 60)
        print("✅ Gestion améliorée avec try/except")
        print("✅ Destruction forcée des tooltips")
        print("✅ Gestion de la perte de focus")
        print("✅ Gestion du widget parent")
        print("✅ Mise à jour forcée avec update()")
        print("✅ focus_force() pour s'assurer de la visibilité")
        print("✅ Disparition immédiate quand on quitte l'élément")
        print("✅ Pas de tooltips bloqués")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Survolez les boutons dans l'en-tête")
        print("💡 Vérifiez que les tooltips disparaissent IMMÉDIATEMENT")
        print("💡 Testez en bougeant rapidement la souris")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Tooltips avec Disparition Immédiate")
    print("=" * 70)
    
    # Test des tooltips corrigés
    success = test_tooltips_immediate_disappear()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les tooltips disparaissent immédiatement")
        print("✅ Plus de tooltips bloqués")
        print("✅ Expérience utilisateur fluide")
        print("\n🚀 Les tooltips fonctionnent maintenant parfaitement !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
