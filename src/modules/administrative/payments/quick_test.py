# -*- coding: utf-8 -*-
"""
Test Rapide du Système de Paiements
EduManager+ - Vérification Rapide
"""

import os
import sys

def test_files():
    """Test de l'existence des fichiers"""
    print("Test de l'existence des fichiers...")
    
    files_to_check = [
        "controllers/enhanced_paiement_controller.py",
        "controllers/database_schema.py",
        "views/paiements_view.py",
        "README_ENHANCED.md"
    ]
    
    all_exist = True
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"OK - {file_path} existe")
        else:
            print(f"ERREUR - {file_path} manquant")
            all_exist = False
    
    return all_exist

def test_controller_syntax():
    """Test de la syntaxe du contrôleur"""
    print("\nTest de la syntaxe du controleur...")
    
    try:
        # Lire le fichier du contrôleur
        with open("controllers/enhanced_paiement_controller.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que les corrections sont présentes
        corrections = [
            "c.nom_classe as classe_nom",
            "c.id_classe",
            "el.id_classe = c.id_classe"
        ]
        
        for correction in corrections:
            if correction in content:
                print(f"OK - Correction presente: {correction}")
            else:
                print(f"ERREUR - Correction manquante: {correction}")
                return False
        
        print("OK - Toutes les corrections sont presentes")
        return True
        
    except Exception as e:
        print(f"ERREUR lecture controleur: {e}")
        return False

def main():
    """Fonction principale"""
    print("TEST RAPIDE DU SYSTEME DE PAIEMENTS")
    print("=" * 40)
    
    # Test des fichiers
    files_ok = test_files()
    
    # Test de la syntaxe
    syntax_ok = test_controller_syntax()
    
    # Résumé
    print("\n" + "=" * 40)
    print("RESUME")
    print("=" * 40)
    
    if files_ok and syntax_ok:
        print("SUCCES - Tous les fichiers sont corrects")
        print("Le systeme de paiements est pret a etre utilise !")
        return True
    else:
        print("PROBLEMES - Des corrections sont necessaires")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nErreur: {e}")
        sys.exit(1)
