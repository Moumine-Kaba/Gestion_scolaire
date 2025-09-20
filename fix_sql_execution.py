#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les problèmes de requêtes SQL dans les modèles RBAC
"""

import os
import re
import glob

def fix_sql_execution():
    """Corrige les problèmes d'exécution des requêtes SQL"""
    
    # Trouver tous les fichiers Python dans src/modules/auth/models/
    python_files = glob.glob('src/modules/auth/models/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Corriger les problèmes spécifiques
            fixes = [
                # Remplacer les requêtes CREATE TABLE IF NOT EXISTS par des vérifications d'existence
                (r'CREATE TABLE IF NOT EXISTS', 'CREATE TABLE'),
                
                # Remplacer INTEGER PRIMARY KEY AUTOINCREMENT par IDENTITY(1,1)
                (r'INTEGER PRIMARY KEY AUTOINCREMENT', 'INT IDENTITY(1,1) PRIMARY KEY'),
                
                # Remplacer TEXT par NVARCHAR(255)
                (r'\bTEXT\b', 'NVARCHAR(255)'),
                
                # Remplacer TIMESTAMP par DATETIME
                (r'TIMESTAMP DEFAULT CURRENT_TIMESTAMP', 'DATETIME DEFAULT GETDATE()'),
                
                # Remplacer sqlite_master par INFORMATION_SCHEMA.TABLES
                (r'sqlite_master', 'INFORMATION_SCHEMA.TABLES'),
                (r"type='table'", "TABLE_TYPE='BASE TABLE'"),
                (r'\bname\b', 'TABLE_NAME'),
                
                # Corriger les méthodes de base de données
                (r'cursor\.fetchall\(\)', 'results'),
                (r'cursor\.fetchone\(\)', 'result'),
                (r'cursor\.execute\(([^)]+)\)', r'db_manager.execute(\1)'),
                (r'conn\.execute\(([^)]+)\)', r'db_manager.execute(\1)'),
                
                # Ajouter des vérifications d'existence de table
                (r'CREATE TABLE (\w+)', r'IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = \'\1\') BEGIN CREATE TABLE \1'),
            ]
            
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content)
            
            # Ajouter l'import nécessaire
            if 'db_manager.execute' in content and 'from database.connection import get_db_connection' not in content:
                content = 'from database.connection import get_db_connection\n' + content
            
            # Remplacer db_manager par get_db_connection()
            content = re.sub(r'db_manager\.', 'get_db_connection().', content)
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ SQL exécution corrigée: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    return fixed_files

if __name__ == "__main__":
    print("🔧 Correction des problèmes d'exécution SQL...")
    
    fixed_files = fix_sql_execution()
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés")
    print("🎉 Correction SQL terminée !")





