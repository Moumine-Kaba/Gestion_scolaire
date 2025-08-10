import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_annonces():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM annonces ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_annonce(titre, contenu, date, auteur_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO annonces (titre, contenu, date, auteur_id)
        VALUES (?, ?, ?, ?)
    """, (titre, contenu, date, auteur_id))
    conn.commit()
    conn.close()

def update_annonce(annonce_id, titre, contenu, date, auteur_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE annonces SET titre=?, contenu=?, date=?, auteur_id=?
        WHERE id=?
    """, (titre, contenu, date, auteur_id, annonce_id))
    conn.commit()
    conn.close()

def delete_annonce(annonce_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM annonces WHERE id=?", (annonce_id,))
    conn.commit()
    conn.close()
