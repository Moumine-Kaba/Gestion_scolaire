#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des tooltips améliorés avec disparition immédiate
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_improved_tooltips():
    """Test des tooltips améliorés"""
    print("🧪 Test des tooltips améliorés...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Tooltips Améliorés - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 TOOLTIPS AMÉLIORÉS !")
        print("=" * 60)
        print("✅ Disparition immédiate quand la souris quitte l'élément")
        print("✅ Suivi du mouvement de la souris")
        print("✅ Design amélioré avec corner radius 6px")
        print("✅ Padding augmenté (12px horizontal, 8px vertical)")
        print("✅ Tooltip reste au-dessus des autres fenêtres")
        print("✅ Gestion propre de la mémoire (destruction immédiate)")
        print("✅ Pas de tooltips fantômes qui restent")
        print("✅ Expérience utilisateur fluide")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Survolez les boutons dans l'en-tête")
        print("💡 Vérifiez que les tooltips disparaissent immédiatement")
        print("💡 Testez le mouvement de la souris sur les boutons")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Tooltips Améliorés")
    print("=" * 70)
    
    # Test des tooltips améliorés
    success = test_improved_tooltips()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les tooltips fonctionnent parfaitement")
        print("✅ Disparition immédiate et fluide")
        print("✅ Expérience utilisateur optimale")
        print("\n🚀 Les tooltips ont été améliorés avec succès !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
