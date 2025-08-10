import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_calendriers():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, titre, date_debut, date_fin, description FROM calendriers")
    data = cur.fetchall()
    conn.close()
    return data

def add_calendrier(titre, date_debut, date_fin, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO calendriers (titre, date_debut, date_fin, description) VALUES (?, ?, ?, ?)",
                (titre, date_debut, date_fin, description))
    conn.commit()
    conn.close()

def update_calendrier(id, titre, date_debut, date_fin, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE calendriers SET titre=?, date_debut=?, date_fin=?, description=? WHERE id=?",
                (titre, date_debut, date_fin, description, id))
    conn.commit()
    conn.close()

def delete_calendrier(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM calendriers WHERE id=?", (id,))
    conn.commit()
    conn.close()
