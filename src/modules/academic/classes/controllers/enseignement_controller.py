# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os

# Chemin de base de données relatif
DB_PATH = "database/edumanager.db"

def _connect():
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server  # Permet d'accéder aux colonnes par leur nom
    return conn

def get_all_enseignements():
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

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
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO enseignement (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut))
            conn.commit()
                conn.close()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur add_enseignement : {e}")
        return False

def update_enseignement(id, professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut):
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cursor = conn.cursor()
            cursor.execute("""
                UPDATE enseignement
                SET professeur_id=?, classe_id=?, matiere_id=?, salle_id=?, jours_cours=?, duree_cours=?, statut=?
                WHERE id=?
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut, id))
            conn.commit()
                conn.close()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur update_enseignement : {e}")
        return False

def delete_enseignement(id):
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cursor = conn.cursor()
            cursor.execute("DELETE FROM enseignement WHERE id=?", (id,))
            conn.commit()
                conn.close()
            return True
    except Exception as e:
        print(f"[Enseignement] Erreur delete_enseignement : {e}")
        return False