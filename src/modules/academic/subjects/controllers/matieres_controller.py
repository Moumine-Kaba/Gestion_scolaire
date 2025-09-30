# -*- coding: utf-8 -*-
"""
Contrôleur des Matières - Système Réorganisé
EduManager+ - Gestion des matières par niveau et classe
"""

from database.connection import get_db_connection
from typing import Dict, List, Optional

def get_all_niveaux() -> Dict[int, Dict]:
    """Récupère tous les niveaux"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_niveau, nom_niveau, description, date_creation
            FROM niveaux
            ORDER BY nom_niveau
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        niveaux = {}
        for row in rows:
            niveaux[row[0]] = {
                'id_niveau': row[0],
                'nom_niveau': row[1],
                'description': row[2],
                'date_creation': row[3]
            }
        
        print(f"✅ {len(niveaux)} niveaux récupérés depuis SQL Server")
        return niveaux
        
    except Exception as e:
        print(f"❌ Erreur get_all_niveaux: {e}")
        return {}

def get_all_matieres() -> List[Dict]:
    """Récupère toutes les matières"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_matiere, nom_matiere, coefficient, description, statut, date_creation
            FROM matieres
            WHERE statut = 'active'
            ORDER BY nom_matiere
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        matieres = []
        for row in rows:
            matieres.append({
                'id_matiere': row[0],
                'nom_matiere': row[1],
                'coefficient': row[2],
                'description': row[3],
                'statut': row[4],
                'date_creation': row[5]
            })
        
        print(f"✅ {len(matieres)} matières récupérées depuis SQL Server")
        return matieres
        
    except Exception as e:
        print(f"❌ Erreur get_all_matieres: {e}")
        return []

def get_classes_by_niveau(niveau_nom: str) -> Dict[int, Dict]:
    """Récupère les classes d'un niveau donné"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id_classe, c.nom_classe, c.niveau
            FROM classes c
            WHERE c.niveau = ?
            ORDER BY c.nom_classe
        """, (niveau_nom,))
        
        rows = cursor.fetchall()
        conn.close()
        
        classes = {}
        for row in rows:
            classes[row[0]] = {
                'id_classe': row[0],
                'nom_classe': row[1],
                'niveau': row[2]
            }
        
        print(f"✅ {len(classes)} classes récupérées pour le niveau {niveau_nom}")
        return classes
        
    except Exception as e:
        print(f"❌ Erreur get_classes_by_niveau: {e}")
        return {}

def get_matieres_by_classe(classe_id: int) -> List[Dict]:
    """Récupère les matières d'une classe donnée"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cm.id_classe_matiere, cm.id_classe, cm.id_matiere, cm.id_professeur,
                   cm.coefficient_classe, cm.statut,
                   c.nom_classe, m.nom_matiere, p.nom + ' ' + p.prenom as professeur_nom
            FROM classe_matieres cm
            LEFT JOIN classes c ON cm.id_classe = c.id_classe
            LEFT JOIN matieres m ON cm.id_matiere = m.id_matiere
            LEFT JOIN professeurs p ON cm.id_professeur = p.id_professeur
            WHERE cm.id_classe = ? AND cm.statut = 'active'
            ORDER BY m.nom_matiere
        """, (classe_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        matieres = []
        for row in rows:
            matieres.append({
                'id_classe_matiere': row[0],
                'id_classe': row[1],
                'id_matiere': row[2],
                'id_professeur': row[3],
                'coefficient_classe': row[4],
                'statut': row[5],
                'classe_nom': row[6],
                'matiere_nom': row[7],
                'professeur_nom': row[8] if row[8] else 'Non assigné'
            })
        
        print(f"✅ {len(matieres)} matières récupérées pour la classe {classe_id}")
        return matieres
        
    except Exception as e:
        print(f"❌ Erreur get_matieres_by_classe: {e}")
        return []

def get_classe_matieres_by_niveau(niveau_nom: str) -> List[Dict]:
    """Récupère toutes les associations classe-matière d'un niveau"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cm.id_classe_matiere, cm.id_classe, cm.id_matiere, cm.id_professeur,
                   cm.coefficient_classe, cm.statut,
                   c.nom_classe, m.nom_matiere, p.nom + ' ' + p.prenom as professeur_nom
            FROM classe_matieres cm
            LEFT JOIN classes c ON cm.id_classe = c.id_classe
            LEFT JOIN matieres m ON cm.id_matiere = m.id_matiere
            LEFT JOIN professeurs p ON cm.id_professeur = p.id_professeur
            WHERE c.niveau = ? AND cm.statut = 'active'
            ORDER BY c.nom_classe, m.nom_matiere
        """, (niveau_nom,))
        
        rows = cursor.fetchall()
        conn.close()
        
        associations = []
        for row in rows:
            associations.append({
                'id_classe_matiere': row[0],
                'id_classe': row[1],
                'id_matiere': row[2],
                'id_professeur': row[3],
                'coefficient_classe': row[4],
                'statut': row[5],
                'classe_nom': row[6],
                'matiere_nom': row[7],
                'professeur_nom': row[8] if row[8] else 'Non assigné'
            })
        
        print(f"✅ {len(associations)} associations récupérées pour le niveau {niveau_nom}")
        return associations
        
    except Exception as e:
        print(f"❌ Erreur get_classe_matieres_by_niveau: {e}")
        return []

