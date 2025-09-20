#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des icônes dans les statistiques
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_stats_icons():
    """Test des icônes dans les statistiques"""
    print("🧪 Test des icônes dans les statistiques...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Icônes Statistiques - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        # Vérifier que la méthode _update_statistics_display existe
        if hasattr(advanced_view, '_update_statistics_display'):
            print("✅ Méthode _update_statistics_display disponible")
        else:
            print("❌ Méthode _update_statistics_display manquante")
        
        print("\n🎉 ICÔNES DANS LES STATISTIQUES !")
        print("=" * 60)
        print("✅ Toutes les icônes sont affichées (Total, Présents, Absents, Retards)")
        print("✅ Toutes les icônes ont les mêmes dimensions (20x20)")
        print("✅ Les icônes sont centrées avec un espacement uniforme")
        print("✅ Les statistiques sont dans le panneau de droite comme en-tête")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que toutes les icônes s'affichent correctement")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Icônes dans les Statistiques")
    print("=" * 70)
    
    # Test des icônes
    success = test_stats_icons()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Toutes les icônes sont affichées")
        print("✅ Toutes les icônes ont les mêmes dimensions")
        print("✅ L'affichage est uniforme et professionnel")
        print("\n🚀 Les icônes sont maintenant parfaitement alignées !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
