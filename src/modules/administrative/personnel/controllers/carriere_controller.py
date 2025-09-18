from database.connection import get_db_connection

def get_all_carrieres():
    """Retourne toutes les carrières"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM carrieres ORDER BY nom")
        rows = cur.fetchall()
        
        # Convertir en dictionnaires pour SQL Server
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des carrières: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_carriere(nom, description=None):
    """Ajoute une nouvelle carrière"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO carrieres (nom, description)
            VALUES (?, ?)
        """, (nom, description))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la carrière: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_carriere(carriere_id, nom, description=None):
    """Met à jour une carrière"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE carrieres 
            SET nom = ?, description = ?
            WHERE id = ?
        """, (nom, description, carriere_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la carrière: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def delete_carriere(carriere_id):
    """Supprime une carrière"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM carrieres WHERE id=?", (carriere_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression de la carrière: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def get_all_calendriers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, titre, date_debut, date_fin, description FROM calendriers ORDER BY date_debut DESC")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_calendrier(titre, date_debut, date_fin, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO calendriers (titre, date_debut, date_fin, description)
        VALUES (?, ?, ?, ?)
    """, (titre, date_debut, date_fin, description))
    conn.commit()
    conn.close()

def delete_calendrier(calendrier_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM calendriers WHERE id=?", (calendrier_id,))
    conn.commit()
    conn.close()
