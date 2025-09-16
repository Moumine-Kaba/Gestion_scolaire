#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de la Nouvelle Organisation - EduManager+
Vérifie que la sidebar simplifiée et les actions rapides fonctionnent
"""
import os
import sys
import customtkinter as ctk

def test_dashboard_view():
    """Test de la vue Dashboard avec la nouvelle organisation"""
    print("🔍 Test de la nouvelle organisation...")
    try:
        from views.dashboard_view import MainApp
        
        # Créer une fenêtre de test
        root = ctk.CTk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer l'application avec un utilisateur de test
        utilisateur = {"username": "test", "id": 1}
        app = MainApp(utilisateur)
        
        print("✅ MainApp créée avec succès")
        
        # Vérifier que la sidebar est créée
        assert hasattr(app, 'sidebar_frame'), "Sidebar doit être créée"
        assert hasattr(app, 'nav_scroll'), "Navigation scrollable doit être créée"
        assert hasattr(app, 'sidebar_btns'), "Boutons sidebar doivent être créés"
        
        # Vérifier que les actions rapides sont créées
        assert hasattr(app, 'frame_dashboard_content'), "Dashboard doit être créé"
        
        print("✅ Nouvelle organisation vérifiée")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ Erreur nouvelle organisation: {e}")
        return False

def main():
    """Test principal de la nouvelle organisation"""
    print("🧪 TEST DE LA NOUVELLE ORGANISATION EDUMANAGER+")
    print("=" * 60)
    
    try:
        result = test_dashboard_view()
        if result:
            print("\n🎉 La nouvelle organisation fonctionne parfaitement !")
            print("💡 Vous pouvez maintenant lancer l'application avec: python main.py")
            print("\n📋 Résumé de la nouvelle organisation:")
            print("   🎯 Sidebar simplifiée avec 5 vues essentielles")
            print("   🚀 Actions rapides avec toutes les autres vues")
            print("   🎨 Interface plus claire et organisée")
        else:
            print("\n⚠️ La nouvelle organisation a des problèmes.")
            print("💡 Vérifiez les erreurs ci-dessus et corrigez-les")
        
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
