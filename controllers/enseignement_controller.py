import sqlite3
import os

# J'utilise le chemin de base de données que vous avez spécifié précédemment.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

def get_all_enseignements():
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut
                FROM enseignement
                ORDER BY id DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"[Enseignement] Erreur get_all_enseignements : {e}")
        return []

def add_enseignement(professeur_id, classe_id, matiere_id, salle_id=None, jours_cours=None, duree_cours=None, statut=None):
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enseignement (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut))
            conn.commit()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur add_enseignement : {e}")
        return False

def update_enseignement(id, professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut):
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE enseignement
                SET professeur_id=?, classe_id=?, matiere_id=?, salle_id=?, jours_cours=?, duree_cours=?, statut=?
                WHERE id=?
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut, id))
            conn.commit()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur update_enseignement : {e}")
        return False

def delete_enseignement(id):
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM enseignement WHERE id=?", (id,))
            conn.commit()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur delete_enseignement : {e}")
        return False