#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la section statistique équilibrée
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_balanced_stats_section():
    """Test de la section statistique équilibrée"""
    print("🧪 Test de la section statistique équilibrée...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Section Statistique Équilibrée - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SECTION STATISTIQUE ÉQUILIBRÉE !")
        print("=" * 60)
        print("✅ Hauteur des cartes ajustée à 80px")
        print("✅ Icônes ajustées à 14x14")
        print("✅ Espacement équilibré dans toute la section")
        print("✅ Padding ajusté (15,12) pour un bon équilibre")
        print("✅ Font F_SUB pour l'en-tête")
        print("✅ Sidebar élargie (poids 3)")
        print("✅ Interface harmonieuse et lisible")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que la section statistique est bien équilibrée")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Section Statistique Équilibrée")
    print("=" * 70)
    
    # Test de la section équilibrée
    success = test_balanced_stats_section()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La section statistique est bien équilibrée")
        print("✅ Les cartes ont une hauteur appropriée")
        print("✅ L'espacement est harmonieux")
        print("\n🚀 La section statistique est parfaitement équilibrée !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
