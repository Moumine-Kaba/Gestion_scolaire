import sqlite3
import os

# Chemin relatif vers la base de données
DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'database', 'edumanager.db')

def _connect():
    """Crée et retourne une connexion à la base de données configurée."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux données par les noms de colonnes
    return conn

def get_all_salles():
    """Liste toutes les salles en tant que dictionnaires."""
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id_salle, nom_salle, capacite, type_salle, equipements, statut, date_creation
                FROM salles
                ORDER BY nom_salle
            """)
            rows = cur.fetchall()
            return [dict(row) for row in rows]
    except Exception as e:
        print(f"[Salle] Erreur get_all_salles: {e}")
        return []

def add_salle(nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
    """Ajoute une nouvelle salle."""
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO salles (nom_salle, capacite, type_salle, equipements, statut, date_creation)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            """, (nom_salle, capacite, type_salle, equipements, statut))
            conn.commit()
            return True
    except Exception as e:
        print(f"[Salle] Erreur add_salle: {e}")
        return False

def update_salle(id_salle, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
    """Met à jour une salle existante."""
    try:
        with _connect() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE salles
                SET nom_salle=?, capacite=?, type_salle=?, equipements=?, statut=?
                WHERE id_salle=?
            """, (nom_salle, capacite, type_salle, equipements, statut, id_salle))
            conn.commit()
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
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            print(f"[SalleController] Erreur de connexion: {e}")
            self.conn = None
    
    def get_all_salles(self):
        """Retourne toutes les salles."""
        return get_all_salles()
    
    def add_salle(self, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
        """Ajoute une nouvelle salle."""
        return add_salle(nom_salle, capacite, type_salle, equipements, statut)
    
    def update_salle(self, id_salle, nom_salle, capacite, type_salle, equipements="", statut="Disponible"):
        """Met à jour une salle."""
        return update_salle(id_salle, nom_salle, capacite, type_salle, equipements, statut)
    
    def delete_salle(self, id_salle):
        """Supprime une salle."""
        return delete_salle(id_salle)
    
    def get_salles_stats(self):
        """Retourne les statistiques des salles."""
        try:
            salles = self.get_all_salles()
            type_counts = {}
            total_capacite = 0
            
            for salle in salles:
                type_salle = salle.get('type_salle', 'Non spécifié')
                type_counts[type_salle] = type_counts.get(type_salle, 0) + 1
                total_capacite += salle.get('capacite', 0)
            
            return type_counts, total_capacite
        except Exception as e:
            print(f"[SalleController] Erreur get_salles_stats: {e}")
            return {}, 0