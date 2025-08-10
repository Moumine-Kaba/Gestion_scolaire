from utils.db_utils import get_connection

def get_all_subjects():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nom FROM matieres
        ORDER BY nom
    """)
    result = cursor.fetchall()
    conn.close()
    return result

# add_subject, update_subject, delete_subject peuvent être ajoutés aussi.
