from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_bulletins(eleve_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    if eleve_id:
        cur.execute("""
            SELECT id, annee_scolaire, trimestre, moyenne, remarque, date_edition FROM bulletins WHERE eleve_id=? ORDER BY date_edition DESC
        """, (eleve_id,))
    else:
        cur.execute("""
            SELECT id, eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition FROM bulletins ORDER BY date_edition DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_bulletin(eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bulletins (eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition))
    conn.commit()
    conn.close()

def update_bulletin(bulletin_id, eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bulletins SET eleve_id=?, annee_scolaire=?, trimestre=?, moyenne=?, remarque=?, date_edition=?
        WHERE id=?
    """, (eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition, bulletin_id))
    conn.commit()
    conn.close()

def delete_bulletin(bulletin_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bulletins WHERE id=?", (bulletin_id,))
    conn.commit()
    conn.close()
