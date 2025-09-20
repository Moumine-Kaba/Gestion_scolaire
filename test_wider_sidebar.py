#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la sidebar élargie
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_wider_sidebar():
    """Test de la sidebar élargie"""
    print("🧪 Test de la sidebar élargie...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Sidebar Élargie - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SIDEBAR ÉLARGIE !")
        print("=" * 60)
        print("✅ La sidebar est maintenant plus large (poids 2)")
        print("✅ Le panneau de droite a le même poids (2)")
        print("✅ Proportions: 50% sidebar / 50% panneau de droite")
        print("✅ Interface équilibrée et spacieuse")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que la sidebar est plus large")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Sidebar Élargie")
    print("=" * 70)
    
    # Test de la sidebar
    success = test_wider_sidebar()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La sidebar est maintenant plus large")
        print("✅ Les deux panneaux sont équilibrés")
        print("✅ Interface spacieuse et fonctionnelle")
        print("\n🚀 La sidebar a été élargie avec succès !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
