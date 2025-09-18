from src.utils.db_utils import get_connection

def _init_actualites_table():
    """Initialise la table actualites si elle n'existe pas."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'actualites'
        """)
        
        if cursor.fetchone()[0] == 0:
            # Créer la table actualites
            cursor.execute("""
                CREATE TABLE actualites (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    titre NVARCHAR(200) NOT NULL,
                    contenu NVARCHAR(MAX),
                    date DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print("✅ Table actualites créée")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur création table actualites: {e}")
        return False

def get_all_actualites():
    # Initialiser la table si nécessaire
    _init_actualites_table()
    
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