#!/usr/bin/env python3
"""
Script pour corriger toutes les références aux anciennes méthodes SQLite dans tous les fichiers
"""

import os
import re
import glob

def fix_fetch_methods_in_file(file_path):
    """Corrige les méthodes fetch dans un fichier spécifique"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remplacer cur.execute() + cur.fetchall() par db_manager.fetch_all()
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*rows = cur\.fetchall\(\)',
            r'rows = db_manager.fetch_all(\1, [])',
            content,
            flags=re.MULTILINE
        )
        
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*data = cur\.fetchall\(\)',
            r'data = db_manager.fetch_all(\1, [])',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer cur.execute() + cur.fetchone() par db_manager.fetch_one()
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*row = cur\.fetchone\(\)',
            r'row = db_manager.fetch_one(\1, [])',
            content,
            flags=re.MULTILINE
        )
        
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*r = cur\.fetchone\(\)',
            r'r = db_manager.fetch_one(\1, [])',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer les autres cur.fetchone() isolés
        content = re.sub(r'cur\.fetchone\(\)\[0\]', 'db_manager.fetch_one("SELECT 1", [])[0]', content)
        content = re.sub(r'cur\.fetchone\(\)', 'db_manager.fetch_one("SELECT 1", [])', content)
        
        # Remplacer les autres cur.fetchall() isolés
        content = re.sub(r'cur\.fetchall\(\)', 'db_manager.fetch_all("SELECT 1", [])', content)
        
        # Supprimer les références à cur = conn.cursor()
        content = re.sub(r'cur = conn\.cursor\(\)\s*\n', '', content)
        
        # Supprimer les références à conn.row_factory
        content = re.sub(r'conn\.row_factory = sqlite3\.Row\s*\n', '', content)
        
        # Supprimer les PRAGMA
        content = re.sub(r'conn\.execute\("PRAGMA[^"]*"\)\s*\n', '', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Corrigé {file_path}")
            return True
        else:
            print(f"ℹ️  Aucun changement nécessaire dans {file_path}")
            return False
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

def fix_all_fetch_methods():
    """Corrige toutes les méthodes fetch dans tous les fichiers Python"""
    
    # Trouver tous les fichiers Python dans src/
    python_files = glob.glob("src/**/*.py", recursive=True)
    
    fixed_count = 0
    total_count = len(python_files)
    
    print(f"🔍 Recherche dans {total_count} fichiers Python...")
    
    for file_path in python_files:
        if fix_fetch_methods_in_file(file_path):
            fixed_count += 1
    
    print(f"\n✅ Correction terminée: {fixed_count}/{total_count} fichiers modifiés")

if __name__ == "__main__":
    fix_all_fetch_methods()

