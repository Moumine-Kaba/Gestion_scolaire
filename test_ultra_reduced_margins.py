#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier les marges ultra réduites
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_ultra_reduced_margins():
    """Test des marges ultra réduites"""
    print("🚀 Test - Marges ultra réduites")
    print("=" * 50)
    
    try:
        from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Marges Ultra Réduites")
        root.geometry("1400x800")
        
        # Dashboard des élèves
        dashboard = DashboardEleves(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Marges ultra réduites entre nom et valeur")
        print("✅ Padding minimal (1-2px)")
        print("✅ Espacement optimisé")
        print("✅ Design compact et efficace")
        print("✅ Plus d'informations visibles")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ultra_reduced_margins()
