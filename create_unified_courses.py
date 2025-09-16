#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer une seule table unifiée pour les cours
"""

import sqlite3
import os

def create_unified_courses_table():
    """Crée une seule table unifiée pour tous les cours"""
    db_path = os.path.join("database", "edumanager.db")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Supprimer les anciennes tables
            cursor.execute("DROP TABLE IF EXISTS enseignement")
            cursor.execute("DROP TABLE IF EXISTS emplois_du_temps")
            print("🗑️ Anciennes tables supprimées")
            
            # Créer la table unifiée "cours"
            cursor.execute("""
                CREATE TABLE cours (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL DEFAULT 'enseignement',
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    salle_id INTEGER,
                    jour TEXT DEFAULT 'Lundi',
                    heure TEXT DEFAULT '08:00',
                    duree INTEGER DEFAULT 60,
                    statut TEXT DEFAULT 'Actif',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("✅ Table unifiée 'cours' créée")
            
            # Ajouter des données de test
            print("📚 Ajout de données de test...")
            
            # Données pour les cours (mix enseignement + emploi du temps)
            cours_data = [
                # Enseignements (type='enseignement')
                ('enseignement', 1, 1, 1, 1, 'Lundi', '08:00', 60, 'Actif', 'Cours de Mathématiques'),
                ('enseignement', 2, 2, 2, 2, 'Mardi', '09:00', 45, 'Actif', 'Cours de Français'),
                ('enseignement', 3, 3, 3, 3, 'Mercredi', '10:00', 90, 'Actif', 'Cours de Sciences'),
                ('enseignement', 4, 4, 4, 4, 'Jeudi', '11:00', 60, 'Actif', 'Cours d\'Histoire'),
                ('enseignement', 5, 5, 5, 5, 'Vendredi', '14:00', 45, 'Actif', 'Cours de Géographie'),
                ('enseignement', 1, 6, 6, 6, 'Lundi', '15:00', 60, 'Actif', 'Cours d\'Anglais'),
                ('enseignement', 2, 7, 7, 7, 'Mardi', '16:00', 90, 'Actif', 'Cours de Physique'),
                ('enseignement', 3, 8, 8, 8, 'Mercredi', '17:00', 45, 'Actif', 'Cours de Chimie'),
                ('enseignement', 4, 9, 1, 9, 'Jeudi', '08:00', 60, 'Actif', 'Cours de Biologie'),
                ('enseignement', 5, 10, 2, 10, 'Vendredi', '09:00', 45, 'Actif', 'Cours d\'Économie'),
                
                # Emplois du temps (type='emploi')
                ('emploi', 1, 1, 1, 1, 'Lundi', '08:00', 60, 'Actif', 'Mathématiques - 1ère'),
                ('emploi', 2, 2, 2, 2, 'Mardi', '09:00', 45, 'Actif', 'Français - 2nde'),
                ('emploi', 3, 3, 3, 3, 'Mercredi', '10:00', 90, 'Actif', 'Sciences - Terminale'),
                ('emploi', 4, 4, 4, 4, 'Jeudi', '11:00', 60, 'Actif', 'Histoire - 3ème'),
                ('emploi', 5, 5, 5, 5, 'Vendredi', '14:00', 45, 'Actif', 'Géographie - 4ème'),
                ('emploi', 1, 6, 6, 6, 'Lundi', '15:00', 60, 'Actif', 'Anglais - 5ème'),
                ('emploi', 2, 7, 7, 7, 'Mardi', '16:00', 90, 'Actif', 'Physique - 6ème'),
                ('emploi', 3, 8, 8, 8, 'Mercredi', '17:00', 45, 'Actif', 'Chimie - 7ème'),
                ('emploi', 4, 9, 1, 9, 'Jeudi', '08:00', 60, 'Actif', 'Biologie - 8ème'),
                ('emploi', 5, 10, 2, 10, 'Vendredi', '09:00', 45, 'Actif', 'Économie - 9ème'),
            ]
            
            for type_cours, prof_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description in cours_data:
                cursor.execute("""
                    INSERT INTO cours 
                    (type, professeur_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (type_cours, prof_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description))
            
            conn.commit()
            
            # Vérifier les résultats
            cursor.execute("SELECT COUNT(*) FROM cours")
            total_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cours WHERE type='enseignement'")
            enseignement_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM cours WHERE type='emploi'")
            emploi_count = cursor.fetchone()[0]
            
            print(f"🎉 Table unifiée créée avec succès!")
            print(f"📊 Total des cours: {total_count}")
            print(f"📊 Enseignements: {enseignement_count}")
            print(f"📊 Emplois du temps: {emploi_count}")
            
            # Afficher quelques exemples
            cursor.execute("SELECT * FROM cours LIMIT 5")
            examples = cursor.fetchall()
            print(f"📝 Exemples de cours:")
            for example in examples:
                print(f"   {example}")
                
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    create_unified_courses_table()
