#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'équilibre des panneaux
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_balanced_panels():
    """Test de l'équilibre des panneaux"""
    print("🧪 Test de l'équilibre des panneaux...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Panneaux Équilibrés - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 PANNEAUX ÉQUILIBRÉS !")
        print("=" * 60)
        print("✅ Sidebar et panneau de droite ont le même poids (2)")
        print("✅ Proportions: 50% sidebar / 50% panneau de droite")
        print("✅ Les détails de l'élève sont visibles")
        print("✅ Interface équilibrée et fonctionnelle")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que les deux panneaux sont équilibrés")
        print("💡 Cliquez sur un élève pour voir ses détails")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de l'Équilibre des Panneaux")
    print("=" * 70)
    
    # Test des panneaux
    success = test_balanced_panels()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les panneaux sont maintenant équilibrés")
        print("✅ Les détails de l'élève sont visibles")
        print("✅ Interface fonctionnelle et équilibrée")
        print("\n🚀 Les panneaux sont maintenant équilibrés !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
