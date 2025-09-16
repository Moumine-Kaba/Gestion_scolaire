# -*- coding: utf-8 -*-
"""
Utilitaires de base de données centralisés pour EduManager+
- Connexions centralisées
- Fonctions utilitaires communes
- Gestion des erreurs
"""

import sqlite3
import os
import sys
from typing import Optional, List, Dict, Any

# Ajouter le chemin racine au sys.path
root_path = os.path.join(os.path.dirname(__file__), "..", "..")
if root_path not in sys.path:
    sys.path.insert(0, root_path)

from src.core.paths import DATABASE_PATH

def get_db_connection() -> Optional[sqlite3.Connection]:
    """
    Retourne une connexion à la base de données centralisée
    
    Returns:
        sqlite3.Connection: Connexion à la base de données ou None en cas d'erreur
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"⚠️ Erreur connexion DB: {e}")
        return None

def get_connection() -> Optional[sqlite3.Connection]:
    """
    Alias pour get_db_connection (compatibilité)
    
    Returns:
        sqlite3.Connection: Connexion à la base de données ou None en cas d'erreur
    """
    return get_db_connection()

def execute_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """
    Exécute une requête SELECT et retourne les résultats
    
    Args:
        query (str): Requête SQL
        params (tuple): Paramètres de la requête
        
    Returns:
        List[Dict[str, Any]]: Liste des résultats
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        # Convertir les Row en dictionnaires
        return [dict(row) for row in results]
    except sqlite3.Error as e:
        print(f"⚠️ Erreur requête: {e}")
        return []
    finally:
        if conn:
            conn.close()

def execute_update(query: str, params: tuple = ()) -> bool:
    """
    Exécute une requête INSERT/UPDATE/DELETE
    
    Args:
        query (str): Requête SQL
        params (tuple): Paramètres de la requête
        
    Returns:
        bool: True si succès, False sinon
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"⚠️ Erreur mise à jour: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def table_exists(table_name: str) -> bool:
    """
    Vérifie si une table existe dans la base de données
    
    Args:
        table_name (str): Nom de la table
        
    Returns:
        bool: True si la table existe
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name=?
        """, (table_name,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"⚠️ Erreur vérification table: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_table_columns(table_name: str) -> List[str]:
    """
    Retourne la liste des colonnes d'une table
    
    Args:
        table_name (str): Nom de la table
        
    Returns:
        List[str]: Liste des noms de colonnes
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        return columns
    except sqlite3.Error as e:
        print(f"⚠️ Erreur récupération colonnes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_tables() -> List[str]:
    """
    Retourne la liste de toutes les tables de la base de données
    
    Returns:
        List[str]: Liste des noms de tables
    """
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"⚠️ Erreur récupération tables: {e}")
        return []
    finally:
        if conn:
            conn.close()

def backup_database(backup_path: str) -> bool:
    """
    Crée une sauvegarde de la base de données
    
    Args:
        backup_path (str): Chemin de la sauvegarde
        
    Returns:
        bool: True si succès
    """
    try:
        import shutil
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"✅ Sauvegarde créée: {backup_path}")
        return True
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde: {e}")
        return False

def restore_database(backup_path: str) -> bool:
    """
    Restaure la base de données depuis une sauvegarde
    
    Args:
        backup_path (str): Chemin de la sauvegarde
        
    Returns:
        bool: True si succès
    """
    try:
        import shutil
        shutil.copy2(backup_path, DATABASE_PATH)
        print(f"✅ Base de données restaurée depuis: {backup_path}")
        return True
    except Exception as e:
        print(f"⚠️ Erreur restauration: {e}")
        return False

# Fonctions utilitaires pour les vues communes
def get_all_eleves() -> List[Dict[str, Any]]:
    """Retourne tous les élèves"""
    return execute_query("SELECT * FROM eleves ORDER BY nom, prenom")

def get_all_professeurs() -> List[Dict[str, Any]]:
    """Retourne tous les professeurs"""
    return execute_query("SELECT * FROM professeurs ORDER BY nom, prenom")

def get_all_classes() -> List[Dict[str, Any]]:
    """Retourne toutes les classes"""
    return execute_query("SELECT * FROM classe ORDER BY nom")

def get_all_matieres() -> List[Dict[str, Any]]:
    """Retourne toutes les matières"""
    return execute_query("SELECT * FROM matieres ORDER BY nom")

