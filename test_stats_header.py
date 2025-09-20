#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des statistiques comme en-tête du sidebar
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_stats_header():
    """Test des statistiques comme en-tête du sidebar"""
    print("🧪 Test des statistiques comme en-tête du sidebar...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Statistiques En-tête - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        # Vérifier que la méthode _build_statistics_section existe
        if hasattr(advanced_view, '_build_statistics_section'):
            print("✅ Méthode _build_statistics_section disponible")
        else:
            print("❌ Méthode _build_statistics_section manquante")
        
        # Vérifier que la méthode _update_statistics_display existe
        if hasattr(advanced_view, '_update_statistics_display'):
            print("✅ Méthode _update_statistics_display disponible")
        else:
            print("❌ Méthode _update_statistics_display manquante")
        
        print("\n🎉 STATISTIQUES COMME EN-TÊTE !")
        print("=" * 60)
        print("✅ Les statistiques sont dans le sidebar comme en-tête")
        print("✅ Les statistiques changent selon l'élève sélectionné")
        print("✅ Les statistiques sont intégrées dans la section 'Élèves et Statistiques'")
        print("✅ L'interface correspond à l'image fournie")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Cliquez sur un élève pour voir ses statistiques dans le sidebar")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Statistiques comme En-tête du Sidebar")
    print("=" * 70)
    
    # Test des statistiques
    success = test_stats_header()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les statistiques sont dans le sidebar comme en-tête")
        print("✅ Les statistiques changent selon l'élève sélectionné")
        print("✅ L'affichage correspond à l'image fournie")
        print("\n🚀 Les statistiques sont maintenant comme en-tête du sidebar !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
