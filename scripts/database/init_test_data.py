#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation des Données de Test
EduManager+ - Gestion Scolaire
"""

import os
import sqlite3
from datetime import date, datetime

def init_test_data():
    """Initialise des données de test dans les tables"""
    print("📊 Initialisation des Données de Test")
    print("=" * 50)
    
    try:
        db_path = "database/edumanager.db"
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Insérer des données de test dans les tables
            
            # 1. Professeurs
            cursor.execute('''
                INSERT OR IGNORE INTO professeurs (matricule, nom, prenom, email, specialite, statut)
                VALUES 
                ('PROF001', 'Dupont', 'Jean', 'jean.dupont@ecole.com', 'Mathématiques', 'Actif'),
                ('PROF002', 'Martin', 'Marie', 'marie.martin@ecole.com', 'Français', 'Actif'),
                ('PROF003', 'Bernard', 'Pierre', 'pierre.bernard@ecole.com', 'Histoire-Géo', 'Actif'),
                ('PROF004', 'Petit', 'Sophie', 'sophie.petit@ecole.com', 'Sciences', 'Actif'),
                ('PROF005', 'Robert', 'Michel', 'michel.robert@ecole.com', 'Anglais', 'Actif')
            ''')
            print("✅ Professeurs de test ajoutés")
            
            # 2. Classes
            cursor.execute('''
                INSERT OR IGNORE INTO classes (nom_classe, niveau, effectif, annee_scolaire, statut)
                VALUES 
                ('6ème A', '6ème', 25, '2024-2025', 'Active'),
                ('6ème B', '6ème', 23, '2024-2025', 'Active'),
                ('5ème A', '5ème', 26, '2024-2025', 'Active'),
                ('5ème B', '5ème', 24, '2024-2025', 'Active'),
                ('4ème A', '4ème', 25, '2024-2025', 'Active'),
                ('3ème A', '3ème', 27, '2024-2025', 'Active')
            ''')
            print("✅ Classes de test ajoutées")
            
            # 3. Matières
            cursor.execute('''
                INSERT OR IGNORE INTO matieres (nom_matiere, code_matiere, description, coefficient, statut)
                VALUES 
                ('Mathématiques', 'MATH', 'Mathématiques générales', 4.0, 'Active'),
                ('Français', 'FRAN', 'Langue française et littérature', 4.0, 'Active'),
                ('Histoire-Géographie', 'HIST', 'Histoire et géographie', 3.0, 'Active'),
                ('Sciences', 'SCIE', 'Sciences de la vie et de la terre', 3.0, 'Active'),
                ('Anglais', 'ANGL', 'Langue anglaise', 2.0, 'Active'),
                ('Éducation physique', 'EPS', 'Sport et activités physiques', 2.0, 'Active'),
                ('Arts plastiques', 'ARTS', 'Expression artistique', 1.0, 'Active'),
                ('Technologie', 'TECH', 'Sciences et techniques', 1.0, 'Active')
            ''')
            print("✅ Matières de test ajoutées")
            
            # 4. Parents
            cursor.execute('''
                INSERT OR IGNORE INTO parents (nom, prenom, telephone, email, profession, statut)
                VALUES 
                ('Durand', 'Paul', '0123456789', 'paul.durand@email.com', 'Ingénieur', 'Actif'),
                ('Leroy', 'Anne', '0987654321', 'anne.leroy@email.com', 'Médecin', 'Actif'),
                ('Moreau', 'François', '0555666777', 'francois.moreau@email.com', 'Avocat', 'Actif'),
                ('Simon', 'Isabelle', '0111222333', 'isabelle.simon@email.com', 'Enseignante', 'Actif'),
                ('Michel', 'Thomas', '0444555666', 'thomas.michel@email.com', 'Architecte', 'Actif')
            ''')
            print("✅ Parents de test ajoutés")
            
            # 5. Élèves
            cursor.execute('''
                INSERT OR IGNORE INTO eleves (matricule, nom, prenom, date_naissance, genre, id_classe, id_parent, statut)
                VALUES 
                ('ELE001', 'Durand', 'Lucas', '2012-03-15', 'M', 1, 1, 'Actif'),
                ('ELE002', 'Leroy', 'Emma', '2012-07-22', 'F', 1, 2, 'Actif'),
                ('ELE003', 'Moreau', 'Hugo', '2012-01-10', 'M', 1, 3, 'Actif'),
                ('ELE004', 'Simon', 'Léa', '2012-11-05', 'F', 2, 4, 'Actif'),
                ('ELE005', 'Michel', 'Nathan', '2012-05-18', 'M', 2, 5, 'Actif'),
                ('ELE006', 'Dubois', 'Chloé', '2011-09-12', 'F', 3, 1, 'Actif'),
                ('ELE007', 'Lefevre', 'Antoine', '2011-12-03', 'M', 3, 2, 'Actif'),
                ('ELE008', 'Garcia', 'Jade', '2011-04-25', 'F', 4, 3, 'Actif')
            ''')
            print("✅ Élèves de test ajoutés")
            
            # 6. Salles
            cursor.execute('''
                INSERT OR IGNORE INTO salles (nom_salle, capacite, type_salle, equipements, statut)
                VALUES 
                ('Salle 101', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle 102', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle 103', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle 104', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle 105', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle 106', 30, 'Salle de classe', 'Tableau, vidéoprojecteur', 'Disponible'),
                ('Salle informatique', 20, 'Salle informatique', 'Ordinateurs, vidéoprojecteur', 'Disponible'),
                ('Salle de sciences', 25, 'Laboratoire', 'Matériel scientifique, vidéoprojecteur', 'Disponible'),
                ('Gymnase', 100, 'Salle de sport', 'Équipements sportifs', 'Disponible')
            ''')
            print("✅ Salles de test ajoutées")
            
            # 7. Enseignements (liaison prof-matiere-classe)
            cursor.execute('''
                INSERT OR IGNORE INTO enseignements (id_professeur, id_matiere, id_classe, heures_semaine, annee_scolaire, statut)
                VALUES 
                (1, 1, 1, 4, '2024-2025', 'Actif'),  -- Prof Dupont (Maths) -> 6ème A
                (2, 2, 1, 4, '2024-2025', 'Actif'),  -- Prof Martin (Français) -> 6ème A
                (3, 3, 1, 3, '2024-2025', 'Actif'),  -- Prof Bernard (Histoire) -> 6ème A
                (4, 4, 1, 3, '2024-2025', 'Actif'),  -- Prof Petit (Sciences) -> 6ème A
                (5, 5, 1, 2, '2024-2025', 'Actif'),  -- Prof Robert (Anglais) -> 6ème A
                (1, 1, 2, 4, '2024-2025', 'Actif'),  -- Prof Dupont (Maths) -> 6ème B
                (2, 2, 2, 4, '2024-2025', 'Actif'),  -- Prof Martin (Français) -> 6ème B
                (3, 3, 2, 3, '2024-2025', 'Actif'),  -- Prof Bernard (Histoire) -> 6ème B
                (4, 4, 2, 3, '2024-2025', 'Actif'),  -- Prof Petit (Sciences) -> 6ème B
                (5, 5, 2, 2, '2024-2025', 'Actif')   -- Prof Robert (Anglais) -> 6ème B
            ''')
            print("✅ Enseignements de test ajoutés")
            
            # 8. Notes de test
            cursor.execute('''
                INSERT OR IGNORE INTO notes (id_eleve, id_matiere, id_professeur, note, coefficient, type_evaluation, date_evaluation)
                VALUES 
                (1, 1, 1, 15.5, 1.0, 'Contrôle', '2024-09-15'),
                (1, 1, 1, 17.0, 1.0, 'Devoir', '2024-09-20'),
                (1, 2, 2, 14.0, 1.0, 'Contrôle', '2024-09-16'),
                (1, 3, 3, 16.5, 1.0, 'Contrôle', '2024-09-17'),
                (2, 1, 1, 18.0, 1.0, 'Contrôle', '2024-09-15'),
                (2, 2, 2, 16.5, 1.0, 'Contrôle', '2024-09-16'),
                (2, 3, 3, 15.0, 1.0, 'Contrôle', '2024-09-17'),
                (3, 1, 1, 13.5, 1.0, 'Contrôle', '2024-09-15'),
                (3, 2, 2, 17.5, 1.0, 'Contrôle', '2024-09-16'),
                (3, 4, 4, 16.0, 1.0, 'Contrôle', '2024-09-18')
            ''')
            print("✅ Notes de test ajoutées")
            
            # 9. Présences de test
            cursor.execute('''
                INSERT OR IGNORE INTO presences (id_eleve, id_classe, id_matiere, date_presence, statut)
                VALUES 
                (1, 1, 1, '2024-09-15', 'Présent'),
                (1, 1, 2, '2024-09-16', 'Présent'),
                (1, 1, 3, '2024-09-17', 'Présent'),
                (2, 1, 1, '2024-09-15', 'Présent'),
                (2, 1, 2, '2024-09-16', 'Présent'),
                (2, 1, 3, '2024-09-17', 'Absent'),
                (3, 1, 1, '2024-09-15', 'Présent'),
                (3, 1, 2, '2024-09-16', 'Retard'),
                (3, 1, 4, '2024-09-18', 'Présent')
            ''')
            print("✅ Présences de test ajoutées")
            
            # 10. Emplois du temps de test
            cursor.execute('''
                INSERT OR IGNORE INTO emplois_temps (id_classe, id_matiere, id_professeur, id_salle, jour_semaine, heure_debut, heure_fin, annee_scolaire, statut)
                VALUES 
                (1, 1, 1, 1, 'Lundi', '08:00', '09:00', '2024-2025', 'Actif'),
                (1, 2, 2, 1, 'Lundi', '09:00', '10:00', '2024-2025', 'Actif'),
                (1, 3, 3, 1, 'Lundi', '10:00', '11:00', '2024-2025', 'Actif'),
                (1, 4, 4, 8, 'Lundi', '14:00', '15:00', '2024-2025', 'Actif'),
                (1, 5, 5, 1, 'Mardi', '08:00', '09:00', '2024-2025', 'Actif'),
                (1, 1, 1, 1, 'Mardi', '09:00', '10:00', '2024-2025', 'Actif'),
                (1, 2, 2, 1, 'Mardi', '10:00', '11:00', '2024-2025', 'Actif'),
                (1, 3, 3, 1, 'Mardi', '14:00', '15:00', '2024-2025', 'Actif')
            ''')
            print("✅ Emplois du temps de test ajoutés")
            
            # 11. Paiements de test
            cursor.execute('''
                INSERT OR IGNORE INTO paiements (id_eleve, montant, type_paiement, date_paiement, mode_paiement, statut)
                VALUES 
                (1, 150.00, 'Frais de scolarité', '2024-09-01', 'Virement', 'Payé'),
                (2, 150.00, 'Frais de scolarité', '2024-09-01', 'Chèque', 'Payé'),
                (3, 150.00, 'Frais de scolarité', '2024-09-01', 'Espèces', 'Payé'),
                (1, 25.00, 'Frais de cantine', '2024-09-15', 'Espèces', 'Payé'),
                (2, 25.00, 'Frais de cantine', '2024-09-15', 'Espèces', 'Payé'),
                (3, 25.00, 'Frais de cantine', '2024-09-15', 'Espèces', 'Payé')
            ''')
            print("✅ Paiements de test ajoutés")
            
            conn.commit()
            print("\n🎉 Toutes les données de test ont été ajoutées avec succès !")
            
            # Vérifier les données
            print("\n📊 Vérification des données:")
            cursor.execute("SELECT COUNT(*) FROM professeurs")
            prof_count = cursor.fetchone()[0]
            print(f"  - Professeurs: {prof_count}")
            
            cursor.execute("SELECT COUNT(*) FROM eleves")
            eleve_count = cursor.fetchone()[0]
            print(f"  - Élèves: {eleve_count}")
            
            cursor.execute("SELECT COUNT(*) FROM classes")
            classe_count = cursor.fetchone()[0]
            print(f"  - Classes: {classe_count}")
            
            cursor.execute("SELECT COUNT(*) FROM notes")
            note_count = cursor.fetchone()[0]
            print(f"  - Notes: {note_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur ajout des données de test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Script d'Initialisation des Données de Test")
    print("=" * 50)
    
    success = init_test_data()
    
    if success:
        print("\n🎉 Initialisation des données de test terminée avec succès !")
        print("✅ L'application dispose maintenant de données pour les tests")
    else:
        print("\n❌ Échec de l'initialisation des données de test")
    
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
