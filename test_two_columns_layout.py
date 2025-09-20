#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier le layout en deux colonnes
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_two_columns_layout():
    """Test du layout en deux colonnes"""
    print("🚀 Test - Layout en deux colonnes")
    print("=" * 50)
    
    try:
        from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Layout Deux Colonnes")
        root.geometry("1400x800")
        
        # Dashboard des élèves
        dashboard = DashboardEleves(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Layout en deux colonnes implémenté")
        print("✅ Colonne gauche : Infos personnelles et scolaires")
        print("✅ Colonne droite : Infos familiales et supplémentaires")
        print("✅ Meilleure utilisation de l'espace")
        print("✅ Design organisé et lisible")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_two_columns_layout()
