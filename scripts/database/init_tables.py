#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation des Tables Manquantes
EduManager+ - Gestion Scolaire
"""

import os
import sqlite3

def init_missing_tables():
    """Initialise toutes les tables manquantes de l'application"""
    print("🗄️ Initialisation des Tables Manquantes")
    print("=" * 50)
    
    try:
        db_path = "database/edumanager.db"
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Table des bulletins
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bulletins (
                    id_bulletin INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_eleve INTEGER NOT NULL,
                    id_classe INTEGER NOT NULL,
                    periode TEXT NOT NULL,
                    annee_scolaire TEXT NOT NULL,
                    moyenne_generale REAL,
                    appreciation TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_eleve) REFERENCES eleves (id_eleve),
                    FOREIGN KEY (id_classe) REFERENCES classes (id_classe)
                )
            ''')
            print("✅ Table bulletins créée")
            
            # Table des notes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id_note INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_eleve INTEGER NOT NULL,
                    id_matiere INTEGER NOT NULL,
                    id_professeur INTEGER NOT NULL,
                    note REAL NOT NULL,
                    coefficient REAL DEFAULT 1.0,
                    type_evaluation TEXT DEFAULT 'Contrôle',
                    date_evaluation DATE NOT NULL,
                    commentaire TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_eleve) REFERENCES eleves (id_eleve),
                    FOREIGN KEY (id_matiere) REFERENCES matieres (id_matiere),
                    FOREIGN KEY (id_professeur) REFERENCES professeurs (id_professeur)
                )
            ''')
            print("✅ Table notes créée")
            
            # Table des présences
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS presences (
                    id_presence INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_eleve INTEGER NOT NULL,
                    id_classe INTEGER NOT NULL,
                    id_matiere INTEGER NOT NULL,
                    date_presence DATE NOT NULL,
                    statut TEXT NOT NULL CHECK (statut IN ('Présent', 'Absent', 'Retard', 'Excusé')),
                    motif_absence TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_eleve) REFERENCES eleves (id_eleve),
                    FOREIGN KEY (id_classe) REFERENCES classes (id_classe),
                    FOREIGN KEY (id_matiere) REFERENCES matieres (id_matiere)
                )
            ''')
            print("✅ Table presences créée")
            
            # Table des élèves
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS eleves (
                    id_eleve INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricule TEXT UNIQUE NOT NULL,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    date_naissance DATE,
                    genre TEXT CHECK (genre IN ('M', 'F')),
                    adresse TEXT,
                    telephone TEXT,
                    email TEXT,
                    id_classe INTEGER,
                    id_parent INTEGER,
                    statut TEXT DEFAULT 'Actif',
                    date_inscription DATE DEFAULT CURRENT_DATE,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_classe) REFERENCES classes (id_classe),
                    FOREIGN KEY (id_parent) REFERENCES parents (id_parent)
                )
            ''')
            print("✅ Table eleves créée")
            
            # Table des professeurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS professeurs (
                    id_professeur INTEGER PRIMARY KEY AUTOINCREMENT,
                    matricule TEXT UNIQUE NOT NULL,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    date_naissance DATE,
                    genre TEXT CHECK (genre IN ('M', 'F')),
                    adresse TEXT,
                    telephone TEXT,
                    email TEXT NOT NULL,
                    specialite TEXT,
                    date_embauche DATE DEFAULT CURRENT_DATE,
                    statut TEXT DEFAULT 'Actif',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Table professeurs créée")
            
            # Table des classes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classes (
                    id_classe INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_classe TEXT NOT NULL,
                    niveau TEXT NOT NULL,
                    effectif INTEGER DEFAULT 0,
                    id_professeur_principal INTEGER,
                    annee_scolaire TEXT NOT NULL,
                    statut TEXT DEFAULT 'Active',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_professeur_principal) REFERENCES professeurs (id_professeur)
                )
            ''')
            print("✅ Table classes créée")
            
            # Table des matières
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matieres (
                    id_matiere INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_matiere TEXT NOT NULL,
                    code_matiere TEXT UNIQUE NOT NULL,
                    description TEXT,
                    coefficient REAL DEFAULT 1.0,
                    id_professeur INTEGER,
                    statut TEXT DEFAULT 'Active',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_professeur) REFERENCES professeurs (id_professeur)
                )
            ''')
            print("✅ Table matieres créée")
            
            # Table des parents
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS parents (
                    id_parent INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    prenom TEXT NOT NULL,
                    telephone TEXT NOT NULL,
                    email TEXT,
                    adresse TEXT,
                    profession TEXT,
                    statut TEXT DEFAULT 'Actif',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Table parents créée")
            
            # Table des salles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS salles (
                    id_salle INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_salle TEXT NOT NULL,
                    capacite INTEGER DEFAULT 30,
                    type_salle TEXT DEFAULT 'Salle de classe',
                    equipements TEXT,
                    statut TEXT DEFAULT 'Disponible',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            print("✅ Table salles créée")
            
            # Table des enseignements (liaison prof-matiere-classe)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enseignements (
                    id_enseignement INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_professeur INTEGER NOT NULL,
                    id_matiere INTEGER NOT NULL,
                    id_classe INTEGER NOT NULL,
                    heures_semaine INTEGER DEFAULT 4,
                    annee_scolaire TEXT NOT NULL,
                    statut TEXT DEFAULT 'Actif',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_professeur) REFERENCES professeurs (id_professeur),
                    FOREIGN KEY (id_matiere) REFERENCES matieres (id_matiere),
                    FOREIGN KEY (id_classe) REFERENCES classes (id_classe),
                    UNIQUE(id_professeur, id_matiere, id_classe, annee_scolaire)
                )
            ''')
            print("✅ Table enseignements créée")
            
            # Table des emplois du temps
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS emplois_temps (
                    id_emploi INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_classe INTEGER NOT NULL,
                    id_matiere INTEGER NOT NULL,
                    id_professeur INTEGER NOT NULL,
                    id_salle INTEGER NOT NULL,
                    jour_semaine TEXT NOT NULL CHECK (jour_semaine IN ('Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi')),
                    heure_debut TEXT NOT NULL,
                    heure_fin TEXT NOT NULL,
                    annee_scolaire TEXT NOT NULL,
                    statut TEXT DEFAULT 'Actif',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_classe) REFERENCES classes (id_classe),
                    FOREIGN KEY (id_matiere) REFERENCES matieres (id_matiere),
                    FOREIGN KEY (id_professeur) REFERENCES professeurs (id_professeur),
                    FOREIGN KEY (id_salle) REFERENCES salles (id_salle)
                )
            ''')
            print("✅ Table emplois_temps créée")
            
            # Table des paiements
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS paiements (
                    id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_eleve INTEGER NOT NULL,
                    montant REAL NOT NULL,
                    type_paiement TEXT NOT NULL,
                    date_paiement DATE NOT NULL,
                    mode_paiement TEXT DEFAULT 'Espèces',
                    reference TEXT,
                    statut TEXT DEFAULT 'Payé',
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_eleve) REFERENCES eleves (id_eleve)
                )
            ''')
            print("✅ Table paiements créée")
            
            conn.commit()
            print("\n🎉 Toutes les tables ont été créées avec succès !")
            
            # Vérifier les tables existantes
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print(f"\n📊 Tables disponibles ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur création des tables: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Script d'Initialisation des Tables")
    print("=" * 40)
    
    success = init_missing_tables()
    
    if success:
        print("\n🎉 Initialisation des tables terminée avec succès !")
        print("✅ L'application peut maintenant fonctionner correctement")
    else:
        print("\n❌ Échec de l'initialisation des tables")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
