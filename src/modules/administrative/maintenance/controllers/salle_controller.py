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

# Chemin relatif vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'database', 'edumanager.db')

def _init_salles_table():
    """Initialise la table salles si elle n'existe pas."""
    try:
        conn = _connect()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        
        # Vérifier si la table existe
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'salles'
        """)
        
        if cursor.fetchone()[0] == 0:
            # Créer la table salles
            cursor.execute("""
                CREATE TABLE salles (
                    id_salle INT IDENTITY(1,1) PRIMARY KEY,
                    nom_salle NVARCHAR(100) NOT NULL,
                    capacite INT NOT NULL,
                    type_salle NVARCHAR(50),
                    equipements NVARCHAR(500),
                    statut NVARCHAR(50) DEFAULT 'Disponible',
                    date_creation DATETIME DEFAULT GETDATE()
                )
            """)
            conn.commit()
            print("✅ Table salles créée")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur création table salles: {e}")
        return False

def _connect():
    """Crée et retourne une connexion à la base de données configurée."""
    conn = get_db_connection()
    # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server  # Permet d'accéder aux données par les noms de colonnes
    # PRAGMA supprimés pour SQL Server
    return conn

# ====== CACHE MÉMOIRE ======

def preload_salles():
    """Précharge les salles en mémoire (supprimé - système de cache supprimé)"""
    try:
        pass  # Fonction supprimée car le système de cache a été supprimé
    except Exception as e:
        print(f"⚠️ Préchargement salles ignoré: {e}")

def get_all_salles():
    """Liste toutes les salles en tant que dictionnaires."""
    try:
        # Initialiser la table si nécessaire
        _init_salles_table()
        
        if None is not None:
            return _CACHE["salles_all"]
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""
                SELECT id_salle, nom_salle, capacite, type_salle, equipements, statut, date_creation
                FROM salles
                ORDER BY nom_salle
            """)
            rows = cur.fetchall()
            data = [dict(row) for row in rows]
            
            return data
    except Exception as e:
        print(f"[Salle] Erreur get_all_salles: {e}")
        return []

def add_salle(nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
    """Ajoute une nouvelle salles."""
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""INSERT INTO salles (nom_salle, capacite, type_salle, equipements, statut, date_creation)
                VALUES (?, ?, ?, ?, ?, GETDATE())
            """, (nom_salle, capacite, type_salle, equipements, statut))
            conn.commit()
            conn.close()
            
            return True
    except Exception as e:
        print(f"[Salle] Erreur add_salle: {e}")
        return False

def update_salle(id_salle, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
    """Met à jour une salles existante."""
    try:
        conn = _connect()

        if not conn:

            print("❌ Impossible de se connecter à la base de données")

            return

            cur = conn.cursor()
            cur.execute("""
                UPDATE salles
                SET nom_salle=?, capacite=?, type_salle=?, equipements=?, statut=?
                WHERE id_salle=?
            """, (nom_salle, capacite, type_salle, equipements, statut, id_salle))
            conn.commit()
            conn.close()
            
            return True
    except Exception as e:
        print(f"[Salle] Erreur update_salle: {e}")
        return False

class SalleController:
    """Contrôleur pour la gestion des salles."""
    
    def __init__(self):
        self.db_path = DB_PATH
        self.conn = None
        self._connect()
    
    def _connect(self):
        """Établit la connexion à la base de données."""
        try:
            self.conn = get_db_connection()
            # self.conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        except Exception as e:
            print(f"[SalleController] Erreur de connexion: {e}")
            self.conn = None
    
    def get_all_salles(self):
        """Retourne toutes les salles."""
        return get_all_salles()
    
    def add_salle(self, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
        """Ajoute une nouvelle salles."""
        return add_salle(nom_salle, capacite, type_salle, equipements, statut)
    
    def update_salle(self, id_salle, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
        """Met à jour une salles."""
        return update_salle(id_salle, nom_salle, capacite, type_salle, equipements, statut)
    
    def delete_salle(self, id_salle):
        """Supprime une salles."""
        return delete_salle(id_salle)
    
    def get_salles_stats(self):
        """Retourne les statistiques des salles."""
        try:
            salles = self.get_all_salles()
            type_counts = {}
            total_capacite = 0
            
            for salles in salles:
                type_salle = salles.get('type_salle', 'Non spécifié')
                type_counts[type_salle] = type_counts.get(type_salle, 0) + 1
                total_capacite += salles.get('capacite', 0)
            
            return type_counts, total_capacite
        except Exception as e:
            print(f"[SalleController] Erreur get_salles_stats: {e}")