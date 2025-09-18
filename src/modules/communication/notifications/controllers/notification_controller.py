from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
# Remplacé par SQL Server  # Remplacé par SQL Server
DB_PATH = "database/edumanager.db"

def get_all_notifications():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM notifications ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_notification(contenu, date, utilisateur_id, lu=0):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO notifications (contenu, date, utilisateur_id, lu)
        VALUES (?, ?, ?, ?)
    """, (contenu, date, utilisateur_id, lu))
    conn.commit()
    conn.close()

def update_notification(notification_id, contenu, date, utilisateur_id, lu):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE notifications SET contenu=?, date=?, utilisateur_id=?, lu=?
        WHERE id=?
    """, (contenu, date, utilisateur_id, lu, notification_id))
    conn.commit()
    conn.close()

def delete_notification(notification_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notifications WHERE id=?", (notification_id,))
    conn.commit()
    conn.close()
