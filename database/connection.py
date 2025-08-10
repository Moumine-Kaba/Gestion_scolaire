import sqlite3
import os

DB_PATH = "database/edumanager.db"

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Active les FK
    return conn

def create_all_tables():
    if not os.path.exists("database"):
        os.makedirs("database")
    conn = connect_db()
    cursor = conn.cursor()

    # Table des professeurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professeurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            sexe TEXT,
            telephone TEXT,
            email TEXT,
            specialite TEXT,
            photo_path TEXT,
            date_embauche TEXT
        )
    """)

    # Table des salles de classe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS salle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            capacite INTEGER,
            type TEXT
        )
    """)

    # Table des classes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS classe (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            niveau TEXT,
            annee_scolaire TEXT,
            professeur_principal_id INTEGER,
            salle_id INTEGER,
            FOREIGN KEY(professeur_principal_id) REFERENCES professeurs(id),
            FOREIGN KEY(salle_id) REFERENCES salle(id)
        )
    """)

    # Table des matières
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matieres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT
        )
    """)

    # Table des élèves
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS eleves (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT,
            sexe TEXT,
            date_naissance TEXT,
            adresse TEXT,
            telephone_parent TEXT,
            email_parent TEXT,
            classe_id INTEGER,
            photo_path TEXT,
            date_inscription TEXT,
            statut TEXT,
            FOREIGN KEY(classe_id) REFERENCES classe(id) ON DELETE CASCADE
        )
    """)

    # Table des enseignements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enseignement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professeur_id INTEGER NOT NULL,
            classe_id INTEGER NOT NULL,
            matiere_id INTEGER NOT NULL,
            salle_id INTEGER,
            FOREIGN KEY(professeur_id) REFERENCES professeurs(id),
            FOREIGN KEY(classe_id) REFERENCES classe(id),
            FOREIGN KEY(matiere_id) REFERENCES matieres(id),
            FOREIGN KEY(salle_id) REFERENCES salle(id)
        )
    """)

    # Table emplois du temps
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emplois_du_temps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            classe_id INTEGER NOT NULL,
            jour TEXT NOT NULL,
            heure TEXT NOT NULL,
            matiere_id INTEGER,
            professeur_id INTEGER,
            salle_id INTEGER,
            FOREIGN KEY(classe_id) REFERENCES classe(id),
            FOREIGN KEY(matiere_id) REFERENCES matieres(id),
            FOREIGN KEY(professeur_id) REFERENCES professeurs(id),
            FOREIGN KEY(salle_id) REFERENCES salle(id)
        )
    """)

    # Table de pointage des présences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS presence (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER NOT NULL,
            classe_id INTEGER NOT NULL,
            professeur_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            statut TEXT NOT NULL,
            commentaire TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id),
            FOREIGN KEY(classe_id) REFERENCES classe(id),
            FOREIGN KEY(professeur_id) REFERENCES professeurs(id)
        )
    """)

    # Table des notes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER NOT NULL,
            matiere_id INTEGER NOT NULL,
            note REAL NOT NULL,
            date TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id),
            FOREIGN KEY(matiere_id) REFERENCES matieres(id)
        )
    """)

    # Table de transfert d’élèves (historique)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transferts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER NOT NULL,
            ancienne_classe_id INTEGER,
            nouvelle_classe_id INTEGER,
            date_transfert TEXT NOT NULL,
            motif TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id),
            FOREIGN KEY(ancienne_classe_id) REFERENCES classe(id),
            FOREIGN KEY(nouvelle_classe_id) REFERENCES classe(id)
        )
    """)

    # Table des paiements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER NOT NULL,
            montant REAL NOT NULL,
            date TEXT NOT NULL,
            mode_paiement TEXT,
            description TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id)
        )
    """)

    # Table des bulletins scolaires
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulletins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            eleve_id INTEGER,
            annee_scolaire TEXT,
            trimestre TEXT,
            moyenne REAL,
            remarque TEXT,
            date_edition TEXT,
            FOREIGN KEY(eleve_id) REFERENCES eleves(id)
        )
    """)

    # ==== TABLES ADMINISTRATIVES ET ANNEXES ====

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            prenom TEXT,
            nom TEXT,
            email TEXT UNIQUE,
            telephone TEXT,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            niveau TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            chemin TEXT,
            type TEXT,
            date_ajout TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS carrieres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            intitule TEXT NOT NULL,
            description TEXT,
            utilisateur_id INTEGER,
            date_debut TEXT,
            date_fin TEXT,
            FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            niveau TEXT,
            utilisateur_id INTEGER,
            FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objectifs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            date_debut TEXT,
            date_fin TEXT,
            statut TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS maintenances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objet TEXT NOT NULL,
            description TEXT,
            statut TEXT,
            date_signalement TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS calendriers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            date_debut TEXT,
            date_fin TEXT,
            description TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bibliotheque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            auteur TEXT,
            type TEXT,
            annee TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expediteur_id INTEGER,
            destinataire_id INTEGER,
            contenu TEXT,
            date_envoi TEXT,
            FOREIGN KEY(expediteur_id) REFERENCES utilisateurs(id),
            FOREIGN KEY(destinataire_id) REFERENCES utilisateurs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS annonces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            contenu TEXT NOT NULL,
            date TEXT NOT NULL,
            auteur_id INTEGER,
            FOREIGN KEY(auteur_id) REFERENCES utilisateurs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contenu TEXT NOT NULL,
            date TEXT NOT NULL,
            utilisateur_id INTEGER,
            lu INTEGER DEFAULT 0,
            FOREIGN KEY(utilisateur_id) REFERENCES utilisateurs(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS taches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            statut TEXT,
            date_echeance TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Toutes les tables principales et annexes sont créées correctement !")

if __name__ == "__main__":
    create_all_tables()
