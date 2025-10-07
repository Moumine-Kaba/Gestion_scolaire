# -*- coding: utf-8 -*-
"""
Test final du système de paiements avec corrections
"""

import os
import sys
import customtkinter as ctk

def main():
    """Test final du système"""
    print("Test final du système de paiements...")
    
    # Configuration de l'environnement
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, '../../../../..'))
    src_root = os.path.join(project_root, 'Gestion_scolaire')
    
    # Ajouter les chemins
    paths_to_add = [project_root, src_root]
    for path in paths_to_add:
        if path not in sys.path:
            sys.path.insert(0, path)
    
    print(f"Racine du projet: {project_root}")
    print(f"Racine src: {src_root}")
    
    # Vérifier les chemins des ressources
    resources_path = os.path.join(src_root, "resources")
    icons_path = os.path.join(resources_path, "icons")
    themes_path = os.path.join(resources_path, "themes")
    
    print(f"Chemin ressources: {resources_path} - Existe: {os.path.exists(resources_path)}")
    print(f"Chemin icônes: {icons_path} - Existe: {os.path.exists(icons_path)}")
    print(f"Chemin thèmes: {themes_path} - Existe: {os.path.exists(themes_path)}")
    
    try:
        # Configuration de CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Créer la fenêtre principale
        root = ctk.CTk()
        root.title("Test Final - Système de Paiements")
        root.geometry("1400x900")
        
        # Test d'import
        print("Test d'import des modules...")
        from Gestion_scolaire.src.modules.administrative.payments.views.paiements_view import PaiementsView
        print("Import réussi!")
        
        # Créer la vue
        paiements_view = PaiementsView(root)
        paiements_view.pack(fill="both", expand=True, padx=5, pady=5)
        
        print("Interface créée avec succès!")
        print("Lancement de l'interface...")
        
        # Lancer l'application
        root.mainloop()
        
    except Exception as e:
        print(f"ERREUR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
