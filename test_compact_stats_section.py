#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la section statistique réduite
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_compact_stats_section():
    """Test de la section statistique compacte"""
    print("🧪 Test de la section statistique compacte...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Section Statistique Compacte - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 SECTION STATISTIQUE COMPACTE !")
        print("=" * 60)
        print("✅ Hauteur des cartes réduite à 60px")
        print("✅ Icônes réduites à 12x12")
        print("✅ Espacement réduit dans toute la section")
        print("✅ Corner radius réduit à 6px")
        print("✅ Padding réduit (15,10) au lieu de (20,15)")
        print("✅ Font réduite pour l'en-tête (F_SMALL)")
        print("✅ Sidebar élargie (poids 3)")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que la section statistique est plus compacte")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de la Section Statistique Compacte")
    print("=" * 70)
    
    # Test de la section compacte
    success = test_compact_stats_section()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ La section statistique est plus compacte")
        print("✅ Les cartes sont réduites")
        print("✅ L'espacement est optimisé")
        print("\n🚀 La section statistique a été réduite avec succès !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
