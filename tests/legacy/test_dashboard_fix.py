#!/usr/bin/env python3
"""
Script de test pour vérifier que le dashboard fonctionne sans erreur d'image
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Ajouter le répertoire racine au path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_dashboard():
    """Teste le dashboard sans erreur d'image"""
    try:
        print("🧪 Test du dashboard...")
        
        # Importer les modules nécessaires
        from views.dashboard_view import MainApp
        
        # Créer une fenêtre Tkinter temporaire
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Créer l'application de test
        utilisateur = {"username": "admin", "id": 1}
        app = MainApp(utilisateur)
        
        # Vérifier que les références sont bien initialisées
        print(f"✅ Références d'images: {len(app._img_refs)}")
        print(f"✅ Références matplotlib: {len(app._matplotlib_refs)}")
        print(f"✅ Icônes chargées: {len(app.icons)}")
        
        # Tester la création du dashboard
        print("🔄 Test création dashboard...")
        app.create_dashboard()
        print("✅ Dashboard créé avec succès")
        
        # Tester la mise à jour du graphique
        print("🔄 Test mise à jour graphique...")
        app.update_graph()
        print("✅ Graphique mis à jour avec succès")
        
        # Nettoyer
        app._cleanup_images()
        app.destroy()
        root.destroy()
        
        print("🎉 Tous les tests sont passés avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dashboard()
    if success:
        print("\n✅ Le problème d'image 'pyimage3' a été résolu !")
    else:
        print("\n❌ Il y a encore des problèmes à résoudre.")
    
    input("\nAppuyez sur Entrée pour continuer...")
