#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger toutes les références SQLite dans l'application
et les remplacer par SQL Server
"""

import os
import re
import glob

def fix_sqlite_references():
    """Corrige toutes les références SQLite dans les fichiers Python"""
    
    # Patterns à remplacer
    replacements = [
        # Import sqlite3
        (r'import sqlite3', '# import sqlite3  # Remplacé par SQL Server'),
        
        # sqlite3.connect
        (r'sqlite3\.connect\([^)]+\)', 'get_db_connection()'),
        
        # sqlite3.Row
        (r'sqlite3\.Row', '# sqlite3.Row  # Remplacé par SQL Server'),
        
        # sqlite3.Error
        (r'sqlite3\.Error', 'Exception'),
        
        # row_factory
        (r'\.row_factory\s*=\s*sqlite3\.Row', '# .row_factory = sqlite3.Row  # Remplacé par SQL Server'),
        
        # cursor.execute avec sqlite3
        (r'cursor\.execute\(', 'cursor.execute('),
        
        # fetchall, fetchone avec sqlite3
        (r'cursor\.fetchall\(\)', 'cursor.fetchall()'),
        (r'cursor\.fetchone\(\)', 'cursor.fetchone()'),
    ]
    
    # Ajouter l'import get_db_connection si nécessaire
    import_pattern = r'from database\.connection import get_db_connection'
    
    # Trouver tous les fichiers Python dans src/
    python_files = glob.glob('src/**/*.py', recursive=True)
    
    fixed_files = []
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Appliquer les remplacements
            for pattern, replacement in replacements:
                content = re.sub(pattern, replacement, content)
            
            # Ajouter l'import si le fichier utilise get_db_connection mais ne l'importe pas
            if 'get_db_connection()' in content and import_pattern not in content:
                # Trouver la première ligne d'import
                lines = content.split('\n')
                import_line = -1
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_line = i
                        break
                
                if import_line >= 0:
                    lines.insert(import_line, 'from database.connection import get_db_connection')
                    content = '\n'.join(lines)
                else:
                    # Ajouter au début du fichier
                    content = 'from database.connection import get_db_connection\n' + content
            
            # Écrire le fichier modifié si des changements ont été faits
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed_files.append(file_path)
                print(f"✅ Corrigé: {file_path}")
                
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    print(f"\n🎯 {len(fixed_files)} fichiers corrigés:")
    for file_path in fixed_files:
        print(f"  - {file_path}")
    
    return fixed_files

def fix_specific_controllers():
    """Corrige des contrôleurs spécifiques qui ont des problèmes connus"""
    
    controllers_to_fix = [
        'src/modules/academic/teachers/controllers/professeur_controller.py',
        'src/modules/academic/students/controllers/eleve_controller.py',
        'src/modules/academic/classes/controllers/classe_controller.py',
        'src/modules/academic/subjects/controllers/matiere_controller.py',
        'src/modules/academic/grades/controllers/notes_controller.py',
        'src/modules/administrative/maintenance/controllers/salle_controller.py',
    ]
    
    for controller_path in controllers_to_fix:
        if os.path.exists(controller_path):
            try:
                with open(controller_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remplacer les patterns spécifiques
                patterns = [
                    (r'import sqlite3', '# import sqlite3  # Remplacé par SQL Server'),
                    (r'sqlite3\.connect\([^)]+\)', 'get_db_connection()'),
                    (r'sqlite3\.Error', 'Exception'),
                    (r'\.row_factory\s*=\s*sqlite3\.Row', '# .row_factory = sqlite3.Row  # Remplacé par SQL Server'),
                ]
                
                original_content = content
                for pattern, replacement in patterns:
                    content = re.sub(pattern, replacement, content)
                
                # Ajouter l'import si nécessaire
                if 'get_db_connection()' in content and 'from database.connection import get_db_connection' not in content:
                    content = 'from database.connection import get_db_connection\n' + content
                
                if content != original_content:
                    with open(controller_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Contrôleur corrigé: {controller_path}")
                    
            except Exception as e:
                print(f"❌ Erreur contrôleur {controller_path}: {e}")

if __name__ == "__main__":
    print("🔧 Correction des références SQLite vers SQL Server...")
    
    # Corriger tous les fichiers
    fixed_files = fix_sqlite_references()
    
    # Corriger des contrôleurs spécifiques
    fix_specific_controllers()
    
    print("\n🎉 Correction terminée !")
    print("📝 Vérifiez que l'application fonctionne maintenant avec SQL Server.")

