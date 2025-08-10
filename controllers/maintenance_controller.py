import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_maintenances():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, objet, description, statut, date_signalement FROM maintenances ORDER BY date_signalement DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_maintenance(objet, description, statut, date_signalement):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO maintenances (objet, description, statut, date_signalement)
        VALUES (?, ?, ?, ?)
    """, (objet, description, statut, date_signalement))
    conn.commit()
    conn.close()

def delete_maintenance(maintenance_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM maintenances WHERE id=?", (maintenance_id,))
    conn.commit()
    conn.close()
