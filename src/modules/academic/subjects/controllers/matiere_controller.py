from database.connection import get_db_connection
import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

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
    Récupère toutes les matières depuis SQL Server.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        
        # Vérifier si la table matieres existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'matieres'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("⚠️ Table 'matieres' n'existe pas dans SQL Server")
            return []
        
        # Récupérer toutes les matières (nous avons exactement 10 matières guinéennes)
        cursor.execute("""
            SELECT id_matiere, nom_matiere, description, coefficient, statut, date_creation
            FROM matieres
            ORDER BY nom_matiere
        """)
        
        rows = cursor.fetchall()
        
        # Convertir les résultats en dictionnaires
        matieres = []
        for row in rows:
            matiere_dict = {
                'id_matiere': row[0],  # id_matiere
                'nom_matiere': row[1],  # nom_matiere
                'code_matiere': row[2] if len(row) > 2 else '',  # description/code
                'description': row[2] if len(row) > 2 else '',  # description
                'coefficient': float(row[3]) if len(row) > 3 and row[3] else 1.0,  # coefficient
                'statut': row[4] if len(row) > 4 else 'Actif',  # statut
                'date_creation': row[5] if len(row) > 5 else None  # date_creation
            }
            matieres.append(matiere_dict)
        
        conn.close()
        print(f"✅ {len(matieres)} matières guinéennes récupérées depuis SQL Server")
        return matieres
        
    except Exception as e:
        print(f"❌ Erreur get_all_matieres: {e}")
        return []

def search_matieres(q):
    """
    Recherche des matières par nom ou description, sans tenir compte de la casse.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        like_term = f"%{q.strip()}%"
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_matiere, nom_matiere, description, coefficient, statut, date_creation
            FROM matieres
            WHERE nom_matiere LIKE ? OR description LIKE ?
            ORDER BY nom_matiere ASC
        """, (like_term, like_term))
        
        rows = cursor.fetchall()
        
        # Convertir les résultats en dictionnaires
        matieres = []
        for row in rows:
            matiere_dict = {
                'id_matiere': row[0],
                'nom_matiere': row[1],
                'code_matiere': row[2] if len(row) > 2 else '',
                'description': row[2] if len(row) > 2 else '',
                'coefficient': float(row[3]) if len(row) > 3 and row[3] else 1.0,
                'statut': row[4] if len(row) > 4 else 'Actif',
                'date_creation': row[5] if len(row) > 5 else None
            }
            matieres.append(matiere_dict)
        
        conn.close()
        return matieres
        
    except Exception as e:
        print(f"❌ Erreur lors de la recherche des matières : {e}")
        return []

def add_matiere(nom, code=""):
    """
    Ajoute une nouvelle matière à la base de données.
    Retourne True en cas de succès, False sinon.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False

        cursor = conn.cursor()
        cursor.execute("INSERT INTO matieres (nom_matiere, description, coefficient, statut) VALUES (?, ?, 1.0, 'Actif')", (nom, code))
        conn.commit()
        conn.close()
        print(f"✅ Matière '{nom}' ajoutée avec succès")
        return True
                
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la matière : {e}")
        return False

def update_matiere(matiere_id, nom, code):
    """
    Met à jour une matière existante par son ID.
    Retourne True en cas de succès, False sinon.
    """
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False

        cursor = conn.cursor()
        cursor.execute("UPDATE matieres SET nom_matiere = ?, description = ? WHERE id_matiere = ?", (nom, code, matiere_id))
        conn.commit()
        conn.close()
        print(f"✅ Matière '{nom}' mise à jour avec succès")
        return True
                
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la matière : {e}")
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
            return False

        cursor = conn.cursor()
        cursor.execute("DELETE FROM matieres WHERE id_matiere = ?", (matiere_id,))
        conn.commit()
        conn.close()
        print(f"✅ Matière #{matiere_id} supprimée avec succès")
        return True
                
    except Exception as e:
        print(f"❌ Erreur lors de la suppression de la matière : {e}")
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