#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les méthodes de base de données dans les modèles RBAC
"""

import os
import re
import glob

def fix_database_methods():
    """Corrige les méthodes de base de données pour SQL Server"""
    
    # Trouver tous les fichiers Python dans src/modules/auth/models/
    python_files = glob.glob('src/modules/auth/models/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Remplacer les méthodes SQLite par SQL Server
            replacements = [
                # Remplacer cursor.fetchall() par db_manager.fetch_all()
                (r'cursor\.fetchall\(\)', 'db_manager.fetch_all(query)'),
                
                # Remplacer cursor.fetchone() par db_manager.fetch_one()
                (r'cursor\.fetchone\(\)', 'db_manager.fetch_one(query)'),
                
                # Remplacer cursor.execute() par db_manager.execute()
                (r'cursor\.execute\(([^)]+)\)', r'db_manager.execute(\1)'),
                
                # Remplacer conn.execute() par db_manager.execute()
                (r'conn\.execute\(([^)]+)\)', r'db_manager.execute(\1)'),
                
                # Adapter les requêtes SQL
                (r'CREATE TABLE IF NOT EXISTS', 'CREATE TABLE'),
                (r'INTEGER PRIMARY KEY AUTOINCREMENT', 'INT IDENTITY(1,1) PRIMARY KEY'),
                (r'\bTEXT\b', 'NVARCHAR(255)'),
                (r'TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT GETDATE()'),
                (r'sqlite_master', 'INFORMATION_SCHEMA.TABLES'),
                (r"type='table'", "TABLE_TYPE='BASE TABLE'"),
                (r'\bname\b', 'TABLE_NAME'),
            ]
            
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # Ajouter l'import db_manager si nécessaire
            if 'db_manager.fetch_all' in content and 'from database.connection import get_db_connection' not in content:
                content = 'from database.connection import get_db_connection\n' + content
            
            # Remplacer db_manager par get_db_connection() dans les fonctions
            content = re.sub(r'db_manager\.', 'get_db_connection().', content)
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Méthodes DB corrigées: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    return fixed_files

if __name__ == "__main__":
    print("🔧 Correction des méthodes de base de données...")
    
    fixed_files = fix_database_methods()
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés")
    print("🎉 Correction des méthodes DB terminée !")



