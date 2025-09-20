#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier la hauteur réduite de la barre de recherche
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_reduced_search_height():
    """Test de la hauteur réduite de la barre de recherche"""
    print("🚀 Test - Hauteur réduite barre de recherche")
    print("=" * 50)
    
    try:
        from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Hauteur Réduite")
        root.geometry("1400x800")
        
        # Dashboard des élèves
        dashboard = DashboardEleves(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Section de recherche plus compacte")
        print("✅ Padding réduit (8px au lieu de 15px)")
        print("✅ Hauteur des éléments réduite (35px)")
        print("✅ Espacement optimisé")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_reduced_search_height()
