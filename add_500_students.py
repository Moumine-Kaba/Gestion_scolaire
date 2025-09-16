#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour ajouter 500 élèves répartis dans les différentes classes
"""

import sqlite3
import random
from datetime import datetime, timedelta

# Chemin vers la base de données
DB_PATH = r"C:\Users\Lenovo\Desktop\Clonage_git\Gestion_scolaire\Gestion_scolaire\database\edumanager.db"

def generate_student_data():
    """Génère des données d'élèves réalistes"""
    
    # Prénoms français et africains
    prenoms_masculins = [
        "Jean", "Pierre", "Paul", "Jacques", "Michel", "André", "Philippe", "Alain", "Bernard", "Robert",
        "Moussa", "Ibrahim", "Amadou", "Boubacar", "Cheikh", "Ousmane", "Mamadou", "Sékou", "Abdoulaye", "Modou",
        "Kevin", "Jordan", "Alexandre", "Thomas", "Nicolas", "Antoine", "Julien", "Maxime", "Romain", "Sébastien"
    ]
    
    prenoms_feminins = [
        "Marie", "Françoise", "Monique", "Catherine", "Sylvie", "Nathalie", "Isabelle", "Christine", "Martine", "Patricia",
        "Fatou", "Aïcha", "Mariama", "Kadiatou", "Aminata", "Rokhaya", "Khadija", "Awa", "Ndeye", "Diarra",
        "Camille", "Julie", "Sarah", "Laura", "Emma", "Chloé", "Léa", "Manon", "Claire", "Sophie"
    ]
    
    noms = [
        "Traoré", "Diop", "Sow", "Diallo", "Ba", "Fall", "Ndiaye", "Gueye", "Sy", "Cissé",
        "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent",
        "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Morel", "Fournier", "Girard"
    ]
    
    # Générer 500 élèves
    eleves = []
    
    for i in range(500):
        # Genre aléatoire
        genre = random.choice(["M", "F"])
        
        # Prénom selon le genre
        if genre == "M":
            prenom = random.choice(prenoms_masculins)
        else:
            prenom = random.choice(prenoms_feminins)
        
        nom = random.choice(noms)
        
        # Date de naissance réaliste (entre 5 et 18 ans)
        age = random.randint(5, 18)
        date_naissance = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
        
        # Email
        email = f"{prenom.lower()}.{nom.lower()}@email.com"
        
        # Téléphone
        telephone = f"77{random.randint(1000000, 9999999)}"
        
        # Adresse
        adresses = [
            "Dakar, Sénégal", "Thiès, Sénégal", "Kaolack, Sénégal", "Ziguinchor, Sénégal",
            "Saint-Louis, Sénégal", "Diourbel, Sénégal", "Tambacounda, Sénégal", "Kolda, Sénégal",
            "Matam, Sénégal", "Kaffrine, Sénégal", "Kédougou, Sénégal", "Sédhiou, Sénégal"
        ]
        adresse = random.choice(adresses)
        
        # Statut
        statut = random.choice(["actif", "actif", "actif", "suspendu"])  # 75% actifs
        
        # Date d'inscription
        date_inscription = datetime.now() - timedelta(days=random.randint(1, 365))
        
        eleve = {
            "prenom": prenom,
            "nom": nom,
            "date_naissance": date_naissance.strftime("%Y-%m-%d"),
            "genre": genre,
            "email": email,
            "telephone": telephone,
            "adresse": adresse,
            "statut": statut,
            "date_inscription": date_inscription.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        eleves.append(eleve)
    
    return eleves

def get_classes_distribution():
    """Récupère les classes et calcule la répartition"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Récupérer toutes les classes
    cursor.execute("SELECT id_classe, nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
    classes = cursor.fetchall()
    
    conn.close()
    
    # Répartition des 500 élèves par niveau
    # PRIMAIRE: 150 élèves (6 classes = 25 élèves/classe)
    # COLLÈGE: 120 élèves (4 classes = 30 élèves/classe)  
    # LYCÉE: 230 élèves (9 classes = 25-26 élèves/classe)
    
    distribution = {}
    eleve_id = 1
    
    for id_classe, nom_classe, niveau in classes:
        if niveau == "PRIMAIRE":
            nb_eleves = 25
        elif niveau == "COLLÈGE":
            nb_eleves = 30
        else:  # LYCÉE
            nb_eleves = 25 if eleve_id <= 250 else 26
        
        distribution[id_classe] = {
            "nom": nom_classe,
            "niveau": niveau,
            "nb_eleves": nb_eleves
        }
        eleve_id += nb_eleves
    
    return distribution

def add_students_to_database():
    """Ajoute les 500 élèves dans la base de données"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        print("🎓 Ajout de 500 élèves dans les classes")
        print("=" * 50)
        
        # Générer les données des élèves
        eleves = generate_student_data()
        print(f"✅ {len(eleves)} élèves générés")
        
        # Obtenir la répartition par classe
        distribution = get_classes_distribution()
        
        # Ajouter les élèves
        eleve_index = 0
        
        for id_classe, info in distribution.items():
            nb_eleves_classe = info["nb_eleves"]
            print(f"📚 {info['nom']} ({info['niveau']}): {nb_eleves_classe} élèves")
            
            for i in range(nb_eleves_classe):
                if eleve_index < len(eleves):
                    eleve = eleves[eleve_index]
                    
                    cursor.execute("""
                        INSERT INTO eleves (
                            prenom, nom, date_naissance, genre, email, telephone, 
                            adresse, statut, date_inscription, id_classe
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        eleve["prenom"],
                        eleve["nom"], 
                        eleve["date_naissance"],
                        eleve["genre"],
                        eleve["email"],
                        eleve["telephone"],
                        eleve["adresse"],
                        eleve["statut"],
                        eleve["date_inscription"],
                        id_classe
                    ))
                    
                    eleve_index += 1
        
        # Valider les changements
        conn.commit()
        
        # Vérifier le résultat
        cursor.execute("SELECT COUNT(*) FROM eleves")
        total_eleves = cursor.fetchone()[0]
        
        cursor.execute("SELECT niveau, COUNT(*) FROM eleves e JOIN classes c ON e.id_classe = c.id_classe GROUP BY niveau")
        par_niveau = cursor.fetchall()
        
        print(f"\n📊 Résultat:")
        print(f"   Total élèves ajoutés: {total_eleves}")
        print(f"\n📚 Répartition par niveau:")
        for niveau, count in par_niveau:
            print(f"   {niveau}: {count} élèves")
        
        conn.close()
        print("\n🎉 Ajout des élèves terminé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_students_to_database()
