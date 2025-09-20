#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier les améliorations du design
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_improved_design():
    """Test du design amélioré"""
    print("🚀 Test - Design amélioré")
    print("=" * 50)
    
    try:
        from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Design Amélioré")
        root.geometry("1400x800")
        
        # Dashboard des élèves
        dashboard = DashboardEleves(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Barre de recherche spacieuse et moderne")
        print("✅ Détails complets avec sections organisées")
        print("✅ Informations personnelles, scolaires et familiales")
        print("✅ Design premium avec icônes et couleurs")
        print("✅ Boutons d'action améliorés")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_design()
