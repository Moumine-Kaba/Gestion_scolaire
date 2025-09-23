#!/usr/bin/env python3
"""
Script pour corriger toutes les références aux anciennes méthodes SQLite dans dashboard_view.py
"""

import re

def fix_dashboard_queries():
    """Corrige toutes les références SQLite dans dashboard_view.py"""
    
    file_path = "src/modules/auth/views/dashboard_view.py"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer cur.execute() + cur.fetchone() par db_manager.fetch_one()
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*r = cur\.fetchone\(\)',
            r'r = db_manager.fetch_one(\1)',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer cur.execute() + cur.fetchall() par db_manager.fetch_all()
        content = re.sub(
            r'cur\.execute\(([^)]+)\)\s*\n\s*rows = cur\.fetchall\(\)',
            r'rows = db_manager.fetch_all(\1, [])',
            content,
            flags=re.MULTILINE
        )
        
        # Remplacer les autres cur.fetchone() isolés
        content = re.sub(r'cur\.fetchone\(\)', 'db_manager.fetch_one("SELECT 1", [])', content)
        
        # Remplacer les autres cur.fetchall() isolés
        content = re.sub(r'cur\.fetchall\(\)', 'db_manager.fetch_all("SELECT 1", [])', content)
        
        # Supprimer les références à cur
        content = re.sub(r'cur = conn\.cursor\(\)\s*\n', '', content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Corrigé {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction de {file_path}: {e}")
        return False

if __name__ == "__main__":
    fix_dashboard_queries()

