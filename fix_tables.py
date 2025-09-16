#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier et corriger la structure des tables de cours
"""

import sqlite3
import os

def check_and_fix_tables():
    """Vérifie et corrige la structure des tables"""
    db_path = os.path.join("database", "edumanager.db")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Vérifier la structure de la table enseignement
            cursor.execute("PRAGMA table_info(enseignement)")
            enseignement_columns = [column[1] for column in cursor.fetchall()]
            print(f"📋 Colonnes enseignement: {enseignement_columns}")
            
            # Vérifier la structure de la table emplois_du_temps
            cursor.execute("PRAGMA table_info(emplois_du_temps)")
            emplois_columns = [column[1] for column in cursor.fetchall()]
            print(f"📋 Colonnes emplois_du_temps: {emplois_columns}")
            
            # Ajouter les colonnes manquantes à enseignement
            if 'jours_cours' not in enseignement_columns:
                cursor.execute("ALTER TABLE enseignement ADD COLUMN jours_cours TEXT DEFAULT 'Lundi'")
                print("✅ Colonne jours_cours ajoutée à enseignement")
            
            if 'duree_cours' not in enseignement_columns:
                cursor.execute("ALTER TABLE enseignement ADD COLUMN duree_cours INTEGER DEFAULT 60")
                print("✅ Colonne duree_cours ajoutée à enseignement")
            
            if 'statut' not in enseignement_columns:
                cursor.execute("ALTER TABLE enseignement ADD COLUMN statut TEXT DEFAULT 'Actif'")
                print("✅ Colonne statut ajoutée à enseignement")
            
            # Ajouter les colonnes manquantes à emplois_du_temps
            if 'jour' not in emplois_columns:
                cursor.execute("ALTER TABLE emplois_du_temps ADD COLUMN jour TEXT DEFAULT 'Lundi'")
                print("✅ Colonne jour ajoutée à emplois_du_temps")
            
            if 'heure' not in emplois_columns:
                cursor.execute("ALTER TABLE emplois_du_temps ADD COLUMN heure TEXT DEFAULT '08:00'")
                print("✅ Colonne heure ajoutée à emplois_du_temps")
            
            conn.commit()
            
            # Vérifier le contenu des tables
            cursor.execute("SELECT COUNT(*) FROM enseignement")
            enseignement_count = cursor.fetchone()[0]
            print(f"📊 Enseignements: {enseignement_count}")
            
            cursor.execute("SELECT COUNT(*) FROM emplois_du_temps")
            emploi_count = cursor.fetchone()[0]
            print(f"📊 Emplois du temps: {emploi_count}")
            
            # Afficher quelques exemples
            if enseignement_count > 0:
                cursor.execute("SELECT * FROM enseignement LIMIT 3")
                examples = cursor.fetchall()
                print(f"📝 Exemples enseignement: {examples}")
            
            if emploi_count > 0:
                cursor.execute("SELECT * FROM emplois_du_temps LIMIT 3")
                examples = cursor.fetchall()
                print(f"📝 Exemples emplois: {examples}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_and_fix_tables()
