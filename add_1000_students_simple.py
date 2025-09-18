#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simplifié pour ajouter 1000 élèves - Évite les imports circulaires
=======================================================================
"""

import random
import sys
import os
import pyodbc
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Configuration SQL Server directe
SQLSERVER_CONFIG = {
    'host': '.',
    'name': 'EduManager',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': True
}

# Données réalistes pour générer les élèves
PRENOMS_MASCULINS = [
    "Ahmed", "Mohamed", "Ali", "Omar", "Hassan", "Youssef", "Karim", "Said", "Rachid", "Mustapha",
    "Abdel", "Ibrahim", "Abdellah", "Hamza", "Anas", "Yassine", "Reda", "Soufiane", "Mehdi", "Adil",
    "Bilal", "Ayoub", "Zakaria", "Imad", "Nabil", "Fouad", "Tarik", "Walid", "Samir", "Nassim",
    "Younes", "Hicham", "Amine", "Salah", "Farid", "Khalil", "Mounir", "Hakim", "Nadir", "Riad",
    "Malik", "Yacine", "Sami", "Houssam", "Badr", "Achraf", "Yahya", "Zine", "Aymen", "Marouane"
]

PRENOMS_FEMININS = [
    "Fatima", "Aicha", "Khadija", "Zineb", "Sara", "Nour", "Amina", "Hajar", "Meryem", "Salma",
    "Layla", "Naima", "Samira", "Khadija", "Hafsa", "Asma", "Zakia", "Malika", "Latifa", "Rachida",
    "Nadia", "Souad", "Hanane", "Khadija", "Jamila", "Saida", "Zakia", "Naima", "Fatima", "Aicha",
    "Yasmina", "Karima", "Houda", "Nabila", "Siham", "Khadija", "Zakia", "Naima", "Fatima", "Aicha",
    "Mouna", "Rania", "Sanaa", "Khadija", "Zakia", "Naima", "Fatima", "Aicha", "Meryem", "Salma"
]

NOMS_FAMILLE = [
    "Alami", "Benali", "Chraibi", "Daoudi", "El Fassi", "Fassi", "Gharbi", "Hassani", "Idrissi", "Jabri",
    "Kabbaj", "Lahlou", "Mansouri", "Naciri", "Ouali", "Qadiri", "Rahmani", "Saadi", "Tazi", "Uthmani",
    "Verdi", "Wahbi", "Yousfi", "Zerouali", "Ait", "Ben", "El", "Ibn", "Ould", "Al",
    "Bennani", "Cherkaoui", "Dahbi", "El Idrissi", "Fassi", "Gharbi", "Hassani", "Idrissi", "Jabri", "Kabbaj",
    "Lahlou", "Mansouri", "Naciri", "Ouali", "Qadiri", "Rahmani", "Saadi", "Tazi", "Uthmani", "Verdi"
]

def get_db_connection():
    """Connexion directe à SQL Server"""
    try:
        connection_string = (
            f"DRIVER={{{SQLSERVER_CONFIG['driver']}}};"
            f"SERVER={SQLSERVER_CONFIG['host']};"
            f"DATABASE={SQLSERVER_CONFIG['name']};"
            f"Trusted_Connection=yes;"
        )
        return pyodbc.connect(connection_string)
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return None

def get_existing_classes() -> List[Dict[str, Any]]:
    """Récupère les classes existantes"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id_classe, nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        classes = []
        for row in cursor.fetchall():
            classes.append({
                'id': row[0],
                'nom': row[1],
                'niveau': row[2]
            })
        return classes
    except Exception as e:
        print(f"❌ Erreur récupération classes: {e}")
        return []
    finally:
        conn.close()

def generate_student_data() -> Dict[str, Any]:
    """Génère des données réalistes pour un élève"""
    genre = random.choice(['M', 'F'])
    
    if genre == 'M':
        prenom = random.choice(PRENOMS_MASCULINS)
    else:
        prenom = random.choice(PRENOMS_FEMININS)
    
    nom = random.choice(NOMS_FAMILLE)
    
    # Générer une date de naissance réaliste (entre 12 et 18 ans)
    age = random.randint(12, 18)
    birth_date = datetime.now() - timedelta(days=age * 365 + random.randint(0, 365))
    
    return {
        'nom': nom,
        'prenom': prenom,
        'genre': genre,
        'date_naissance': birth_date.strftime('%Y-%m-%d'),
        'lieu_naissance': random.choice([
            "Casablanca", "Rabat", "Marrakech", "Fès", "Meknès", "Tanger", "Agadir", "Oujda",
            "Kénitra", "Tétouan", "Safi", "Mohammedia", "Khouribga", "Beni Mellal", "El Jadida"
        ]),
        'adresse': f"{random.randint(1, 200)} Rue {random.choice(['Mohammed V', 'Hassan II', 'Ibn Sina', 'Al Andalous', 'Ibn Battuta'])}",
        'telephone': f"0{random.randint(6, 7)}{random.randint(10000000, 99999999)}",
        'email': f"{prenom.lower()}.{nom.lower()}@gmail.com"
    }

