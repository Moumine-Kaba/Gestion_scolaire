from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_bibliotheques():
    """Retourne tous les livres/documents de la bibliothèque."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bibliotheque ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_bibliotheque(titre, auteur, type, annee):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bibliotheque (titre, auteur, type, annee)
        VALUES (?, ?, ?, ?)
    """, (titre, auteur, type, annee))
    conn.commit()
    conn.close()

def update_bibliotheque(id, titre, auteur, type, annee):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bibliotheque
        SET titre=?, auteur=?, type=?, annee=?
        WHERE id=?
    """, (titre, auteur, type, annee, id))
    conn.commit()
    conn.close()

def delete_bibliotheque(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bibliotheque WHERE id=?", (id,))
    conn.commit()
    conn.close()
