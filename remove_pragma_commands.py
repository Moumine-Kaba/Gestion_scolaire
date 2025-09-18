#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour supprimer toutes les commandes PRAGMA SQLite
"""

import os
import re
import glob

def remove_pragma_commands():
    """Supprime toutes les commandes PRAGMA SQLite des fichiers Python"""
    
    # Trouver tous les fichiers Python dans src/
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Supprimer les commandes PRAGMA
            pragma_patterns = [
                r'conn\.execute\("PRAGMA[^"]*"\)\s*;?\s*\n?',
                r'cur\.execute\("PRAGMA[^"]*"\)\s*;?\s*\n?',
                r'cursor\.execute\("PRAGMA[^"]*"\)\s*;?\s*\n?',
                r'PRAGMA\s+\w+\s*=\s*\w+\s*;?\s*\n?',
                r'conn\.execute\(text\("PRAGMA[^"]*"\)\)\s*;?\s*\n?',
                r'cur\.execute\(text\("PRAGMA[^"]*"\)\)\s*;?\s*\n?',
            ]
            
            for pattern in pragma_patterns:
                content = re.sub(pattern, '', content, flags=re.MULTILINE | re.IGNORECASE)
            
            # Nettoyer les lignes vides multiples
            content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ PRAGMA supprimé: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    return fixed_files

if __name__ == "__main__":
    print("🔧 Suppression des commandes PRAGMA SQLite...")
    
    fixed_files = remove_pragma_commands()
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés")
    print("🎉 Suppression des commandes PRAGMA terminée !")



