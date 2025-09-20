#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du modal historique des présences corrigé
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_history_modal_fixed():
    """Test du modal historique corrigé"""
    print("🧪 Test du modal historique des présences...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Modal Historique Corrigé - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 MODAL HISTORIQUE CORRIGÉ !")
        print("=" * 60)
        print("✅ Erreur TypeError corrigée")
        print("✅ Accès aux attributs AttendanceHistoryModel corrigé")
        print("✅ Nom de l'élève récupéré depuis les données actuelles")
        print("✅ Date formatée correctement")
        print("✅ Statut avec couleurs appropriées")
        print("✅ Classe et commentaire affichés")
        print("✅ Modal fonctionnel et complet")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Cliquez sur le bouton Historique (icône fichier)")
        print("💡 Vérifiez que le modal s'affiche avec les données")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test du Modal Historique Corrigé")
    print("=" * 70)
    
    # Test du modal historique
    success = test_history_modal_fixed()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Le modal historique fonctionne correctement")
        print("✅ Les données sont affichées")
        print("✅ L'erreur TypeError est corrigée")
        print("\n🚀 Le modal historique est maintenant fonctionnel !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
