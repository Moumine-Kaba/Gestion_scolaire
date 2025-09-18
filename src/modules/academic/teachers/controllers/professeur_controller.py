from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Utiliser le gestionnaire de base de données unifié
from database.connection import get_db_connection

def connect_db():
    """Crée et retourne une connexion à la base de données SQL Server."""
    return get_db_connection()

def create_table():
    """Les tables sont déjà créées dans SQL Server lors de la migration."""
    print("✅ Table professeurs déjà créée dans SQL Server !")

# ====== CACHE MÉMOIRE ======

def preload_professeurs():
    """Précharge les professeurs en mémoire (supprimé - système de cache supprimé)"""
    try:
        pass  # Fonction supprimée car le système de cache a été supprimé
    except Exception as e:
        print(f"⚠️ Préchargement professeurs ignoré: {e}")

def get_all_professeurs():
    """
    Liste tous les professeurs de la base de données.
    Retourne une liste de dictionnaires.
    """
    # Vider le cache pour forcer une nouvelle requête

    cached = None
    if cached is not None:
        return cached
    
    try:
        conn = connect_db()
        if not conn:
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_professeur, nom, prenom, telephone, email, specialite, date_embauche, statut
            FROM professeurs
            ORDER BY nom
        """)
        
        result = []
        for row in cursor.fetchall():
            if hasattr(row, 'keys'):
                result.append(dict(row))
            else:
                columns = [desc[0] for desc in cursor.description]
                result.append(dict(zip(columns, row)))
        
        conn.close()
        
        return result
    except Exception as e:
        print(f"❌ Erreur get_all_professeurs: {e}")
        return []

def add_professeur(data):
    """
    Ajoute un nouveau professeurs.
    data : dict avec les clés ('nom', 'prenom', 'sexe', 'telephone', 'email', 'specialite', 'photo_path', 'date_embauche')
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO professeurs (nom, prenom, sexe, telephone, email, specialite, photo_path, date_embauche)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('nom', ''),
        data.get('prenom', ''),
        data.get('sexe', ''),
        data.get('telephone', ''),
        data.get('email', ''),
        data.get('specialite', ''),
        data.get('photo_path', ''),
        data.get('date_embauche', ''),
    ))
    conn.commit()
    conn.close()

def update_professeur(data):
    """
    Met à jour un professeurs existant.
    data : dict avec les mêmes clés que add_professeur + 'id'
    """
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE professeurs
        SET nom=?, prenom=?, sexe=?, telephone=?, email=?, specialite=?, photo_path=?, date_embauche=?
        WHERE id=?
    """, (
        data.get('nom', ''),
        data.get('prenom', ''),
        data.get('sexe', ''),
        data.get('telephone', ''),
        data.get('email', ''),
        data.get('specialite', ''),
        data.get('photo_path', ''),
        data.get('date_embauche', ''),
        data.get('id', ''),
    ))
    conn.commit()
    conn.close()

def delete_professeur(prof_id):
    """Supprime un professeurs selon son ID."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM professeurs WHERE id=?", (prof_id,))
    conn.commit()
    conn.close()

def get_professeur(prof_id):
    """Récupère un professeurs par son ID. Retourne un dictionnaire ou None."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nom, prenom, sexe, telephone, email, specialite, photo_path, date_embauche
        FROM professeurs
        WHERE id = ?
    """, (prof_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None