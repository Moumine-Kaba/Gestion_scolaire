import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_personnel():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, nom, prenom, poste, telephone, email FROM personnel")
    data = cur.fetchall()
    conn.close()
    return data

def add_personnel(nom, prenom, poste, telephone, email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO personnel (nom, prenom, poste, telephone, email) VALUES (?, ?, ?, ?, ?)",
                (nom, prenom, poste, telephone, email))
    conn.commit()
    conn.close()

def update_personnel(id, nom, prenom, poste, telephone, email):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("UPDATE personnel SET nom=?, prenom=?, poste=?, telephone=?, email=? WHERE id=?",
                (nom, prenom, poste, telephone, email, id))
    conn.commit()
    conn.close()

def delete_personnel(id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM personnel WHERE id=?", (id,))
    conn.commit()
    conn.close()
