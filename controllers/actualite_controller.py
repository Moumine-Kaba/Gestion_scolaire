from utils.db_utils import get_connection

def get_all_actualites():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, titre, contenu, date
        FROM actualites
        ORDER BY date DESC
    """)
    result = cursor.fetchall()
    conn.close()
    return result

def add_actualite(titre, contenu, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO actualites (titre, contenu, date)
        VALUES (?, ?, ?)
    """, (titre, contenu, date))
    conn.commit()
    conn.close()
    return True

def update_actualite(id, titre, contenu, date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE actualites SET titre=?, contenu=?, date=?
        WHERE id=?
    """, (titre, contenu, date, id))
    conn.commit()
    conn.close()
    return True

def delete_actualite(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM actualites WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return True
