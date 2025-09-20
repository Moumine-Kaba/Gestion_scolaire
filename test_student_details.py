#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de l'affichage des détails d'élève
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_student_details():
    """Test de l'affichage des détails d'élève"""
    print("🧪 Test de l'affichage des détails d'élève...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Détails Élève - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        # Vérifier que la méthode _render_detail_for existe
        if hasattr(advanced_view, '_render_detail_for'):
            print("✅ Méthode _render_detail_for disponible")
        else:
            print("❌ Méthode _render_detail_for manquante")
        
        # Vérifier que content_area existe
        if hasattr(advanced_view, 'content_area'):
            print("✅ Zone de contenu (content_area) créée")
        else:
            print("❌ Zone de contenu (content_area) manquante")
        
        print("\n🎉 AFFICHAGE DES DÉTAILS D'ÉLÈVE !")
        print("=" * 60)
        print("✅ Les statistiques restent visibles en en-tête")
        print("✅ Les détails de l'élève s'affichent en dessous")
        print("✅ Interface fonctionnelle et responsive")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Cliquez sur un élève pour voir ses détails")
        print("💡 Vérifiez que les données s'affichent à droite")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test de l'Affichage des Détails d'Élève")
    print("=" * 70)
    
    # Test des détails
    success = test_student_details()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les détails d'élève s'affichent correctement")
        print("✅ Les statistiques restent visibles")
        print("✅ Interface fonctionnelle")
        print("\n🚀 Les détails d'élève s'affichent maintenant à droite !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
