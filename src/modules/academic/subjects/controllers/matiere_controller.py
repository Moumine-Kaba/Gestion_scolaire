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

# ====== DB PATH from persistent information ======
# Le chemin de la base de données est conservé comme demandé.

def _connect():
    """
    Crée et retourne une connexion à la base de données.
    Utilise 'with' pour garantir la fermeture automatique de la connexion.
    """
    try:
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

# ====== CACHE MÉMOIRE ======

def preload_matieres():
    """Précharge les matières en mémoire (supprimé - système de cache supprimé)"""
    try:
        pass  # Fonction supprimée car le système de cache a été supprimé
    except Exception as e:
        print(f"⚠️ Préchargement matières ignoré: {e}")

def get_all_matieres():
    """
    Récupère toutes les matières de la base de données, triées par nom.
    """
    try:
        if None is not None:
            return _CACHE["matieres_all"]
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id_matiere as id, nom_matiere as nom, code_matiere FROM matieres ORDER BY nom_matiere ASC")
                matieres = cursor.fetchall()
                data = [dict(m) for m in matieres]
                
                return data
    except Exception as e:
        print(f"Erreur lors de la récupération de toutes les matières : {e}")
    return []

def search_matieres(q):
    """
    Recherche des matières par nom ou description, sans tenir compte de la casse.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            if conn:
                like_term = f"%{q.strip()}%"
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id_matiere as id, nom_matiere as nom, code_matiere
                    FROM matieres
                    WHERE nom_matiere LIKE ? COLLATE NOCASE
                       OR code_matiere LIKE ? COLLATE NOCASE
                    ORDER BY nom_matiere ASC
                """, (like_term, like_term))
                matieres = cursor.fetchall()
                return [dict(m) for m in matieres]
    except Exception as e:
        print(f"Erreur lors de la recherche des matières : {e}")
    return []

def add_matiere(nom, description=""):
    """
    Ajoute une nouvelle matière à la base de données.
    Retourne True en cas de succès, False sinon.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            if conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO matieres (nom, description) VALUES (?, ?)", (nom, description))
                conn.commit()
                conn.close()
                
                return True
    except Exception as e:
        print(f"Erreur lors de l'ajout de la matière : {e}")
    return False

def update_matiere(matiere_id, nom, description):
    """
    Met à jour une matière existante par son ID.
    Retourne True en cas de succès, False sinon.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE matieres SET nom = ?, description = ? WHERE id = ?", (nom, description, matiere_id))
                conn.commit()
                conn.close()
                
                return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de la matière : {e}")
    return False

def delete_matiere(matiere_id):
    """
    Supprime une matière de la base de données par son ID.
    Retourne True en cas de succès, False sinon.
    """
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM matieres WHERE id_matiere = ?", (matiere_id,))
                conn.commit()
                conn.close()
                
                return True
    except Exception as e:
        print(f"Erreur lors de la suppression de la matière : {e}")
    return False

def preload_matieres_cache():
    """Précharge le cache des matières pour optimiser les performances."""
    try:
        conn = _connect()
        if not conn:
            return {}
        
        cursor = conn.cursor()
        cursor.execute("SELECT id_matiere, nom_matiere FROM matieres WHERE statut = 'Active'")
        matieres = cursor.fetchall()
        
        cache = {}
        for matiere in matieres:
            cache[matiere[0]] = matiere[1]
        
        conn.close()
        return cache
    except Exception as e:
        print(f"⚠️ Erreur préchargement cache matières: {e}")
        return {}