import sqlite3
import os

DB_PATH = r"C:\Users\Lenovo\Desktop\EduManager+\database\edumanager.db"

def _connect():
    """Crée et retourne une connexion à la base de données configurée."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux données par les noms de colonnes
    return conn

def get_all_salles():
    """Liste toutes les salles en tant que dictionnaires."""
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nom, capacite, type
                FROM salle
                ORDER BY nom
            """)
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[Salle] Erreur get_all_salles: {e}")
        return []

def add_salle(nom, capacite, type_):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO salle (nom, capacite, type)
                VALUES (?, ?, ?)
            """, (nom, capacite, type_))
            conn.commit()
    except Exception as e:
        print(f"[Salle] Erreur add_salle: {e}")

def update_salle(salle_id, nom, capacite, type_):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE salle
                SET nom=?, capacite=?, type=?
                WHERE id=?
            """, (nom, capacite, type_, salle_id))
            conn.commit()
    except Exception as e:
        print(f"[Salle] Erreur update_salle: {e}")

def delete_salle(salle_id):
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM salle WHERE id=?", (salle_id,))
            conn.commit()
    except Exception as e:
        print(f"[Salle] Erreur delete_salle: {e}")