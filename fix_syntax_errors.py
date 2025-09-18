#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les erreurs de syntaxe créées par le script précédent
"""

import os
import re
import glob

def fix_syntax_errors():
    """Corrige les erreurs de syntaxe dans les fichiers Python"""
    
    # Trouver tous les fichiers Python dans src/
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Corriger les erreurs de syntaxe spécifiques
            fixes = [
                # Corriger les lignes avec plusieurs commentaires répétés
                (r'# # # sqlite3\.Row.*?# Remplacé par SQL Server.*?# Remplacé par SQL Server.*?# Remplacé par SQL Server', 
                 '# sqlite3.Row  # Remplacé par SQL Server'),
                
                # Corriger les lignes avec des parenthèses mal fermées
                (r'get_db_connection\(\), timeout=\d+, check_same_thread=False\)', 
                 'get_db_connection()'),
                
                # Corriger les lignes avec des assignations mal formées
                (r'conn\.row_factory = #.*?sqlite3\.Row.*?# Remplacé par SQL Server', 
                 '# conn.row_factory = sqlite3.Row  # Remplacé par SQL Server'),
                
                # Corriger les lignes avec des commentaires multiples
                (r'# # #.*?# Remplacé par SQL Server.*?# Remplacé par SQL Server', 
                 '# Remplacé par SQL Server'),
                
                # Corriger les lignes vides avec des commentaires
                (r'^\s*# # #.*?$\n', ''),
                
                # Corriger les assignations incomplètes
                (r'(\w+)\.row_factory = #.*?$\n', r'# \1.row_factory = sqlite3.Row  # Remplacé par SQL Server\n'),
            ]
            
            # Appliquer les corrections
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            # Nettoyer les lignes vides multiples
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Syntaxe corrigée: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    return fixed_files

def fix_specific_files():
    """Corrige des fichiers spécifiques avec des problèmes connus"""
    
    specific_fixes = {
        'src/utils/db_utils.py': [
            (r'conn\.row_factory = #.*?sqlite3\.Row.*?# Remplacé par SQL Server.*?# Remplacé par SQL Server.*?# Remplacé par SQL Server', 
             '# conn.row_factory = sqlite3.Row  # Remplacé par SQL Server'),
        ],
        'src/modules/auth/views/login_view.py': [
            (r'conn = get_db_connection\(\), timeout=\d+, check_same_thread=False\)', 
             'conn = get_db_connection()'),
        ]
    }
    
    for file_path, fixes in specific_fixes.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                original_content = content
                
                for pattern, replacement in fixes:
                    content = re.sub(pattern, replacement, content)
                
                if content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fichier spécifique corrigé: {file_path}")
                    
            except Exception as e:
                print(f"❌ Erreur fichier spécifique {file_path}: {e}")

if __name__ == "__main__":
    print("🔧 Correction des erreurs de syntaxe...")
    
    # Corriger tous les fichiers
    fixed_files = fix_syntax_errors()
    
    # Corriger des fichiers spécifiques
    fix_specific_files()
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés")
    print("🎉 Correction des erreurs de syntaxe terminée !")