def create_matiere(nom_matiere: str, coefficient: float, description: str = None) -> Optional[int]:
    """Crée une nouvelle matière"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return None
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO matieres (nom_matiere, coefficient, description)
            VALUES (?, ?, ?)
        """, (nom_matiere, coefficient, description or f"Matière {nom_matiere}"))
        
        # Récupérer l'ID de la matière créée
        cursor.execute("SELECT @@IDENTITY")
        matiere_id = cursor.fetchone()[0]
        
        conn.commit()
        conn.close()
        
        print(f"✅ Matière '{nom_matiere}' créée avec l'ID {matiere_id}")
        return matiere_id
        
    except Exception as e:
        print(f"❌ Erreur create_matiere: {e}")
        return None

def create_classe_matiere(classe_id: int, matiere_id: int, professeur_id: int = None, coefficient: float = 1.0) -> bool:
    """Crée une association classe-matière"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO classe_matieres (id_classe, id_matiere, id_professeur, coefficient_classe)
            VALUES (?, ?, ?, ?)
        """, (classe_id, matiere_id, professeur_id, coefficient))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Association classe-matière créée: classe {classe_id}, matière {matiere_id}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur create_classe_matiere: {e}")
        return False

def update_matiere(matiere_id: int, nom_matiere: str = None, coefficient: float = None, description: str = None) -> bool:
    """Met à jour une matière"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        
        # Construire la requête dynamiquement
        updates = []
        params = []
        
        if nom_matiere is not None:
            updates.append("nom_matiere = ?")
            params.append(nom_matiere)
        
        if coefficient is not None:
            updates.append("coefficient = ?")
            params.append(coefficient)
        
        if description is not None:
            updates.append("description = ?")
            params.append(description)
        
        if not updates:
            return True  # Rien à mettre à jour
        
        query = f"UPDATE matieres SET {', '.join(updates)} WHERE id_matiere = ?"
        params.append(matiere_id)
        
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        print(f"✅ Matière {matiere_id} mise à jour")
        return True
        
    except Exception as e:
        print(f"❌ Erreur update_matiere: {e}")
        return False

def delete_matiere(matiere_id: int) -> bool:
    """Supprime une matière (soft delete)"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE matieres SET statut = 'inactive' WHERE id_matiere = ?
        """, (matiere_id,))
        
        # Supprimer aussi les associations
        cursor.execute("""
            UPDATE classe_matieres SET statut = 'inactive' WHERE id_matiere = ?
        """, (matiere_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Matière {matiere_id} supprimée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur delete_matiere: {e}")
        return False

def assign_professeur_to_matiere(classe_matiere_id: int, professeur_id: int) -> bool:
    """Assigne un professeur à une matière dans une classe"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE classe_matieres SET id_professeur = ? WHERE id_classe_matiere = ?
        """, (professeur_id, classe_matiere_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Professeur {professeur_id} assigné à la matière {classe_matiere_id}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur assign_professeur_to_matiere: {e}")
        return False

def get_statistics() -> Dict:
    """Récupère les statistiques des matières"""
    try:
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        
        # Statistiques générales
        cursor.execute("SELECT COUNT(*) FROM matieres WHERE statut = 'active'")
        total_matieres = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM niveaux")
        total_niveaux = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM classe_matieres WHERE statut = 'active'")
        total_associations = cursor.fetchone()[0]
        
        # Statistiques par niveau
        cursor.execute("""
            SELECT n.nom_niveau, COUNT(DISTINCT m.id_matiere) as nb_matieres,
                   COUNT(DISTINCT c.id_classe) as nb_classes,
                   COUNT(cm.id_classe_matiere) as nb_associations
            FROM niveaux n
            LEFT JOIN classes c ON c.niveau = n.nom_niveau
            LEFT JOIN classe_matieres cm ON cm.id_classe = c.id_classe AND cm.statut = 'active'
            LEFT JOIN matieres m ON cm.id_matiere = m.id_matiere AND m.statut = 'active'
            GROUP BY n.id_niveau, n.nom_niveau
            ORDER BY n.nom_niveau
        """)
        
        stats_by_niveau = []
        for row in cursor.fetchall():
            stats_by_niveau.append({
                'niveau': row[0],
                'nb_matieres': row[1],
                'nb_classes': row[2],
                'nb_associations': row[3]
            })
        
        conn.close()
        
        stats = {
            'total_matieres': total_matieres,
            'total_niveaux': total_niveaux,
            'total_associations': total_associations,
            'stats_by_niveau': stats_by_niveau
        }
        
        print(f"✅ Statistiques récupérées: {total_matieres} matières, {total_niveaux} niveaux, {total_associations} associations")
        return stats
        
    except Exception as e:
        print(f"❌ Erreur get_statistics: {e}")
        return {}
