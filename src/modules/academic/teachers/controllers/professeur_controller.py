import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

# Utiliser le gestionnaire de base de données SQL Server
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
    Liste tous les professeurs de la base de données SQL Server.
    Retourne une liste de dictionnaires.
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return []
        
        cursor = conn.cursor()
        
        # Vérifier si la table professeurs existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'professeurs'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("⚠️ Table 'professeurs' non trouvée dans SQL Server")
            return []
        
        # Récupérer tous les professeurs
        cursor.execute("""
            SELECT id_professeur, nom, prenom, email, telephone, specialite, statut, date_embauche
            FROM professeurs
            ORDER BY nom, prenom
        """)
        
        rows = cursor.fetchall()
        
        # Convertir en liste de dictionnaires
        result = []
        for row in rows:
            prof_dict = {
                'id': row[0],  # id_professeur
                'matricule': f"PROF{row[0]:04d}",  # Générer un matricule basé sur l'ID
                'nom': row[1] or '',
                'prenom': row[2] or '',
                'sexe': '',  # Pas disponible dans la table
                'telephone': row[4] or '',
                'email': row[3] or '',
                'specialite': row[5] or '',
                'date_embauche': str(row[7]) if row[7] else '',
                'statut': row[6] or 'Actif',
                'adresse': '',  # Pas disponible dans la table
                'date_naissance': '',  # Pas disponible dans la table
                'photo_path': ''  # Pas de photo dans la structure actuelle
            }
            result.append(prof_dict)
        
        conn.close()
        print(f"✅ {len(result)} professeurs récupérés depuis SQL Server")
        return result
        
    except Exception as e:
        print(f"❌ Erreur get_all_professeurs SQL Server: {e}")
        return []

def add_professeur(data):
    """
    Ajoute un nouveau professeur dans SQL Server.
    data : dict avec les clés ('nom', 'prenom', 'sexe', 'telephone', 'email', 'specialite', 'date_embauche', 'statut', 'matricule', 'adresse', 'date_naissance')
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return False
        
        cursor = conn.cursor()
        
        # Générer un matricule si non fourni
        matricule = data.get('matricule', '')
        if not matricule:
            # Générer un matricule automatique
            cursor.execute("SELECT COUNT(*) FROM professeurs")
            count = cursor.fetchone()[0]
            matricule = f"PROF{count + 1:04d}"
        
        cursor.execute("""
            INSERT INTO professeurs (nom, prenom, email, telephone, specialite, statut)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data.get('nom', ''),
            data.get('prenom', ''),
            data.get('email', ''),
            data.get('telephone', ''),
            data.get('specialite', ''),
            data.get('statut', 'Actif')
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Professeur ajouté avec matricule: {matricule}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur add_professeur SQL Server: {e}")
        return False

def update_professeur(prof_id, data):
    """
    Met à jour un professeur existant dans SQL Server.
    prof_id : ID du professeur à modifier
    data : dict avec les nouvelles données
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return False
        
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE professeurs 
            SET nom=?, prenom=?, email=?, telephone=?, specialite=?, statut=?
            WHERE id_professeur=?
        """, (
            data.get('nom', ''),
            data.get('prenom', ''),
            data.get('email', ''),
            data.get('telephone', ''),
            data.get('specialite', ''),
            data.get('statut', 'Actif'),
            prof_id
        ))
        
        conn.commit()
        conn.close()
        print(f"✅ Professeur {prof_id} mis à jour dans SQL Server")
        return True
        
    except Exception as e:
        print(f"❌ Erreur update_professeur SQL Server: {e}")
        return False

def delete_professeur(prof_id):
    """Supprime un professeur selon son ID dans SQL Server."""
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return False
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professeurs WHERE id_professeur=?", (prof_id,))
        conn.commit()
        conn.close()
        print(f"✅ Professeur {prof_id} supprimé de SQL Server")
        return True
        
    except Exception as e:
        print(f"❌ Erreur delete_professeur SQL Server: {e}")
        return False

def get_professeur(prof_id):
    """Récupère un professeur par son ID depuis SQL Server. Retourne un dictionnaire ou None."""
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return None
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_professeur, nom, prenom, email, telephone, specialite, statut, date_embauche
            FROM professeurs
            WHERE id_professeur = ?
        """, (prof_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            prof_dict = {
                'id': row[0],  # id_professeur
                'matricule': f"PROF{row[0]:04d}",  # Générer un matricule basé sur l'ID
                'nom': row[1] or '',
                'prenom': row[2] or '',
                'sexe': '',  # Pas disponible dans la table
                'telephone': row[4] or '',
                'email': row[3] or '',
                'specialite': row[5] or '',
                'date_embauche': str(row[7]) if row[7] else '',
                'statut': row[6] or 'Actif',
                'adresse': '',  # Pas disponible dans la table
                'date_naissance': '',  # Pas disponible dans la table
                'photo_path': ''  # Pas de photo dans la structure actuelle
            }
            return prof_dict
        
        return None
        
    except Exception as e:
        print(f"❌ Erreur get_professeur SQL Server: {e}")
        return None