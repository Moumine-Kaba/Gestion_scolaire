#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter 20 cours de test dans la base de données
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import random

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), '.')
sys.path.insert(0, root_path)

def connect_db():
    """Connexion à la base de données"""
    db_path = os.path.join(root_path, "database", "edumanager.db")
    return sqlite3.connect(db_path)

def get_random_ids():
    """Récupère des IDs aléatoires des tables de référence"""
    with connect_db() as conn:
        cursor = conn.cursor()
        
        # Récupérer les IDs des professeurs
        cursor.execute("SELECT id FROM professeurs LIMIT 10")
        prof_ids = [row[0] for row in cursor.fetchall()]
        
        # Récupérer les IDs des classes
        cursor.execute("SELECT id FROM classes LIMIT 15")
        classe_ids = [row[0] for row in cursor.fetchall()]
        
        # Récupérer les IDs des matières
        cursor.execute("SELECT id FROM matieres LIMIT 8")
        matiere_ids = [row[0] for row in cursor.fetchall()]
        
        # Récupérer les IDs des salles
        cursor.execute("SELECT id FROM salles LIMIT 12")
        salle_ids = [row[0] for row in cursor.fetchall()]
        
        return prof_ids, classe_ids, matiere_ids, salle_ids

def add_test_courses():
    """Ajoute 20 cours de test"""
    try:
        prof_ids, classe_ids, matiere_ids, salle_ids = get_random_ids()
        
        if not prof_ids or not classe_ids or not matiere_ids:
            print("❌ Données de référence insuffisantes. Veuillez d'abord ajouter des professeurs, classes et matières.")
            return
        
        jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        heures_cours = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        durees = [45, 60, 90]
        statuts = ['Actif', 'Suspendu', 'Terminé']
        
        with connect_db() as conn:
            cursor = conn.cursor()
            
            # Vérifier si la table existe et créer si nécessaire
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS enseignement (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    salle_id INTEGER,
                    jours_cours TEXT DEFAULT 'Lundi',
                    duree_cours INTEGER DEFAULT 60,
                    statut TEXT DEFAULT 'Actif',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (professeur_id) REFERENCES professeurs(id),
                    FOREIGN KEY (classe_id) REFERENCES classes(id),
                    FOREIGN KEY (matiere_id) REFERENCES matieres(id),
                    FOREIGN KEY (salle_id) REFERENCES salles(id)
                )
            """)
            
            # Ajouter 20 cours de test
            for i in range(20):
                professeur_id = random.choice(prof_ids)
                classe_id = random.choice(classe_ids)
                matiere_id = random.choice(matiere_ids)
                salle_id = random.choice(salle_ids) if salle_ids else None
                jour = random.choice(jours_semaine)
                duree = random.choice(durees)
                statut = random.choice(statuts)
                
                cursor.execute("""
                    INSERT INTO enseignement 
                    (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (professeur_id, classe_id, matiere_id, salle_id, jour, duree, statut))
                
                print(f"✅ Cours {i+1}/20 ajouté: Prof {professeur_id}, Classe {classe_id}, Matière {matiere_id}")
            
            conn.commit()
            print(f"\n🎉 {20} cours de test ajoutés avec succès!")
            
            # Afficher un résumé
            cursor.execute("SELECT COUNT(*) FROM enseignement")
            total = cursor.fetchone()[0]
            print(f"📊 Total des cours dans la base: {total}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des cours: {e}")

def add_test_emplois():
    """Ajoute 20 emplois du temps de test"""
    try:
        prof_ids, classe_ids, matiere_ids, salle_ids = get_random_ids()
        
        if not prof_ids or not classe_ids or not matiere_ids:
            print("❌ Données de référence insuffisantes.")
            return
        
        jours_semaine = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi']
        heures_cours = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00', '17:00']
        
        with connect_db() as conn:
            cursor = conn.cursor()
            
            # Vérifier si la table existe et créer si nécessaire
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS emplois_du_temps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jour TEXT NOT NULL,
                    heure TEXT NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER,
                    salle_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (matiere_id) REFERENCES matieres(id),
                    FOREIGN KEY (professeur_id) REFERENCES professeurs(id),
                    FOREIGN KEY (classe_id) REFERENCES classes(id),
                    FOREIGN KEY (salle_id) REFERENCES salles(id)
                )
            """)
            
            # Ajouter 20 emplois de test
            for i in range(20):
                professeur_id = random.choice(prof_ids)
                classe_id = random.choice(classe_ids)
                matiere_id = random.choice(matiere_ids)
                salle_id = random.choice(salle_ids) if salle_ids else None
                jour = random.choice(jours_semaine)
                heure = random.choice(heures_cours)
                
                cursor.execute("""
                    INSERT INTO emplois_du_temps 
                    (jour, heure, matiere_id, professeur_id, classe_id, salle_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (jour, heure, matiere_id, professeur_id, classe_id, salle_id))
                
                print(f"✅ Emploi {i+1}/20 ajouté: {jour} {heure}, Prof {professeur_id}, Classe {classe_id}")
            
            conn.commit()
            print(f"\n🎉 {20} emplois du temps de test ajoutés avec succès!")
            
            # Afficher un résumé
            cursor.execute("SELECT COUNT(*) FROM emplois_du_temps")
            total = cursor.fetchone()[0]
            print(f"📊 Total des emplois dans la base: {total}")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des emplois: {e}")

if __name__ == "__main__":
    print("🚀 Ajout de 20 cours de test...")
    print("=" * 50)
    
    # Ajouter des cours (enseignements)
    print("\n📚 Ajout des enseignements:")
    add_test_courses()
    
    print("\n" + "=" * 50)
    
    # Ajouter des emplois du temps
    print("\n📅 Ajout des emplois du temps:")
    add_test_emplois()
    
    print("\n✅ Script terminé!")
