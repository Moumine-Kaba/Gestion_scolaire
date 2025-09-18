#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour adapter les requêtes SQL SQLite vers SQL Server
"""

import os
import re
import glob

def adapt_sqlite_to_sqlserver():
    """Adapte les requêtes SQL SQLite vers SQL Server"""
    
    # Trouver tous les fichiers Python dans src/modules/auth/models/
    python_files = glob.glob('src/modules/auth/models/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Adapter les requêtes SQL
            sql_replacements = [
                # Remplacer CREATE TABLE IF NOT EXISTS par CREATE TABLE
                (r'CREATE TABLE IF NOT EXISTS', 'CREATE TABLE'),
                
                # Remplacer INTEGER PRIMARY KEY AUTOINCREMENT par IDENTITY(1,1)
                (r'INTEGER PRIMARY KEY AUTOINCREMENT', 'INT IDENTITY(1,1) PRIMARY KEY'),
                
                # Remplacer TEXT par NVARCHAR(255)
                (r'\bTEXT\b', 'NVARCHAR(255)'),
                
                # Remplacer TIMESTAMP DEFAULT CURRENT_TIMESTAMP par DATETIME DEFAULT GETDATE()
                (r'TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT GETDATE()'),
                
                # Remplacer sqlite_master par INFORMATION_SCHEMA.TABLES
                (r'sqlite_master', 'INFORMATION_SCHEMA.TABLES'),
                
                # Remplacer type='table' par TABLE_TYPE='BASE TABLE'
                (r"type='table'", "TABLE_TYPE='BASE TABLE'"),
                
                # Remplacer name par TABLE_NAME
                (r'\bname\b', 'TABLE_NAME'),
            ]
            
            for pattern, replacement in sql_replacements:
                content = re.sub(pattern, replacement, content)
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ SQL adapté: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    return fixed_files

if __name__ == "__main__":
    print("🔧 Adaptation des requêtes SQL SQLite vers SQL Server...")
    
    fixed_files = adapt_sqlite_to_sqlserver()
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés")
    print("🎉 Adaptation SQL terminée !")




