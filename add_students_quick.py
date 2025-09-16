#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplifié pour ajouter 500 élèves rapidement
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def add_students_quick():
    """Ajoute rapidement 500 élèves"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🎓 Ajout rapide de 500 élèves")
        print("=" * 40)
        
        # Prénoms et noms simples
        prenoms = ["Jean", "Marie", "Pierre", "Sophie", "Paul", "Julie", "Jacques", "Camille", "Michel", "Sarah"]
        noms = ["Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent"]
        
        # Récupérer les classes
        cursor.execute("SELECT id_classe, nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        classes = cursor.fetchall()
        
        print(f"📚 {len(classes)} classes trouvées")
        
        # Répartition: ~26 élèves par classe (500/19 ≈ 26)
        eleves_par_classe = 26
        eleve_count = 0
        
        for id_classe, nom_classe, niveau in classes:
            print(f"   Ajout dans {nom_classe}...")
            
            for i in range(eleves_par_classe):
                prenom = random.choice(prenoms)
                nom = random.choice(noms)
                
                # Données simplifiées
                cursor.execute("""
                    INSERT INTO eleves (
                        prenom, nom, date_naissance, genre, email, telephone, 
                        adresse, statut, date_inscription, id_classe
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"{prenom}{i}",  # Éviter les doublons
                    nom,
                    "2010-01-01",  # Date fixe
                    random.choice(["M", "F"]),
                    f"{prenom.lower()}{i}@email.com",
                    f"77{random.randint(1000000, 9999999)}",
                    "Dakar, Sénégal",
                    "actif",
                    "2024-09-01 08:00:00",
                    id_classe
                ))
                eleve_count += 1
        
        # Valider
        conn.commit()
        
        # Vérifier
        cursor.execute("SELECT COUNT(*) FROM eleves")
        total = cursor.fetchone()[0]
        
        print(f"\n✅ {total} élèves ajoutés avec succès!")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_students_quick()