def get_all_notes() -> List[Dict[str, Any]]:
    """Retourne toutes les notes"""
    return execute_query("SELECT * FROM notes ORDER BY date_creation DESC")

def get_all_presences() -> List[Dict[str, Any]]:
    """Retourne toutes les présences"""
    return execute_query("SELECT * FROM presences ORDER BY date DESC")

def get_all_bulletins() -> List[Dict[str, Any]]:
    """Retourne tous les bulletins"""
    return execute_query("SELECT * FROM bulletins ORDER BY date_creation DESC")

def get_all_paiements() -> List[Dict[str, Any]]:
    """Retourne tous les paiements"""
    return execute_query("SELECT * FROM paiements ORDER BY date_paiement DESC")

def get_all_salles() -> List[Dict[str, Any]]:
    """Retourne toutes les salles"""
    return execute_query("SELECT * FROM salles ORDER BY nom")

def get_all_utilisateurs() -> List[Dict[str, Any]]:
    """Retourne tous les utilisateurs"""
    return execute_query("SELECT * FROM utilisateurs ORDER BY username")

# Fonctions de recherche
def search_eleves(search_term: str) -> List[Dict[str, Any]]:
    """Recherche des élèves par nom ou prénom"""
    query = """
        SELECT * FROM eleves 
        WHERE nom LIKE ? OR prenom LIKE ? OR numero_eleve LIKE ?
        ORDER BY nom, prenom
    """
    search_pattern = f"%{search_term}%"
    return execute_query(query, (search_pattern, search_pattern, search_pattern))

def search_professeurs(search_term: str) -> List[Dict[str, Any]]:
    """Recherche des professeurs par nom ou prénom"""
    query = """
        SELECT * FROM professeurs 
        WHERE nom LIKE ? OR prenom LIKE ? OR specialite LIKE ?
        ORDER BY nom, prenom
    """
    search_pattern = f"%{search_term}%"
    return execute_query(query, (search_pattern, search_pattern, search_pattern))

def search_classes(search_term: str) -> List[Dict[str, Any]]:
    """Recherche des classes par nom ou niveau"""
    query = """
        SELECT * FROM classe 
        WHERE nom LIKE ? OR niveau LIKE ?
        ORDER BY nom
    """
    search_pattern = f"%{search_term}%"
    return execute_query(query, (search_pattern, search_pattern))

# Fonctions de statistiques
def get_stats_eleves() -> Dict[str, Any]:
    """Retourne les statistiques des élèves"""
    total = execute_query("SELECT COUNT(*) as count FROM eleves")[0]['count']
    par_classe = execute_query("""
        SELECT c.nom as classe, COUNT(e.id) as count 
        FROM classe c 
        LEFT JOIN eleves e ON c.id = e.classe_id 
        GROUP BY c.id, c.nom 
        ORDER BY c.nom
    """)
    return {
        'total': total,
        'par_classe': par_classe
    }

def get_stats_professeurs() -> Dict[str, Any]:
    """Retourne les statistiques des professeurs"""
    total = execute_query("SELECT COUNT(*) as count FROM professeurs")[0]['count']
    par_specialite = execute_query("""
        SELECT specialite, COUNT(*) as count 
        FROM professeurs 
        GROUP BY specialite 
        ORDER BY specialite
    """)
    return {
        'total': total,
        'par_specialite': par_specialite
    }

def get_stats_classes() -> Dict[str, Any]:
    """Retourne les statistiques des classes"""
    total = execute_query("SELECT COUNT(*) as count FROM classe")[0]['count']
    par_niveau = execute_query("""
        SELECT niveau, COUNT(*) as count 
        FROM classe 
        GROUP BY niveau 
        ORDER BY niveau
    """)
    return {
        'total': total,
        'par_niveau': par_niveau
    }

if __name__ == "__main__":
    # Test des fonctions
    print("🔍 Test des utilitaires de base de données...")
    
    # Test de connexion
    conn = get_db_connection()
    if conn:
        print("✅ Connexion à la base de données réussie")
        conn.close()
    else:
        print("❌ Connexion à la base de données échouée")
    
    # Test des tables
    tables = get_all_tables()
    print(f"📋 Tables disponibles: {tables}")
    
    # Test des statistiques
    if 'eleves' in tables:
        stats = get_stats_eleves()
        print(f"📊 Statistiques élèves: {stats}")
    
    print("✅ Test terminé")
