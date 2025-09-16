#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier la structure de la base de données et corriger les problèmes
"""

import sqlite3
import os

def check_database_structure():
    """Vérifie la structure de la base de données"""
    db_path = os.path.join("database", "edumanager.db")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Lister toutes les tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"📋 Tables disponibles: {tables}")
            
            # Vérifier la structure de chaque table importante
            important_tables = ['cours', 'professeurs', 'classes', 'matieres', 'salles']
            
            for table in important_tables:
                if table in tables:
                    cursor.execute(f"PRAGMA table_info({table})")
                    columns = cursor.fetchall()
                    print(f"\n📊 Structure de la table '{table}':")
                    for col in columns:
                        print(f"   - {col[1]} ({col[2]})")
                    
                    # Compter les enregistrements
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📈 Nombre d'enregistrements: {count}")
                else:
                    print(f"\n❌ Table '{table}' manquante")
            
            # Tester une requête simple sur la table cours
            if 'cours' in tables:
                print(f"\n🧪 Test de requête sur la table cours:")
                cursor.execute("SELECT * FROM cours LIMIT 3")
                rows = cursor.fetchall()
                for i, row in enumerate(rows):
                    print(f"   Ligne {i+1}: {row}")
                    
    except Exception as e:
        print(f"❌ Erreur: {e}")

def create_missing_tables():
    """Crée les tables manquantes avec des données de test"""
    db_path = os.path.join("database", "edumanager.db")
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Créer la table professeurs si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS professeurs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    email TEXT,
                    telephone TEXT,
                    specialite TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer la table classes si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    niveau TEXT,
                    effectif INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer la table matieres si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS matieres (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    code TEXT,
                    coefficient REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer la table salles si elle n'existe pas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS salles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    capacite INTEGER DEFAULT 30,
                    equipements TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Ajouter des données de test
            print("📚 Ajout de données de test...")
            
            # Professeurs de test
            professeurs_data = [
                ('Dupont', 'Jean', 'jean.dupont@email.com', '0123456789', 'Mathématiques'),
                ('Martin', 'Marie', 'marie.martin@email.com', '0123456788', 'Français'),
                ('Bernard', 'Pierre', 'pierre.bernard@email.com', '0123456787', 'Sciences'),
                ('Durand', 'Sophie', 'sophie.durand@email.com', '0123456786', 'Histoire'),
                ('Moreau', 'Paul', 'paul.moreau@email.com', '0123456785', 'Géographie'),
            ]
            
            for nom, prenom, email, tel, spec in professeurs_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO professeurs (nom, prenom, email, telephone, specialite)
                    VALUES (?, ?, ?, ?, ?)
                """, (nom, prenom, email, tel, spec))
            
            # Classes de test
            classes_data = [
                ('6ème A', '6ème', 25),
                ('5ème B', '5ème', 28),
                ('4ème C', '4ème', 30),
                ('3ème D', '3ème', 27),
                ('2nde E', '2nde', 32),
                ('1ère F', '1ère', 29),
                ('Terminale G', 'Terminale', 26),
                ('CP H', 'CP', 24),
                ('CE1 I', 'CE1', 22),
                ('CE2 J', 'CE2', 23),
            ]
            
            for nom, niveau, effectif in classes_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO classes (nom, niveau, effectif)
                    VALUES (?, ?, ?)
                """, (nom, niveau, effectif))
            
            # Matières de test
            matieres_data = [
                ('Mathématiques', 'MATH', 4.0),
                ('Français', 'FR', 4.0),
                ('Sciences Physiques', 'SPC', 3.0),
                ('Histoire-Géographie', 'HG', 3.0),
                ('Anglais', 'ANG', 2.5),
                ('Sciences de la Vie et de la Terre', 'SVT', 2.0),
                ('Éducation Physique et Sportive', 'EPS', 2.0),
                ('Arts Plastiques', 'ART', 1.0),
            ]
            
            for nom, code, coef in matieres_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO matieres (nom, code, coefficient)
                    VALUES (?, ?, ?)
                """, (nom, code, coef))
            
            # Salles de test
            salles_data = [
                ('Salle 101', 30, 'Tableau, Projecteur'),
                ('Salle 102', 25, 'Tableau'),
                ('Salle 103', 35, 'Tableau, Ordinateur'),
                ('Salle 201', 28, 'Tableau, Projecteur'),
                ('Salle 202', 32, 'Tableau'),
                ('Salle 203', 26, 'Tableau, Ordinateur'),
                ('Laboratoire 1', 20, 'Paillasses, Matériel scientifique'),
                ('Laboratoire 2', 18, 'Paillasses, Ordinateurs'),
                ('Salle informatique', 24, 'Ordinateurs, Projecteur'),
                ('Salle de sport', 40, 'Matériel sportif'),
            ]
            
            for nom, capacite, equipements in salles_data:
                cursor.execute("""
                    INSERT OR IGNORE INTO salles (nom, capacite, equipements)
                    VALUES (?, ?, ?)
                """, (nom, capacite, equipements))
            
            conn.commit()
            print("✅ Tables et données de test créées avec succès!")
            
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")

if __name__ == "__main__":
    print("🔍 Vérification de la structure de la base de données...")
    check_database_structure()
    
    print("\n" + "="*50)
    print("🛠️ Création des tables manquantes...")
    create_missing_tables()
    
    print("\n" + "="*50)
    print("🔍 Vérification finale...")
    check_database_structure()
