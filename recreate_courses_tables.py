#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour recréer les tables de cours avec la bonne structure
"""

import sqlite3
import os

def recreate_tables():
    """Recrée les tables avec la bonne structure"""
    db_path = os.path.join("database", "edumanager.db")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Supprimer les anciennes tables
            cursor.execute("DROP TABLE IF EXISTS enseignement")
            cursor.execute("DROP TABLE IF EXISTS emplois_du_temps")
            print("🗑️ Anciennes tables supprimées")
            
            # Créer la table enseignement avec la bonne structure
            cursor.execute("""
                CREATE TABLE enseignement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    salle_id INTEGER,
                    jours_cours TEXT DEFAULT 'Lundi',
                    duree_cours INTEGER DEFAULT 60,
                    statut TEXT DEFAULT 'Actif',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table enseignement créée")
            
            # Créer la table emplois_du_temps avec la bonne structure
            cursor.execute("""
                CREATE TABLE emplois_du_temps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jour TEXT NOT NULL,
                    heure TEXT NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER,
                    salle_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table emplois_du_temps créée")
            
            # Ajouter des données de test
            print("📚 Ajout de données de test...")
            
            # Données pour enseignement
            enseignements = [
                (1, 1, 1, 1, 'Lundi', 60, 'Actif'),
                (2, 2, 2, 2, 'Mardi', 45, 'Actif'),
                (3, 3, 3, 3, 'Mercredi', 90, 'Actif'),
                (4, 4, 4, 4, 'Jeudi', 60, 'Actif'),
                (5, 5, 5, 5, 'Vendredi', 45, 'Actif'),
                (1, 6, 6, 6, 'Lundi', 60, 'Actif'),
                (2, 7, 7, 7, 'Mardi', 90, 'Actif'),
                (3, 8, 8, 8, 'Mercredi', 45, 'Actif'),
                (4, 9, 1, 9, 'Jeudi', 60, 'Actif'),
                (5, 10, 2, 10, 'Vendredi', 45, 'Actif'),
                (1, 11, 3, 11, 'Lundi', 90, 'Actif'),
                (2, 12, 4, 12, 'Mardi', 60, 'Actif'),
                (3, 13, 5, 1, 'Mercredi', 45, 'Actif'),
                (4, 14, 6, 2, 'Jeudi', 60, 'Actif'),
                (5, 15, 7, 3, 'Vendredi', 90, 'Actif'),
                (1, 16, 8, 4, 'Lundi', 45, 'Actif'),
                (2, 17, 1, 5, 'Mardi', 60, 'Actif'),
                (3, 18, 2, 6, 'Mercredi', 90, 'Actif'),
                (4, 19, 3, 7, 'Jeudi', 45, 'Actif'),
                (5, 20, 4, 8, 'Vendredi', 60, 'Actif'),
            ]
            
            for prof_id, classe_id, matiere_id, salle_id, jour, duree, statut in enseignements:
                cursor.execute("""
                    INSERT INTO enseignement 
                    (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (prof_id, classe_id, matiere_id, salle_id, jour, duree, statut))
            
            # Données pour emplois_du_temps
            emplois = [
                ('Lundi', '08:00', 1, 1, 1, 1),
                ('Lundi', '09:00', 2, 2, 2, 2),
                ('Mardi', '10:00', 3, 3, 3, 3),
                ('Mardi', '11:00', 4, 4, 4, 4),
                ('Mercredi', '14:00', 5, 5, 5, 5),
                ('Mercredi', '15:00', 6, 1, 6, 6),
                ('Jeudi', '16:00', 7, 2, 7, 7),
                ('Jeudi', '17:00', 8, 3, 8, 8),
                ('Vendredi', '08:00', 1, 4, 9, 9),
                ('Vendredi', '09:00', 2, 5, 10, 10),
                ('Lundi', '10:00', 3, 1, 11, 11),
                ('Lundi', '11:00', 4, 2, 12, 12),
                ('Mardi', '14:00', 5, 3, 13, 13),
                ('Mardi', '15:00', 6, 4, 14, 14),
                ('Mercredi', '16:00', 7, 5, 15, 15),
                ('Mercredi', '17:00', 8, 1, 16, 16),
                ('Jeudi', '08:00', 1, 2, 17, 17),
                ('Jeudi', '09:00', 2, 3, 18, 18),
                ('Vendredi', '10:00', 3, 4, 19, 19),
                ('Vendredi', '11:00', 4, 5, 20, 20),
            ]
            
            for jour, heure, matiere_id, prof_id, classe_id, salle_id in emplois:
                cursor.execute("""
                    INSERT INTO emplois_du_temps 
                    (jour, heure, matiere_id, professeur_id, classe_id, salle_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (jour, heure, matiere_id, prof_id, classe_id, salle_id))
            
            conn.commit()
            
            # Vérifier les résultats
            cursor.execute("SELECT COUNT(*) FROM enseignement")
            enseignement_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM emplois_du_temps")
            emploi_count = cursor.fetchone()[0]
            
            print(f"🎉 Tables recréées avec succès!")
            print(f"📊 Enseignements: {enseignement_count}")
            print(f"📊 Emplois du temps: {emploi_count}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    recreate_tables()
