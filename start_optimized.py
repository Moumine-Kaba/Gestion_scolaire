#!/usr/bin/env python3
"""
SCRIPT DE DÉMARRAGE OPTIMISÉ EDUMANAGER+
========================================

Ce script démarre l'application avec toutes les optimisations activées.
"""

import sys
import os
import time

def main():
    """Fonction principale de démarrage"""
    print("🚀 Démarrage d'EduManager+ avec optimisations...")
    
    start_time = time.time()
    
    try:
        # Initialiser le système d'optimisation
        from src.core.optimization.edu_manager_optimizer import initialize_optimization_system
        initialize_optimization_system()
        
        # Démarrer l'application principale
        from src.modules.auth.views.dashboard_view import MainApp
        import customtkinter as ctk
        
        # Configurer CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Créer et lancer l'application
        app = MainApp()
        app.run()
        
    except Exception as e:
        print(f"❌ Erreur démarrage: {e}")
        sys.exit(1)
    
    finally:
        total_time = time.time() - start_time
        print(f"⏱️ Temps total de démarrage: {total_time:.3f}s")

if __name__ == "__main__":
    main()
