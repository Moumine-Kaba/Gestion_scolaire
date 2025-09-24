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

def get_professeurs_paginated(limit: int = 50, offset: int = 0, 
                              query: str = None, statut: str = None, 
                              specialite: str = None, principal: bool = None):
    """
    Récupère une liste paginée de professeurs avec filtres optionnels.
    - limit: nombre de lignes à récupérer
    - offset: décalage de départ
    - query: recherche texte sur nom/prenom/email/specialite
    - statut: filtre par statut exact (e.g., 'Actif', 'Inactif')
    - specialite: filtre exact par spécialité
    - principal: filtre par colonne est_professeur_principal si disponible
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à SQL Server")
            return []

        cursor = conn.cursor()

        # Vérifier existence table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'professeurs'
        """)
        if cursor.fetchone()[0] == 0:
            print("⚠️ Table 'professeurs' non trouvée dans SQL Server")
            return []

        # Déterminer si la colonne est_professeur_principal existe
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'professeurs' AND COLUMN_NAME = 'est_professeur_principal'
        """)
        has_principal = cursor.fetchone()[0] > 0

        # Construction du WHERE dynamique
        where_clauses = []
        params = []
        if query:
            where_clauses.append("(nom LIKE ? OR prenom LIKE ? OR email LIKE ? OR specialite LIKE ?)")
            like = f"%{query}%"
            params += [like, like, like, like]
        if statut:
            where_clauses.append("statut = ?")
            params.append(statut)
        if specialite:
            where_clauses.append("specialite = ?")
            params.append(specialite)
        if principal is not None and has_principal:
            where_clauses.append("est_professeur_principal = ?")
            params.append(1 if principal else 0)

        where_sql = (" WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # Sélection des colonnes
        columns = (
            "id_professeur, nom, prenom, email, telephone, specialite, statut, date_embauche"
            + (", est_professeur_principal" if has_principal else "")
        )

        # Requête paginée (SQL Server OFFSET/FETCH nécessite ORDER BY)
        query_sql = f"""
            SELECT {columns}
            FROM professeurs
            {where_sql}
            ORDER BY nom, prenom
            OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
        """
        params += [offset, limit]
        cursor.execute(query_sql, params)

        rows = cursor.fetchall()

        result = []
        for row in rows:
            # Indexation dynamique selon présence 'est_professeur_principal'
            base = {
                'id': row[0],
                'matricule': f"PROF{row[0]:04d}",
                'nom': row[1] or '',
                'prenom': row[2] or '',
                'sexe': '',
                'telephone': row[4] or '',
                'email': row[3] or '',
                'specialite': row[5] or '',
                'date_embauche': str(row[7]) if row[7] else '',
                'statut': row[6] or 'Actif',
                'adresse': '',
                'date_naissance': '',
                'photo_path': ''
            }
            if has_principal:
                base['est_professeur_principal'] = bool(row[8])
            result.append(base)

        conn.close()
        return result

    except Exception as e:
        print(f"❌ Erreur get_professeurs_paginated SQL Server: {e}")
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