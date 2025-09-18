from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_maintenances():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, objet, description, statut, date_signalement FROM maintenances ORDER BY date_signalement DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_maintenance(objet, description, statut, date_signalement):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO maintenances (objet, description, statut, date_signalement)
        VALUES (?, ?, ?, ?)
    """, (objet, description, statut, date_signalement))
    conn.commit()
    conn.close()

def update_maintenance(maintenance_id, objet, description, statut, date_signalement):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE maintenances 
        SET objet=?, description=?, statut=?, date_signalement=?
        WHERE id=?
    """, (objet, description, statut, date_signalement, maintenance_id))
    conn.commit()
    conn.close()

def delete_maintenance(maintenance_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM maintenances WHERE id=?", (maintenance_id,))
    conn.commit()
    conn.close()
