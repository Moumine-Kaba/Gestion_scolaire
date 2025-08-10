import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_competences():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, titre, description, niveau, utilisateur_id FROM competences ORDER BY titre")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_competence(titre, description, niveau, utilisateur_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO competences (titre, description, niveau, utilisateur_id)
        VALUES (?, ?, ?, ?)
    """, (titre, description, niveau, utilisateur_id))
    conn.commit()
    conn.close()

def delete_competence(comp_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM competences WHERE id=?", (comp_id,))
    conn.commit()
    conn.close()
