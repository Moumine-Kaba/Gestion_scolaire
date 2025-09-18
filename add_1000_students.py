#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter 1000 élèves et les répartir dans les classes
===============================================================

Ce script génère 1000 élèves avec des données réalistes et les répartit
équitablement dans les classes existantes.
"""

import random
import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, root_path)

from database.connection import get_db_connection

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

NIVEAUX_CLASSES = [
    "6ème", "5ème", "4ème", "3ème", "2ème", "1ère", "Terminale"
]

def get_existing_classes() -> List[Dict[str, Any]]:
    """Récupère les classes existantes de la base de données"""
    conn = get_db_connection()
    if not conn:
        print("❌ Impossible de se connecter à la base de données")
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom, niveau FROM classes ORDER BY niveau, nom")
        classes = []
        for row in cursor.fetchall():
            classes.append({
                'id': row[0],
                'nom': row[1],
                'niveau': row[2]
            })
        return classes
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des classes: {e}")
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
    """Répartit les élèves dans les classes de manière équitable"""
    if not classes:
        print("❌ Aucune classe trouvée")
        return []
    
    # Calculer le nombre d'élèves par classe
    students_per_class = len(students) // len(classes)
    remaining_students = len(students) % len(classes)
    
    print(f"📊 Répartition: {students_per_class} élèves par classe, {remaining_students} élèves supplémentaires")
    
    # Répartir les élèves
    distributed_students = []
    student_index = 0
    
    for i, classe in enumerate(classes):
        # Nombre d'élèves pour cette classe
        class_size = students_per_class
        if i < remaining_students:
            class_size += 1
        
        print(f"📚 Classe {classe['nom']} ({classe['niveau']}): {class_size} élèves")
        
        # Assigner les élèves à cette classe
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
        print("❌ Impossible de se connecter à la base de données")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Préparer la requête d'insertion
        insert_query = """
        INSERT INTO eleves (
            nom, prenom, genre, date_naissance, lieu_naissance, 
            adresse, telephone, email, classe_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Insérer les élèves par lots pour optimiser les performances
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
                    student['lieu_naissance'],
                    student['adresse'],
                    student['telephone'],
                    student['email'],
                    student['classe_id']
                ))
            
            cursor.executemany(insert_query, batch_data)
            total_inserted += len(batch_data)
            print(f"✅ {total_inserted}/{len(students)} élèves insérés...")
        
        conn.commit()
        print(f"🎉 Tous les {len(students)} élèves ont été insérés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des élèves: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def update_classes_statistics():
    """Met à jour les statistiques des classes"""
    conn = get_db_connection()
    if not conn:
        print("❌ Impossible de se connecter à la base de données")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Compter les élèves par classe
        cursor.execute("""
            SELECT classe_id, COUNT(*) as nb_eleves,
                   COUNT(CASE WHEN genre = 'M' THEN 1 END) as nb_garcons,
                   COUNT(CASE WHEN genre = 'F' THEN 1 END) as nb_filles
            FROM eleves 
            WHERE classe_id IS NOT NULL
            GROUP BY classe_id
        """)
        
        stats = cursor.fetchall()
        print(f"📊 Statistiques mises à jour pour {len(stats)} classes")
        
        for stat in stats:
            classe_id, nb_eleves, nb_garcons, nb_filles = stat
            print(f"   Classe ID {classe_id}: {nb_eleves} élèves ({nb_garcons} garçons, {nb_filles} filles)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour des statistiques: {e}")
        return False
    finally:
        conn.close()

def main():
    """Fonction principale"""
    print("🚀 Début de l'ajout de 1000 élèves...")
    print("=" * 50)
    
    # 1. Récupérer les classes existantes
    print("📚 Récupération des classes existantes...")
    classes = get_existing_classes()
    
    if not classes:
        print("❌ Aucune classe trouvée. Veuillez d'abord créer des classes.")
        return False
    
    print(f"✅ {len(classes)} classes trouvées:")
    for classe in classes:
        print(f"   - {classe['nom']} ({classe['niveau']})")
    
    # 2. Générer 1000 élèves
    print("\n👥 Génération de 1000 élèves...")
    students = []
    for i in range(1000):
        student = generate_student_data()
        students.append(student)
        if (i + 1) % 100 == 0:
            print(f"   {i + 1}/1000 élèves générés...")
    
    print(f"✅ {len(students)} élèves générés avec succès!")
    
    # 3. Répartir les élèves dans les classes
    print("\n📊 Répartition des élèves dans les classes...")
    distributed_students = distribute_students_to_classes(students, classes)
    
    if not distributed_students:
        print("❌ Échec de la répartition des élèves")
        return False
    
    # 4. Insérer les élèves dans la base de données
    print("\n💾 Insertion des élèves dans la base de données...")
    success = insert_students_to_database(distributed_students)
    
    if not success:
        print("❌ Échec de l'insertion des élèves")
        return False
    
    # 5. Mettre à jour les statistiques
    print("\n📈 Mise à jour des statistiques...")
    update_classes_statistics()
    
    print("\n🎉 Processus terminé avec succès!")
    print("=" * 50)
    print(f"✅ {len(distributed_students)} élèves ajoutés et répartis dans {len(classes)} classes")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Mission accomplie! Les 1000 élèves ont été ajoutés avec succès.")
        else:
            print("\n❌ Échec du processus d'ajout des élèves.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ Processus interrompu par l'utilisateur.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
