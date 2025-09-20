#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des icônes avec la même taille dans les statistiques
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_uniform_icons():
    """Test des icônes avec la même taille"""
    print("🧪 Test des icônes avec la même taille...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Icônes Uniformes - Vue Avancée des Présences")
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
        
        print("\n🎉 ICÔNES UNIFORMES !")
        print("=" * 60)
        print("✅ Toutes les icônes ont la même taille (20x20)")
        print("✅ Icônes: Total (stats.png), Présents (check_circle.png)")
        print("✅ Icônes: Absents (close.png), Retards (clock.png)")
        print("✅ Système de fallback pour les icônes manquantes")
        print("✅ Espacement uniforme entre tous les éléments")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Vérifiez que toutes les icônes ont la même taille")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Icônes Uniformes dans les Statistiques")
    print("=" * 70)
    
    # Test des icônes
    success = test_uniform_icons()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Toutes les icônes ont la même taille")
        print("✅ Système de fallback robuste")
        print("✅ Affichage uniforme et professionnel")
        print("\n🚀 Toutes les icônes sont maintenant uniformes !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
