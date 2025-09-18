#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vérification et Nettoyage SQLite
===============================

Script pour vérifier ce qui n'a pas été migré et supprimer les traces SQLite.
"""

import sqlite3
import pyodbc
import os
import shutil

def check_migration_status():
    """Vérifie l'état de la migration"""
    
    print("🔍 Vérification de l'État de la Migration")
    print("=" * 50)
    
    try:
        # Connexion SQLite
        sqlite_conn = sqlite3.connect('database/edumanager.db')
        sqlite_cursor = sqlite_conn.cursor()
        
        # Connexion SQL Server
        sqlserver_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        sqlserver_cursor = sqlserver_conn.cursor()
        
        # Obtenir toutes les tables SQLite
        sqlite_cursor.execute('SELECT name FROM sqlite_master WHERE type="table"')
        sqlite_tables = [row[0] for row in sqlite_cursor.fetchall()]
        
        # Obtenir toutes les tables SQL Server
        sqlserver_cursor.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = "BASE TABLE"')
        sqlserver_tables = [row[0] for row in sqlserver_cursor.fetchall()]
        
        print(f"📊 SQLite: {len(sqlite_tables)} tables")
        print(f"📊 SQL Server: {len(sqlserver_tables)} tables")
        
        # Tables manquantes dans SQL Server
        missing_tables = []
        for table in sqlite_tables:
            if table not in sqlserver_tables:
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n❌ Tables manquantes dans SQL Server ({len(missing_tables)}):")
            for table in missing_tables:
                try:
                    sqlite_cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    count = sqlite_cursor.fetchone()[0]
                    print(f"  - {table}: {count} enregistrements")
                except:
                    print(f"  - {table}: erreur de comptage")
        else:
            print("\n✅ Toutes les tables SQLite sont présentes dans SQL Server!")
        
        # Vérifier les données manquantes
        print(f"\n🔍 Vérification des Données par Table:")
        tables_with_data_missing = []
        
        for table in sqlite_tables:
            if table in sqlserver_tables:
                try:
                    sqlite_cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    sqlite_count = sqlite_cursor.fetchone()[0]
                    
                    sqlserver_cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    sqlserver_count = sqlserver_cursor.fetchone()[0]
                    
                    if sqlite_count != sqlserver_count:
                        tables_with_data_missing.append((table, sqlite_count, sqlserver_count))
                        print(f"  ⚠️ {table}: SQLite={sqlite_count}, SQL Server={sqlserver_count}")
                    else:
                        print(f"  ✅ {table}: {sqlite_count} enregistrements")
                except Exception as e:
                    print(f"  ❌ {table}: erreur - {e}")
        
        if tables_with_data_missing:
            print(f"\n⚠️ Tables avec données manquantes ({len(tables_with_data_missing)}):")
            for table, sqlite_count, sqlserver_count in tables_with_data_missing:
                print(f"  - {table}: {sqlite_count - sqlserver_count} enregistrements manquants")
        else:
            print(f"\n✅ Toutes les données sont correctement migrées!")
        
        sqlite_conn.close()
        sqlserver_conn.close()
        
        return len(missing_tables) == 0 and len(tables_with_data_missing) == 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def clean_sqlite_traces():
    """Supprime toutes les traces de SQLite"""
    
    print("\n🧹 Nettoyage des Traces SQLite")
    print("=" * 50)
    
    # Fichiers SQLite à supprimer
    sqlite_files = [
        'database/edumanager.db',
        'database/edumanager.db-shm',
        'database/edumanager.db-wal',
        'database/edumanager_backup_20250907_115434.db',
        'database/edumanager_backup_20250907_115440.db',
        'database/edumanager_backup_20250907_115456.db',
        'database/edumanager_rbac_backup_20250907_115901.db',
        'database/edumanager_rbac_backup_20250907_115906.db'
    ]
    
    # Scripts de migration à supprimer
    migration_scripts = [
        'migrate_to_sqlserver.py',
        'migrate_data_simple.py',
        'migrate_direct_pyodbc.py',
        'migrate_rbac_tables.py',
        'create_rbac_tables.py',
        'recreate_sqlserver_tables.py',
        'migrate_final.py',
        'check_sqlite_data.py',
        'test_sqlserver_connection.py',
        'test_final_migration.py',
        'configure_for_ssms.py',
        'test_ssms_compatibility.py'
    ]
    
    # Guides à supprimer
    guides = [
        'MIGRATION_SQLSERVER_GUIDE.md',
        'GUIDE_SSMS.md'
    ]
    
    deleted_files = []
    
    # Supprimer les fichiers SQLite
    print("🗑️ Suppression des fichiers SQLite...")
    for file_path in sqlite_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                deleted_files.append(file_path)
                print(f"  ✅ Supprimé: {file_path}")
            except Exception as e:
                print(f"  ❌ Erreur suppression {file_path}: {e}")
        else:
            print(f"  ⚪ Non trouvé: {file_path}")
    
    # Supprimer les scripts de migration
    print("\n🗑️ Suppression des scripts de migration...")
    for script in migration_scripts:
        if os.path.exists(script):
            try:
                os.remove(script)
                deleted_files.append(script)
                print(f"  ✅ Supprimé: {script}")
            except Exception as e:
                print(f"  ❌ Erreur suppression {script}: {e}")
        else:
            print(f"  ⚪ Non trouvé: {script}")
    
    # Supprimer les guides
    print("\n🗑️ Suppression des guides de migration...")
    for guide in guides:
        if os.path.exists(guide):
            try:
                os.remove(guide)
                deleted_files.append(guide)
                print(f"  ✅ Supprimé: {guide}")
            except Exception as e:
                print(f"  ❌ Erreur suppression {guide}: {e}")
        else:
            print(f"  ⚪ Non trouvé: {guide}")
    
    # Supprimer le fichier requirements SQL Server
    if os.path.exists('requirements_sqlserver.txt'):
        try:
            os.remove('requirements_sqlserver.txt')
            deleted_files.append('requirements_sqlserver.txt')
            print(f"  ✅ Supprimé: requirements_sqlserver.txt")
        except Exception as e:
            print(f"  ❌ Erreur suppression requirements_sqlserver.txt: {e}")
    
    print(f"\n📊 Résumé du nettoyage:")
    print(f"  - {len(deleted_files)} fichiers supprimés")
    print(f"  - Migration SQLite → SQL Server terminée")
    print(f"  - Application maintenant 100% SQL Server")
    
    return len(deleted_files)

