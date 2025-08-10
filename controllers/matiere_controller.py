import sqlite3
import os

# ====== DB PATH from persistent information ======
# Le chemin de la base de données est conservé comme demandé.
DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def _connect():
    """
    Crée et retourne une connexion à la base de données.
    Utilise 'with' pour garantir la fermeture automatique de la connexion.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def get_all_matieres():
    """
    Récupère toutes les matières de la base de données, triées par nom.
    """
    try:
        with _connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nom, description FROM matieres ORDER BY nom ASC")
                matieres = cursor.fetchall()
                return [dict(m) for m in matieres]
    except sqlite3.Error as e:
        print(f"Erreur lors de la récupération de toutes les matières : {e}")
    return []

def search_matieres(q):
    """
    Recherche des matières par nom ou description, sans tenir compte de la casse.
    """
    try:
        with _connect() as conn:
            if conn:
                like_term = f"%{q.strip()}%"
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nom, description
                    FROM matieres
                    WHERE nom LIKE ? COLLATE NOCASE
                       OR description LIKE ? COLLATE NOCASE
                    ORDER BY nom ASC
                """, (like_term, like_term))
                matieres = cursor.fetchall()
                return [dict(m) for m in matieres]
    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche des matières : {e}")
    return []

def add_matiere(nom, description=""):
    """
    Ajoute une nouvelle matière à la base de données.
    Retourne True en cas de succès, False sinon.
    """
    try:
        with _connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO matieres (nom, description) VALUES (?, ?)", (nom, description))
                conn.commit()
                return True
    except sqlite3.IntegrityError:
        print(f"Erreur: La matière '{nom}' existe déjà.")
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de la matière : {e}")
    return False

def update_matiere(matiere_id, nom, description):
    """
    Met à jour une matière existante par son ID.
    Retourne True en cas de succès, False sinon.
    """
    try:
        with _connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE matieres SET nom = ?, description = ? WHERE id = ?", (nom, description, matiere_id))
                conn.commit()
                return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour de la matière : {e}")
    return False

def delete_matiere(matiere_id):
    """
    Supprime une matière de la base de données par son ID.
    Retourne True en cas de succès, False sinon.
    """
    try:
        with _connect() as conn:
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM matieres WHERE id = ?", (matiere_id,))
                conn.commit()
                return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la suppression de la matière : {e}")
    return False