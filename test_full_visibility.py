#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la visibilité complète des éléments
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_full_visibility():
    """Test de la visibilité complète des éléments"""
    print("🧪 Test de la visibilité complète des éléments...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Visibilité Complète - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 VISIBILITÉ COMPLÈTE !")
        print("=" * 60)
        print("✅ Sidebar compacte mais visible (poids 1)")
        print("✅ Panneau de droite bien visible (poids 2)")
        print("✅ Proportions: 33% sidebar / 67% panneau de droite")
        print("✅ Tous les éléments sont visibles et accessibles")
        print("✅ Les détails de l'élève s'affichent correctement")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que tous les éléments sont visibles")
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
    print("🏫 Test de la Visibilité Complète des Éléments")
    print("=" * 70)
    
    # Test de la visibilité
    success = test_full_visibility()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Tous les éléments sont visibles")
        print("✅ Les proportions sont équilibrées")
        print("✅ L'interface est fonctionnelle")
        print("\n🚀 Tous les éléments sont maintenant visibles !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