def update_config_for_sqlserver():
    """Met à jour la configuration pour utiliser uniquement SQL Server"""
    
    print("\n⚙️ Mise à jour de la Configuration")
    print("=" * 50)
    
    # Mettre à jour src/core/config.py
    config_file = 'src/core/config.py'
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remplacer la configuration par défaut pour SQL Server
            new_content = content.replace(
                'type: str = "sqlite"',
                'type: str = "sqlserver"'
            )
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"  ✅ Configuration mise à jour: {config_file}")
            
        except Exception as e:
            print(f"  ❌ Erreur mise à jour config: {e}")
    
    print("  ✅ Application configurée pour SQL Server uniquement")

if __name__ == "__main__":
    print("🚀 Vérification et Nettoyage Post-Migration")
    print("=" * 60)
    
    # Vérifier l'état de la migration
    migration_complete = check_migration_status()
    
    if migration_complete:
        print("\n✅ Migration complète détectée!")
        
        # Demander confirmation avant suppression
        print("\n⚠️ ATTENTION: Cette action va supprimer définitivement:")
        print("  - Tous les fichiers SQLite")
        print("  - Tous les scripts de migration")
        print("  - Tous les guides de migration")
        print("  - Les sauvegardes SQLite")
        
        response = input("\n❓ Voulez-vous continuer? (oui/non): ").lower()
        
        if response in ['oui', 'o', 'yes', 'y']:
            # Nettoyer les traces SQLite
            deleted_count = clean_sqlite_traces()
            
            # Mettre à jour la configuration
            update_config_for_sqlserver()
            
            print(f"\n🎉 Nettoyage terminé!")
            print(f"✅ {deleted_count} fichiers supprimés")
            print(f"✅ Application maintenant 100% SQL Server")
            print(f"✅ Configuration mise à jour")
            print(f"\n🚀 Votre application est prête avec SQL Server!")
        else:
            print("\n❌ Nettoyage annulé par l'utilisateurs")
    else:
        print("\n⚠️ Migration incomplète détectée!")
        print("Veuillez terminer la migration avant de nettoyer les traces SQLite")

