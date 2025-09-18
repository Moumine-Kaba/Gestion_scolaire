#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la répartition des élèves
"""

import sqlite3

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def check_students_distribution():
    """Vérifie la répartition des élèves"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("📊 Répartition des élèves")
        print("=" * 50)
        
        # Total des élèves
        cursor.execute("SELECT COUNT(*) FROM eleves")
        total = cursor.fetchone()[0]
        print(f"🎓 Total des élèves: {total}")
        
        # Par niveau
        cursor.execute("""
            SELECT c.niveau, COUNT(e.id_eleve) as nb_eleves
            FROM classes c 
            LEFT JOIN eleves e ON c.id_classe = e.id_classe 
            GROUP BY c.niveau 
            ORDER BY c.niveau
        """)
        par_niveau = cursor.fetchall()
        
        print(f"\n📚 Répartition par niveau:")
        for niveau, count in par_niveau:
            print(f"   {niveau}: {count} élèves")
        
        # Par classes
        cursor.execute("""
            SELECT c.nom_classe, c.niveau, COUNT(e.id_eleve) as nb_eleves
            FROM classes c 
            LEFT JOIN eleves e ON c.id_classe = e.id_classe 
            GROUP BY c.id_classe, c.nom_classe, c.niveau
            ORDER BY c.niveau, c.nom_classe
        """)
        par_classe = cursor.fetchall()
        
        print(f"\n🏫 Répartition par classes:")
        for nom, niveau, count in par_classe:
            print(f"   {nom} ({niveau}): {count} élèves")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_students_distribution()
