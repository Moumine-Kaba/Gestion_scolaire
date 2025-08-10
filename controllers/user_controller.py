import sqlite3
DB_PATH = "database/edumanager.db"

def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, username, prenom, nom, email, telephone, role, niveau
        FROM utilisateurs
        ORDER BY nom
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_user(username, prenom, nom, email, telephone, password, role, niveau):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO utilisateurs (username, prenom, nom, email, telephone, password, role, niveau)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, prenom, nom, email, telephone, password, role, niveau))
    conn.commit()
    conn.close()

def update_user(user_id, username, prenom, nom, email, telephone, password, role, niveau):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        UPDATE utilisateurs SET username=?, prenom=?, nom=?, email=?, telephone=?, password=?, role=?, niveau=?
        WHERE id=?
    """, (username, prenom, nom, email, telephone, password, role, niveau, user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM utilisateurs WHERE id=?", (user_id,))
    conn.commit()
    conn.close()
