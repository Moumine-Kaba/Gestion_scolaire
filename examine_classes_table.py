#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour examiner la structure de la table classes
"""

import sqlite3

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def examine_classes_table():
    """Examine la structure de la table classes"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔍 Structure de la table classes:")
        print("=" * 50)
        
        # Obtenir la structure de la table
        cursor.execute("PRAGMA table_info(classes)")
        columns = cursor.fetchall()
        
        print("Colonnes:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'PK' if col[5] else ''}")
        
        # Vérifier s'il y a des données
        cursor.execute("SELECT COUNT(*) FROM classes")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre de classes existantes: {count}")
        
        if count > 0:
            # Afficher quelques exemples
            cursor.execute("SELECT * FROM classes LIMIT 5")
            examples = cursor.fetchall()
            print("\nExemples de données:")
            for example in examples:
                print(f"  {example}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    examine_classes_table()
