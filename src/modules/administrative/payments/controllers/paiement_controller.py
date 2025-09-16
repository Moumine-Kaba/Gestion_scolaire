import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_paiements(eleve_id=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if eleve_id:
        cur.execute("""
            SELECT id, montant, date, mode_paiement, description FROM paiements WHERE eleve_id=? ORDER BY date DESC
        """, (eleve_id,))
    else:
        cur.execute("""
            SELECT id, eleve_id, montant, date, mode_paiement, description FROM paiements ORDER BY date DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_paiement(eleve_id, montant, date, mode_paiement, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO paiements (eleve_id, montant, date, mode_paiement, description)
        VALUES (?, ?, ?, ?, ?)
    """, (eleve_id, montant, date, mode_paiement, description))
    conn.commit()
    conn.close()

def update_paiement(paiement_id, eleve_id, montant, date, mode_paiement, description):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE paiements SET eleve_id=?, montant=?, date=?, mode_paiement=?, description=?
        WHERE id=?
    """, (eleve_id, montant, date, mode_paiement, description, paiement_id))
    conn.commit()
    conn.close()

def delete_paiement(paiement_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM paiements WHERE id=?", (paiement_id,))
    conn.commit()
    conn.close()
