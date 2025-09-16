#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour examiner la structure de la table eleves
"""

import sqlite3

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def examine_eleves_table():
    """Examine la structure de la table eleves"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🔍 Structure de la table eleves:")
        print("=" * 50)
        
        # Obtenir la structure de la table
        cursor.execute("PRAGMA table_info(eleves)")
        columns = cursor.fetchall()
        
        print("Colonnes:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'} - {'PK' if col[5] else ''}")
        
        # Vérifier s'il y a des données
        cursor.execute("SELECT COUNT(*) FROM eleves")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre d'élèves existants: {count}")
        
        if count > 0:
            # Afficher quelques exemples
            cursor.execute("SELECT * FROM eleves LIMIT 3")
            examples = cursor.fetchall()
            print("\nExemples de données:")
            for example in examples:
                print(f"  {example}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    examine_eleves_table()
