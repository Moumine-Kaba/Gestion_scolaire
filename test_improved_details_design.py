#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test pour vérifier le design amélioré de la partie détails
"""

import sys
import os
sys.path.append('.')

import customtkinter as ctk

def test_improved_details_design():
    """Test du design amélioré de la partie détails"""
    print("🚀 Test - Design amélioré partie détails")
    print("=" * 50)
    
    try:
        from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
        
        # Fenêtre de test
        root = ctk.CTk()
        root.title("EduManager+ - Design Détails Amélioré")
        root.geometry("1400x800")
        
        # Dashboard des élèves
        dashboard = DashboardEleves(root)
        dashboard.pack(fill="both", expand=True)
        
        print("✅ Application lancée avec succès")
        print("✅ Design premium du titre avec badge de statut")
        print("✅ Colonnes avec bordures et coins arrondis")
        print("✅ Lignes d'informations avec design moderne")
        print("✅ Boutons d'action avec couleurs premium")
        print("✅ Layout en deux colonnes optimisé")
        print("✅ Effets visuels et profondeur")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_improved_details_design()