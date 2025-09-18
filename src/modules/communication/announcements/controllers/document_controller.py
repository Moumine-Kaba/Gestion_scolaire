from database.connection import get_db_connection

def get_all_documents():
    """Retourne tous les documents"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, nom, chemin, type, date_ajout FROM documents ORDER BY date_ajout DESC")
        rows = cur.fetchall()
        
        # Convertir en dictionnaires pour SQL Server
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des documents: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_document(nom, chemin, type_, date_ajout):
    """Ajoute un nouveau document"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO documents (nom, chemin, type, date_ajout)
            VALUES (?, ?, ?, ?)
        """, (nom, chemin, type_, date_ajout))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout du document: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_document(doc_id, nom, chemin, type_, date_ajout):
    """Met à jour un document"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE documents 
            SET nom = ?, chemin = ?, type = ?, date_ajout = ?
            WHERE id = ?
        """, (nom, chemin, type_, date_ajout, doc_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du document: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def delete_document(doc_id):
    """Supprime un document"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM documents WHERE id=?", (doc_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du document: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()