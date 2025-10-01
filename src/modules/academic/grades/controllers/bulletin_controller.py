from database.connection import get_db_connection

def get_all_bulletins(eleve_id=None):
    """Récupère tous les bulletins dynamiques depuis SQL Server avec les noms associés."""
    try:
        conn = get_db_connection()
        if not conn:
            print("Impossible de se connecter a la base de donnees")
            return []
        
        cursor = conn.cursor()
        
        # Vérifier si la table bulletins existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'bulletins'
        """)
        
        table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("Table 'bulletins' n'existe pas dans SQL Server")
            return []
        
        # Construire la requête selon le paramètre
        if eleve_id:
            cursor.execute("""
                SELECT 
                    b.id_bulletin, b.id_eleve, b.periode, b.moyenne_generale, 
                    b.rang, b.appreciation, b.date_creation,
                    e.nom as eleve_nom, e.prenom as eleve_prenom,
                    c.nom_classe as classe_nom
                FROM bulletins b
                LEFT JOIN eleves e ON b.id_eleve = e.id_eleve
                LEFT JOIN classes c ON e.id_classe = c.id_classe
                WHERE b.id_eleve = ?
                ORDER BY b.periode, b.rang
            """, (eleve_id,))
        else:
            cursor.execute("""
                SELECT 
                    b.id_bulletin, b.id_eleve, b.periode, b.moyenne_generale, 
                    b.rang, b.appreciation, b.date_creation,
                    e.nom as eleve_nom, e.prenom as eleve_prenom,
                    c.nom_classe as classe_nom
                FROM bulletins b
                LEFT JOIN eleves e ON b.id_eleve = e.id_eleve
                LEFT JOIN classes c ON e.id_classe = c.id_classe
                ORDER BY c.nom_classe, b.periode, b.rang
            """)
        
        rows = cursor.fetchall()
        
        # Convertir les résultats en dictionnaires
        bulletins = []
        for row in rows:
            bulletin_dict = {
                'id': row[0],  # id_bulletin
                'id_eleve': row[1],  # id_eleve
                'periode': row[2],  # periode
                'moyenne_generale': float(row[3]) if row[3] else 0.0,  # moyenne_generale
                'rang': row[4],  # rang
                'appreciation': row[5],  # appreciation (mention)
                'date_creation': row[6],  # date_creation
                'eleve_nom': row[7],  # eleve_nom
                'eleve_prenom': row[8],  # eleve_prenom
                'classe_nom': row[9] if len(row) > 9 else None  # classe_nom
            }
            bulletins.append(bulletin_dict)
        
        conn.close()
        print(f"{len(bulletins)} bulletins dynamiques recuperes depuis SQL Server")
        return bulletins
        
    except Exception as e:
        print(f"Erreur get_all_bulletins: {e}")
        return []

def add_bulletin(eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition):
    """Ajoute un bulletin avec les bons noms de colonnes"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la colonne id_classe existe dans la table bulletins
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'bulletins' AND COLUMN_NAME = 'id_classe'
        """)
        has_id_classe = cur.fetchone()[0] > 0
        
        if has_id_classe:
            # Récupérer id_classe de l'élève
            cur.execute("SELECT id_classe FROM eleves WHERE id_eleve = ?", (eleve_id,))
            result = cur.fetchone()
            id_classe = result[0] if result else None
            
            if not id_classe:
                print(f"Classe non trouvée pour l'élève {eleve_id}")
                conn.close()
                return False
            
            # Insérer avec id_classe
            cur.execute("""
                INSERT INTO bulletins (id_eleve, id_classe, periode, moyenne_generale, appreciation, date_creation)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (eleve_id, id_classe, trimestre, moyenne, remarque, date_edition))
        else:
            # Insérer sans id_classe
            cur.execute("""
                INSERT INTO bulletins (id_eleve, periode, moyenne_generale, appreciation, date_creation)
                VALUES (?, ?, ?, ?, ?)
            """, (eleve_id, trimestre, moyenne, remarque, date_edition))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur add_bulletin: {e}")
        if conn:
            conn.close()
        return False

def update_bulletin(bulletin_id, eleve_id, annee_scolaire, trimestre, moyenne, remarque, date_edition):
    """Met à jour un bulletin avec les bons noms de colonnes"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la colonne id_classe existe dans la table bulletins
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'bulletins' AND COLUMN_NAME = 'id_classe'
        """)
        has_id_classe = cur.fetchone()[0] > 0
        
        if has_id_classe:
            # Récupérer id_classe de l'élève
            cur.execute("SELECT id_classe FROM eleves WHERE id_eleve = ?", (eleve_id,))
            result = cur.fetchone()
            id_classe = result[0] if result else None
            
            # Mettre à jour avec id_classe
            cur.execute("""
                UPDATE bulletins 
                SET id_eleve=?, id_classe=?, periode=?, moyenne_generale=?, appreciation=?, date_creation=?
                WHERE id_bulletin=?
            """, (eleve_id, id_classe, trimestre, moyenne, remarque, date_edition, bulletin_id))
        else:
            # Mettre à jour sans id_classe
            cur.execute("""
                UPDATE bulletins 
                SET id_eleve=?, periode=?, moyenne_generale=?, appreciation=?, date_creation=?
                WHERE id_bulletin=?
            """, (eleve_id, trimestre, moyenne, remarque, date_edition, bulletin_id))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur update_bulletin: {e}")
        if conn:
            conn.close()
        return False

def delete_bulletin(bulletin_id):
    """Supprime un bulletin"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM bulletins WHERE id_bulletin=?", (bulletin_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Erreur delete_bulletin: {e}")
        if conn:
            conn.close()
        return False
