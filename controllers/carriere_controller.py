import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_calendriers():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, titre, date_debut, date_fin, description FROM calendriers ORDER BY date_debut DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_calendrier(titre, date_debut, date_fin, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO calendriers (titre, date_debut, date_fin, description)
        VALUES (?, ?, ?, ?)
    """, (titre, date_debut, date_fin, description))
    conn.commit()
    conn.close()

def delete_calendrier(calendrier_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM calendriers WHERE id=?", (calendrier_id,))
    conn.commit()
    conn.close()
