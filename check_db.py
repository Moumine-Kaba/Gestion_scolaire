#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure de la base de données
"""

import sqlite3
import os

def check_database():
    """Vérifie la structure de la base de données"""
    db_path = os.path.join("database", "edumanager.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Lister toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tables disponibles: {tables}")
            
            # Vérifier les tables importantes
            important_tables = ['professeurs', 'classes', 'matieres', 'salles']
            
            for table in important_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table '{table}': {count} enregistrements")
                    
                    # Afficher quelques exemples
                    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                    rows = cursor.fetchall()
                    if rows:
                        print(f"   Exemples: {rows}")
                else:
                    print(f"❌ Table '{table}' manquante")
            
            # Vérifier les tables de cours
            cours_tables = ['enseignement', 'emplois_du_temps']
            for table in cours_tables:
                if table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table '{table}': {count} enregistrements")
                else:
                    print(f"❌ Table '{table}' manquante")
                    
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_database()
