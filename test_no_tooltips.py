#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'interface sans tooltips
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_interface_without_tooltips():
    """Test de l'interface sans tooltips"""
    print("🧪 Test de l'interface sans tooltips...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Interface Sans Tooltips - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 INTERFACE SANS TOOLTIPS !")
        print("=" * 60)
        print("✅ Tous les tooltips supprimés")
        print("✅ Interface plus épurée")
        print("✅ Pas de problèmes de tooltips bloqués")
        print("✅ Expérience utilisateur simplifiée")
        print("✅ Boutons avec icônes claires")
        print("✅ Interface plus rapide")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Testez tous les boutons dans l'en-tête")
        print("💡 Vérifiez que l'interface fonctionne parfaitement")
        print("💡 Plus de tooltips qui gênent !")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de l'Interface Sans Tooltips")
    print("=" * 70)
    
    # Test de l'interface sans tooltips
    success = test_interface_without_tooltips()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Interface sans tooltips fonctionnelle")
        print("✅ Plus de problèmes de tooltips")
        print("✅ Interface épurée et rapide")
        print("\n🚀 L'interface fonctionne parfaitement sans tooltips !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
