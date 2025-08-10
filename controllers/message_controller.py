import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_messages():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, expediteur_id, destinataire_id, contenu, date_envoi
        FROM messages ORDER BY date_envoi DESC
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_message(expediteur_id, destinataire_id, contenu, date_envoi):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO messages (expediteur_id, destinataire_id, contenu, date_envoi)
        VALUES (?, ?, ?, ?)
    """, (expediteur_id, destinataire_id, contenu, date_envoi))
    conn.commit()
    conn.close()

def delete_message(message_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM messages WHERE id=?", (message_id,))
    conn.commit()
    conn.close()