def distribute_students_to_classes(students: List[Dict[str, Any]], classes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Répartit les élèves dans les classes"""
    if not classes:
        return []
    
    students_per_class = len(students) // len(classes)
    remaining_students = len(students) % len(classes)
    
    print(f"📊 Répartition: {students_per_class} élèves par classe, {remaining_students} supplémentaires")
    
    distributed_students = []
    student_index = 0
    
    for i, classe in enumerate(classes):
        class_size = students_per_class
        if i < remaining_students:
            class_size += 1
        
        print(f"📚 Classe {classe['nom']} ({classe['niveau']}): {class_size} élèves")
        
        for j in range(class_size):
            if student_index < len(students):
                student = students[student_index].copy()
                student['classe_id'] = classe['id']
                student['classe_nom'] = classe['nom']
                student['classe_niveau'] = classe['niveau']
                distributed_students.append(student)
                student_index += 1
    
    return distributed_students

def insert_students_to_database(students: List[Dict[str, Any]]) -> bool:
    """Insère les élèves dans la base de données"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        insert_query = """
        INSERT INTO eleves (
            nom, prenom, genre, date_naissance, adresse, 
            telephone, email, id_classe, statut
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(students), batch_size):
            batch = students[i:i + batch_size]
            batch_data = []
            
            for student in batch:
                batch_data.append((
                    student['nom'],
                    student['prenom'],
                    student['genre'],
                    student['date_naissance'],
                    student['adresse'],
                    student['telephone'],
                    student['email'],
                    student['classe_id'],
                    'Actif'  # Statut par défaut
                ))
            
            cursor.executemany(insert_query, batch_data)
            total_inserted += len(batch_data)
            print(f"✅ {total_inserted}/{len(students)} élèves insérés...")
        
        conn.commit()
        print(f"🎉 Tous les {len(students)} élèves ont été insérés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur insertion: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_classes_statistics():
    """Met à jour les statistiques des classes"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Ajouter les colonnes si elles n'existent pas
        try:
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_eleves INTEGER DEFAULT 0")
        except:
            pass  # Colonne existe déjà
        
        try:
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_garcons INTEGER DEFAULT 0")
        except:
            pass
        
        try:
            cursor.execute("ALTER TABLE classes ADD COLUMN nb_filles INTEGER DEFAULT 0")
        except:
            pass
        
        # Mettre à jour les statistiques
        cursor.execute("""
            UPDATE classes 
            SET 
                capacite = (
                    SELECT COUNT(*) 
                    FROM eleves 
                    WHERE eleves.id_classe = classes.id_classe
                )
        """)
        
        conn.commit()
        print("✅ Statistiques des classes mises à jour")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour stats: {e}")
        return False
    finally:
        conn.close()

def main():
    """Fonction principale"""
    print("🚀 Ajout de 1000 élèves...")
    print("=" * 50)
    
    # 1. Récupérer les classes
    print("📚 Récupération des classes...")
    classes = get_existing_classes()
    
    if not classes:
        print("❌ Aucune classe trouvée!")
        return False
    
    print(f"✅ {len(classes)} classes trouvées")
    
    # 2. Générer 1000 élèves
    print("\n👥 Génération de 1000 élèves...")
    students = []
    for i in range(1000):
        student = generate_student_data()
        students.append(student)
        if (i + 1) % 100 == 0:
            print(f"   {i + 1}/1000 élèves générés...")
    
    # 3. Répartir les élèves
    print("\n📊 Répartition des élèves...")
    distributed_students = distribute_students_to_classes(students, classes)
    
    # 4. Insérer dans la base
    print("\n💾 Insertion dans la base de données...")
    success = insert_students_to_database(distributed_students)
    
    if not success:
        return False
    
    # 5. Mettre à jour les statistiques
    print("\n📈 Mise à jour des statistiques...")
    update_classes_statistics()
    
    print("\n🎉 Processus terminé avec succès!")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 1000 élèves ajoutés avec succès!")
        else:
            print("\n❌ Échec du processus.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)
