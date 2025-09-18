from database.connection import get_db_connection

def get_all_messages():
    """Retourne tous les messages"""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, expediteur_id, destinataire_id, contenu, date_envoi
            FROM messages ORDER BY date_envoi DESC
        """)
        rows = cur.fetchall()
        
        # Convertir en dictionnaires pour SQL Server
        columns = [desc[0] for desc in cur.description] if cur.description else []
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        print(f"Erreur lors de la récupération des messages: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_message(expediteur_id, destinataire_id, contenu, date_envoi):
    """Ajoute un nouveau message"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO messages (expediteur_id, destinataire_id, contenu, date_envoi)
            VALUES (?, ?, ?, ?)
        """, (expediteur_id, destinataire_id, contenu, date_envoi))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de l'ajout du message: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_message(message_id, expediteur_id, destinataire_id, contenu, date_envoi):
    """Met à jour un message"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE messages 
            SET expediteur_id = ?, destinataire_id = ?, contenu = ?, date_envoi = ?
            WHERE id = ?
        """, (expediteur_id, destinataire_id, contenu, date_envoi, message_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du message: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def delete_message(message_id):
    """Supprime un message"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM messages WHERE id=?", (message_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Erreur lors de la suppression du message: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()