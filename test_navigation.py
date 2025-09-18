#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier que le système de navigation fonctionne
"""

import sys
import os
sys.path.insert(0, '.')

try:
    import customtkinter as ctk
    from src.modules.academic.students.views.eleves_dashboard import DashboardEleves
    
    print("🚀 Test du système de navigation...")
    
    # Créer une fenêtre de test
    root = ctk.CTk()
    root.title("Test Navigation - EduManager+")
    root.geometry("1200x800")
    
    # Créer le dashboard
    dashboard = DashboardEleves(root)
    dashboard.pack(fill="both", expand=True)
    
    print("✅ Dashboard créé avec succès")
    print("✅ Système de navigation prêt")
    print("📝 Instructions de test:")
    print("   1. Cliquez sur une classe dans la sidebar")
    print("   2. Vérifiez que la vue change pour afficher les étudiants")
    print("   3. Utilisez le bouton retour (←) pour revenir aux classes")
    print("   4. Testez les boutons CRUD (Modifier, Supprimer, Exporter)")
    
    # Démarrer l'application
    root.mainloop()
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
