# -*- coding: utf-8 -*-
"""
Lanceur du Système de Paiements Corrigé
EduManager+ - Système Fonctionnel

Ce script lance le système de paiements avec toutes les corrections appliquées.
"""

import os
import sys
import customtkinter as ctk

def setup_environment():
    """Configure l'environnement pour les imports"""
    print("Configuration de l'environnement...")
    
    # Ajouter les chemins nécessaires
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../../../..'))
    src_root = os.path.join(project_root, 'Gestion_scolaire')
    
    # Ajouter les chemins dans l'ordre correct
    paths_to_add = [project_root, src_root]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"Repertoire projet: {project_root}")
    return project_root

def launch_payments_view():
    """Lance la vue des paiements"""
    print("Lancement de la vue des paiements...")
    
    try:
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Créer la fenêtre principale
        root = ctk.CTk()
        root.title("EduManager+ - Système de Paiements Amélioré")
        root.geometry("1400x900")
        
        # Centrer la fenêtre
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1400 // 2)
        y = (root.winfo_screenheight() // 2) - (900 // 2)
        root.geometry(f"1400x900+{x}+{y}")
        
        # Importer et créer la vue
        try:
            from Gestion_scolaire.src.modules.administrative.payments.views.paiements_view import PaiementsView
            from Gestion_scolaire.resources.themes.theme import apply_theme_to_app, MARGIN_LARGE
            
            # Appliquer le thème EduManager+
            apply_theme_to_app(root)
            
            # Créer et afficher la vue
            paiements_view = PaiementsView(root)
            paiements_view.pack(fill="both", expand=True, padx=5, pady=5)
            
            print("SUCCES - Interface lancee avec succes")
            print("Le systeme de paiements ameliore est maintenant actif !")
            print()
            print("Fonctionnalites disponibles:")
            print("  - Tableau de bord moderne")
            print("  - Gestion des types de frais")
            print("  - Echeanciers automatiques")
            print("  - Systeme de remises")
            print("  - Rapports financiers")
            print("  - Statistiques en temps reel")
            
            # Lancer l'application
            root.mainloop()
            
        except ImportError as e:
            print(f"ERREUR import vue: {e}")
            print("Verifiez que tous les modules sont correctement installes")
            
            # Afficher une fenêtre d'erreur simple
            error_window = ctk.CTk()
            error_window.title("Erreur - EduManager+")
            error_window.geometry("500x300")
            
            error_frame = ctk.CTkFrame(error_window)
            error_frame.pack(expand=True, fill="both", padx=20, pady=20)
            
            ctk.CTkLabel(error_frame, text="ERREUR DE CHARGEMENT", 
                        font=("Arial", 16, "bold")).pack(pady=20)
            
            ctk.CTkLabel(error_frame, text="Impossible de charger le module de paiements.", 
                        font=("Arial", 12)).pack(pady=10)
            
            ctk.CTkLabel(error_frame, text=f"Erreur: {str(e)}", 
                        font=("Arial", 10), text_color="red").pack(pady=10)
            
            ctk.CTkButton(error_frame, text="Fermer", 
                         command=error_window.destroy).pack(pady=20)
            
            error_window.mainloop()
            
    except Exception as e:
        print(f"ERREUR critique: {e}")
        print("Le systeme ne peut pas demarrer")

def show_startup_info():
    """Affiche les informations de démarrage"""
    print("=" * 60)
    print("EDUMANAGER+ - SYSTEME DE PAIEMENTS AMELIORE")
    print("=" * 60)
    print("Version: 2.0 (Corrigee)")
    print("Date: 2024")
    print()
    print("Nouvelles fonctionnalites:")
    print("  - Gestion des types de frais")
    print("  - Echeanciers automatiques")
    print("  - Systeme de remises et bourses")
    print("  - Relances automatiques")
    print("  - Rapports financiers avances")
    print("  - Penalites de retard")
    print("  - Statistiques en temps reel")
    print()
    print("Corrections appliquees:")
    print("  - Noms de colonnes corriges")
    print("  - Requetes SQL optimisees")
    print("  - Compatibilite base de donnees")
    print()
    print("=" * 60)

def main():
    """Fonction principale"""
    try:
        # Afficher les informations de démarrage
        show_startup_info()
        
        # Configurer l'environnement
        project_root = setup_environment()
        
        # Lancer l'interface
        launch_payments_view()
        
    except KeyboardInterrupt:
        print("\nArret demande par l'utilisateur")
    except Exception as e:
        print(f"\nERREUR critique: {e}")
        print("Contactez le support technique")

if __name__ == "__main__":
    main()
