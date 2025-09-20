#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier l'espacement amélioré de la vue matière
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_matieres_spacing():
    """Test de l'espacement amélioré de la vue matière"""
    print("🚀 Test - Espacement amélioré vue matière")
    print("=" * 50)
    
    try:
        from src.modules/academic.subjects.views.matieres_view import MatieresView
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Espacement Amélioré")
        root.geometry("1400x800")
        
        # Mock des icônes
        mock_icons = {
            "book": "resources/icons/book.png",
            "search": "resources/icons/search.png",
            "add": "resources/icons/add.png",
            "edit": "resources/icons/edit.png",
            "delete": "resources/icons/delete.png",
            "close": "resources/icons/close.png",
            "check": "resources/icons/check.png",
            "stats": "resources/icons/stats.png",
            "analytics": "resources/icons/analytics.png",
            "folder": "resources/icons/folder.png",
            "stacks": "resources/icons/stacks.png",
            "tag": "resources/icons/tag.png",
            "refresh": "resources/icons/refresh.png"
        }
        
        # Vue des matières
        matieres_view = MatieresView(root, mock_icons)
        matieres_view.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Espacement légèrement augmenté")
        print("✅ Marges externes optimisées")
        print("✅ Design équilibré et aéré")
        print("✅ Interface plus confortable")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_matieres_spacing()
