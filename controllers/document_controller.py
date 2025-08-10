import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_documents():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, nom, chemin, type, date_ajout FROM documents ORDER BY date_ajout DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_document(nom, chemin, type_, date_ajout):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO documents (nom, chemin, type, date_ajout)
        VALUES (?, ?, ?, ?)
    """, (nom, chemin, type_, date_ajout))
    conn.commit()
    conn.close()

def delete_document(doc_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM documents WHERE id=?", (doc_id,))
    conn.commit()
    conn.close()
