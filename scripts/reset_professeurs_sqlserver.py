"""
Réinitialise la table professeurs et heures_cours dans SQL Server,
recrée le schéma propre, puis insère 20 professeurs avec un taux horaire.
"""

import random
from datetime import datetime
from database.connection import get_db_connection


PROF_SPECIALITES = [
    "Mathématiques", "Physique", "Chimie", "SVT", "Informatique",
    "Histoire", "Géographie", "Français", "Anglais", "Philosophie",
    "Comptabilité", "Economie", "Droit", "Espagnol", "Arabe",
    "Education Civique", "Arts", "Musique", "Sport", "Technologie"
]

NOMS_EXEMPLE = [
    "Diallo", "Bah", "Camara", "Barry", "Sylla", "Sow", "Condé", "Keita",
    "Cissé", "Conté", "Traoré", "Kaba", "Bangoura", "Dramé", "Balde",
    "Djalo", "Sidibé", "Diakité", "Fofana", "Touré"
]

PRENOMS_EXEMPLE = [
    "Mamadou", "Ibrahima", "Aissatou", "Fatoumata", "Alpha", "Mariam",
    "Oumar", "Amadou", "N'Faly", "Abdoulaye", "Kadiatou", "Mouctar",
    "Saliou", "Néné", "Mory", "Naby", "Souleymane", "Maimouna", "Nana", "Ibrahima Sory"
]


def drop_and_recreate_tables():
    conn = get_db_connection()
    if not conn:
        print("❌ Connexion SQL Server indisponible")
        return False
    cur = conn.cursor()

    try:
        cur.execute("IF OBJECT_ID('dbo.heures_cours', 'U') IS NOT NULL DROP TABLE dbo.heures_cours;")
    except Exception:
        pass
    try:
        cur.execute("IF OBJECT_ID('dbo.professeurs', 'U') IS NOT NULL DROP TABLE dbo.professeurs;")
    except Exception:
        pass

    cur.execute(
        """
        CREATE TABLE dbo.professeurs (
            id INT IDENTITY(1,1) PRIMARY KEY,
            nom NVARCHAR(100) NOT NULL,
            prenom NVARCHAR(100) NOT NULL,
            email NVARCHAR(150) NULL,
            telephone NVARCHAR(50) NULL,
            specialite NVARCHAR(100) NULL,
            sexe NVARCHAR(1) NULL,
            salaire_horaire DECIMAL(18,2) NOT NULL DEFAULT 0,
            date_embauche DATE NULL,
            statut NVARCHAR(20) NULL
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE dbo.heures_cours (
            id INT IDENTITY(1,1) PRIMARY KEY,
            professeur_id INT NOT NULL,
            date_cours DATE NOT NULL,
            nombre_heures DECIMAL(8,2) NOT NULL,
            matiere NVARCHAR(100) NULL,
            classe NVARCHAR(100) NULL,
            statut NVARCHAR(20) NOT NULL DEFAULT 'effectue',
            commentaire NVARCHAR(255) NULL,
            CONSTRAINT FK_heures_professeurs FOREIGN KEY (professeur_id)
                REFERENCES dbo.professeurs(id)
        );
        """
    )

    conn.commit()
    conn.close()
    print("✅ Tables professeurs et heures_cours recréées")
    return True


def seed_professeurs(n=20):
    conn = get_db_connection()
    if not conn:
        print("❌ Connexion SQL Server indisponible")
        return False
    cur = conn.cursor()

    today = datetime.now().date()
    rows = []
    for i in range(n):
        nom = random.choice(NOMS_EXEMPLE)
        prenom = random.choice(PRENOMS_EXEMPLE)
        spec = PROF_SPECIALITES[i % len(PROF_SPECIALITES)]
        sexe = random.choice(['M', 'F'])
        taux = random.choice([40000, 45000, 50000, 55000, 60000, 65000])
        email = f"{prenom.lower()}.{nom.lower()}@ecole.gn"
        tel = f"62{random.randint(1000000, 9999999)}"
        rows.append((nom, prenom, email, tel, spec, sexe, taux, today, 'Actif'))

    cur.executemany(
        """
        INSERT INTO dbo.professeurs (nom, prenom, email, telephone, specialite, sexe, salaire_horaire, date_embauche, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    conn.commit()
    conn.close()
    print(f"✅ {n} professeurs insérés avec taux horaire")
    return True


def main():
    if drop_and_recreate_tables():
        seed_professeurs(20)


if __name__ == "__main__":
    main()


