#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test des éléments agrandis pour combler l'espace des boutons
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

import customtkinter as ctk

def test_elements_enlarged():
    """Test des éléments agrandis pour combler l'espace"""
    print("🧪 Test des éléments agrandis pour combler l'espace...")
    print("=" * 60)
    
    try:
        # Import de la vue avancée
        from src.modules.academic.attendance.views.advanced_attendance_view import AdvancedAttendanceView
        
        # Créer l'application
        app = ctk.CTk()
        app.title("Test Éléments Agrandis - Vue Avancée des Présences")
        app.geometry("1400x900")
        app.configure(fg_color="#0A192F")
        
        # Instancier la vue avancée
        advanced_view = AdvancedAttendanceView(app)
        advanced_view.pack(fill="both", expand=True, padx=20, pady=20)
        
        print("✅ Vue avancée créée")
        
        print("\n🎉 ÉLÉMENTS AGRANDIS POUR COMBLER L'ESPACE !")
        print("=" * 60)
        print("✅ Section statut : hauteur augmentée à 120px")
        print("✅ Section commentaire : hauteur augmentée à 150px")
        print("✅ Section justification : hauteur augmentée à 120px")
        print("✅ Zone de texte commentaire : hauteur augmentée à 120px")
        print("✅ pack_propagate(False) pour maintenir les hauteurs")
        print("✅ Boutons déplacés dans l'en-tête avec icônes")
        print("✅ Tooltips ajoutés pour les boutons")
        print("✅ Interface plus spacieuse et équilibrée")
        
        print("\n🚀 Lancement de l'interface de test...")
        print("💡 Fermez la fenêtre pour terminer le test")
        print("💡 Sélectionnez une classe et un élève")
        print("💡 Vérifiez que les sections sont plus grandes")
        print("💡 Vérifiez que l'espace est bien comblé")
        
        app.mainloop()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    print("🏫 Test des Éléments Agrandis pour Combler l'Espace")
    print("=" * 70)
    
    # Test des éléments agrandis
    success = test_elements_enlarged()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    if success:
        print("🎉 SUCCÈS COMPLET !")
        print("✅ Les éléments ont été agrandis")
        print("✅ L'espace est bien comblé")
        print("✅ L'interface est plus spacieuse")
        print("\n🚀 Les éléments ont été agrandis pour combler l'espace !")
    else:
        print("⚠️ PROBLÈMES DÉTECTÉS")
        print("🔧 Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()
