from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_objectifs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titre, description, date_debut, date_fin, statut FROM objectifs ORDER BY date_debut DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_objectif(titre, description, date_debut, date_fin, statut):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO objectifs (titre, description, date_debut, date_fin, statut)
        VALUES (?, ?, ?, ?, ?)
    """, (titre, description, date_debut, date_fin, statut))
    conn.commit()
    conn.close()

def update_objectif(obj_id, titre, description, date_debut, date_fin, statut):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE objectifs SET titre=?, description=?, date_debut=?, date_fin=?, statut=?
        WHERE id=?
    """, (titre, description, date_debut, date_fin, statut, obj_id))
    conn.commit()
    conn.close()

def delete_objectif(obj_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM objectifs WHERE id=?", (obj_id,))
    conn.commit()
    conn.close()
