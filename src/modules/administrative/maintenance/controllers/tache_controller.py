from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_taches():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titre, description, statut, date_echeance FROM taches ORDER BY date_echeance DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_tache(titre, description, statut, date_echeance):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO taches (titre, description, statut, date_echeance)
        VALUES (?, ?, ?, ?)
    """, (titre, description, statut, date_echeance))
    conn.commit()
    conn.close()

def update_tache(tache_id, titre, description, statut, date_echeance):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE taches SET titre=?, description=?, statut=?, date_echeance=?
        WHERE id=?
    """, (titre, description, statut, date_echeance, tache_id))
    conn.commit()
    conn.close()

def delete_tache(tache_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM taches WHERE id=?", (tache_id,))
    conn.commit()
    conn.close()
