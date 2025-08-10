import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_transferts(eleve_id=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if eleve_id:
        cur.execute("""
            SELECT id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif FROM transferts
            WHERE eleve_id=? ORDER BY date_transfert DESC
        """, (eleve_id,))
    else:
        cur.execute("""
            SELECT id, eleve_id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif FROM transferts
            ORDER BY date_transfert DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_transfert(eleve_id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO transferts (eleve_id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif)
        VALUES (?, ?, ?, ?, ?)
    """, (eleve_id, ancienne_classe_id, nouvelle_classe_id, date_transfert, motif))
    conn.commit()
    conn.close()

def delete_transfert(transfert_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM transferts WHERE id=?", (transfert_id,))
    conn.commit()
    conn.close()
