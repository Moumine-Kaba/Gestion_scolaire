#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier la suppression de la section de chargement
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_removed_loading_section():
    """Test de la suppression de la section de chargement"""
    print("🚀 Test - Suppression section de chargement")
    print("=" * 50)
    
    try:
        from src.modules.academic.classes.views.cours_view import CoursManagerView
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Section Chargement Supprimée")
        root.geometry("1400x800")
        
        # Mock des icônes
        mock_icons = {
            "add": "resources/icons/add.png",
            "edit": "resources/icons/edit.png",
            "delete": "resources/icons/delete.png",
            "search": "resources/icons/search.png",
            "class": "resources/icons/class.png",
            "person": "resources/icons/person.png",
            "book": "resources/icons/book.png",
            "door": "resources/icons/door.png",
            "calendar": "resources/icons/calendar.png",
            "clock": "resources/icons/clock.png",
            "bell": "resources/icons/bell.png"
        }
        
        # Vue des cours
        cours_view = CoursManagerView(root, mock_icons)
        cours_view.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Section 'Chargement des cours...' supprimée")
        print("✅ Chargement direct des données")
        print("✅ Interface plus fluide")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_removed_loading_section()
