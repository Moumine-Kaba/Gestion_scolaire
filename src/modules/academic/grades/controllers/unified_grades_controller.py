"""
Contrôleur unifié pour la gestion des liaisons entre matières, notes et bulletins
Gère les relations entre les tables pour une cohérence optimale des données
"""

from database.connection import get_db_connection
import os
import sys
from typing import List, Dict, Any, Optional

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def connect_db():
    """Crée et retourne une connexion à la base de données SQL Server."""
    conn = get_db_connection()
    return conn

def get_student_complete_grades(student_id: int) -> List[Dict[str, Any]]:
    """
    Récupère toutes les notes d'un élève avec les informations complètes des matières
    Liaison: notes -> matieres -> bulletins
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        
        # Requête avec jointures complètes (corrigée pour SQL Server)
        cursor.execute("""
            SELECT 
                n.id_note,
                n.id_eleve,
                n.id_matiere,
                n.note,
                n.coefficient as note_coefficient,
                n.type_evaluation,
                n.date_evaluation,
                n.commentaire as note_commentaire,
                
                m.nom_matiere,
                m.coefficient as matiere_coefficient,
                m.description as matiere_description,
                m.statut as matiere_statut,
                
                e.nom as eleve_nom,
                e.prenom as eleve_prenom,
                e.id_classe,
                
                b.id_bulletin,
                b.periode,
                b.moyenne_generale,
                b.rang,
                b.appreciation as bulletin_appreciation,
                b.date_creation as bulletin_date_creation
                
            FROM notes n
            LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
            LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
            LEFT JOIN bulletins b ON n.id_eleve = b.id_eleve AND b.periode = 'Année scolaire 2025-2026'
            WHERE n.id_eleve = ?
            ORDER BY m.nom_matiere, n.date_evaluation DESC
        """, (student_id,))
        
        rows = cursor.fetchall()
        
        # Mapping des matières pour avoir des noms corrects
        matiere_names = {
            1: "Mathématiques",
            2: "Français", 
            3: "Histoire-Géographie",
            4: "Sciences Physiques",
            5: "Sciences de la Vie",
            6: "Anglais",
            7: "Éducation Physique",
            8: "Arts Plastiques",
            9: "Informatique",
            10: "Philosophie"
        }
        
        # Organiser les données par matière
        subjects_data = {}
        
        for row in rows:
            matiere_id = row[2]  # id_matiere
            
            if matiere_id not in subjects_data:
                # Sécuriser le coefficient (corriger l'index - le coefficient est à row[9])
                coeff_value = row[9]  # matiere_coefficient (corrigé)
                try:
                    coefficient = float(coeff_value) if coeff_value else 1.0
                except (ValueError, TypeError):
                    coefficient = 1.0
                
                # Utiliser le mapping pour le nom de la matière (corriger l'index)
                nom_matiere = matiere_names.get(matiere_id, row[8] if row[8] else f"Matière {matiere_id}")
                
                subjects_data[matiere_id] = {
                    'id_matiere': matiere_id,
                    'nom_matiere': nom_matiere,
                    'coefficient': coefficient,
                    'description': row[10] if row[10] else '',  # matiere_description (corrigé)
                    'statut': row[12] if row[12] else 'Active',  # matiere_statut
                    'notes': [],
                    'moyenne_matiere': 0,
                    'total_points': 0,
                    'total_coefficients': 0
                }
            
            # Ajouter la note
            note_data = {
                'id_note': row[0],
                'note': row[3],
                'coefficient': row[4],  # note_coefficient
                'type_evaluation': row[5],
                'date_evaluation': row[6],
                'commentaire': row[7]
            }
            
            subjects_data[matiere_id]['notes'].append(note_data)
            
            # Calculer la moyenne pondérée pour cette matière
            if note_data['note'] > 0:
                points = note_data['note'] * note_data['coefficient']
                subjects_data[matiere_id]['total_points'] += points
                subjects_data[matiere_id]['total_coefficients'] += note_data['coefficient']
        
        # Calculer les moyennes par matière
        result = []
        for matiere_id, data in subjects_data.items():
            if data['total_coefficients'] > 0:
                data['moyenne_matiere'] = data['total_points'] / data['total_coefficients']
            else:
                data['moyenne_matiere'] = 0
            
            # Utiliser le coefficient de la matière pour la moyenne générale
            data['coefficient'] = data['coefficient']  # Garder le coefficient de la matière
            
            result.append(data)
        
        conn.close()
        print(f"✅ {len(result)} matières récupérées pour l'élève {student_id}")
        return result
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des notes complètes: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_class_complete_bulletins(classe_id: int) -> List[Dict[str, Any]]:
    """
    Récupère tous les bulletins d'une classe avec les informations complètes
    Liaison: bulletins -> eleves -> notes -> matieres
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return []
        
        cursor = conn.cursor()
        
        # Requête avec jointures complètes
        cursor.execute("""
            SELECT 
                b.id_bulletin,
                b.id_eleve,
                b.periode,
                b.moyenne_generale,
                b.rang,
                b.appreciation,
                b.date_creation as bulletin_date_creation,
                
                e.nom as eleve_nom,
                e.prenom as eleve_prenom,
                e.id_classe,
                e.genre,
                e.date_naissance,
                e.statut as eleve_statut,
                
                COUNT(n.id_note) as nombre_notes,
                AVG(n.note) as moyenne_calculée,
                COUNT(DISTINCT n.id_matiere) as nombre_matieres
                
            FROM bulletins b
            LEFT JOIN eleves e ON b.id_eleve = e.id_eleve
            LEFT JOIN notes n ON b.id_eleve = n.id_eleve
            WHERE e.id_classe = ?
            GROUP BY b.id_bulletin, b.id_eleve, b.periode, b.moyenne_generale, 
                     b.rang, b.appreciation, b.date_creation,
                     e.nom, e.prenom, e.id_classe, e.genre, e.date_naissance, e.statut
            ORDER BY b.moyenne_generale DESC, b.rang ASC
        """, (classe_id,))
        
        rows = cursor.fetchall()
        
        bulletins_data = []
        for row in rows:
            bulletin_dict = {
                'id': row[0],  # id_bulletin
                'id_eleve': row[1],  # id_eleve
                'periode': row[2],  # periode
                'moyenne_generale': float(row[3]) if row[3] else 0.0,  # moyenne_generale
                'rang': row[4],  # rang
                'appreciation': row[5],  # appreciation
                'date_creation': row[6],  # bulletin_date_creation
                'eleve_nom': row[7],  # eleve_nom
                'eleve_prenom': row[8],  # eleve_prenom
                'id_classe': row[9],  # id_classe
                'eleve_genre': row[10],  # genre
                'eleve_date_naissance': row[11],  # date_naissance
                'eleve_statut': row[12],  # eleve_statut
                'nombre_notes': row[13],  # nombre_notes
                'moyenne_calculée': float(row[14]) if row[14] else 0.0,  # moyenne_calculée
                'nombre_matieres': row[15]  # nombre_matieres
            }
            bulletins_data.append(bulletin_dict)
        
        conn.close()
        print(f"✅ {len(bulletins_data)} bulletins récupérés pour la classe {classe_id}")
        return bulletins_data
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des bulletins de classe: {e}")
        import traceback
        traceback.print_exc()
        return []

def get_subject_statistics(matiere_id: int, classe_id: Optional[int] = None) -> Dict[str, Any]:
    """
    Récupère les statistiques d'une matière avec liaisons complètes
    Liaison: matieres -> notes -> eleves -> bulletins
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        
        # Construire la requête selon les paramètres
        if classe_id:
            cursor.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom_matiere,
                    m.coefficient,
                    m.description,
                    m.statut,
                    
                    COUNT(n.id_note) as nombre_notes,
                    AVG(n.note) as moyenne_generale,
                    MIN(n.note) as note_min,
                    MAX(n.note) as note_max,
                    COUNT(DISTINCT n.id_eleve) as nombre_eleves,
                    
                    COUNT(DISTINCT b.id_bulletin) as nombre_bulletins,
                    AVG(b.moyenne_generale) as moyenne_bulletins
                    
                FROM matieres m
                LEFT JOIN notes n ON m.id_matiere = n.id_matiere
                LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
                LEFT JOIN bulletins b ON e.id_eleve = b.id_eleve
                WHERE m.id_matiere = ? AND e.id_classe = ?
                GROUP BY m.id_matiere, m.nom_matiere, m.coefficient, m.description, m.statut
            """, (matiere_id, classe_id))
        else:
            cursor.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom_matiere,
                    m.coefficient,
                    m.description,
                    m.statut,
                    
                    COUNT(n.id_note) as nombre_notes,
                    AVG(n.note) as moyenne_generale,
                    MIN(n.note) as note_min,
                    MAX(n.note) as note_max,
                    COUNT(DISTINCT n.id_eleve) as nombre_eleves,
                    
                    COUNT(DISTINCT b.id_bulletin) as nombre_bulletins,
                    AVG(b.moyenne_generale) as moyenne_bulletins
                    
                FROM matieres m
                LEFT JOIN notes n ON m.id_matiere = n.id_matiere
                LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
                LEFT JOIN bulletins b ON e.id_eleve = b.id_eleve
                WHERE m.id_matiere = ?
                GROUP BY m.id_matiere, m.nom_matiere, m.coefficient, m.description, m.statut
            """, (matiere_id,))
        
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return {}
        
        statistics = {
            'id_matiere': row[0],
            'nom_matiere': row[1],
            'coefficient': row[2],
            'description': row[3],
            'statut': row[4],
            'nombre_notes': row[5],
            'moyenne_generale': float(row[6]) if row[6] else 0.0,
            'note_min': float(row[7]) if row[7] else 0.0,
            'note_max': float(row[8]) if row[8] else 0.0,
            'nombre_eleves': row[9],
            'nombre_bulletins': row[10],
            'moyenne_bulletins': float(row[11]) if row[11] else 0.0
        }
        
        conn.close()
        print(f"✅ Statistiques récupérées pour la matière {statistics['nom_matiere']}")
        return statistics
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des statistiques matière: {e}")
        import traceback
        traceback.print_exc()
        return {}

def validate_data_consistency() -> Dict[str, Any]:
    """
    Valide la cohérence des données entre les tables
    Vérifie les liaisons et détecte les incohérences
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        
        # Vérifications de cohérence
        checks = {}
        
        # 1. Notes orphelines (sans matière)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM notes n 
            LEFT JOIN matieres m ON n.id_matiere = m.id_matiere 
            WHERE m.id_matiere IS NULL
        """)
        checks['notes_orphelines'] = cursor.fetchone()[0]
        
        # 2. Notes orphelines (sans élève)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM notes n 
            LEFT JOIN eleves e ON n.id_eleve = e.id_eleve 
            WHERE e.id_eleve IS NULL
        """)
        checks['notes_sans_eleve'] = cursor.fetchone()[0]
        
        # 3. Bulletins orphelins (sans élève)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM bulletins b 
            LEFT JOIN eleves e ON b.id_eleve = e.id_eleve 
            WHERE e.id_eleve IS NULL
        """)
        checks['bulletins_orphelins'] = cursor.fetchone()[0]
        
        # 4. Élèves sans notes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM eleves e 
            LEFT JOIN notes n ON e.id_eleve = n.id_eleve 
            WHERE n.id_eleve IS NULL
        """)
        checks['eleves_sans_notes'] = cursor.fetchone()[0]
        
        # 5. Élèves sans bulletins
        cursor.execute("""
            SELECT COUNT(*) 
            FROM eleves e 
            LEFT JOIN bulletins b ON e.id_eleve = b.id_eleve 
            WHERE b.id_eleve IS NULL
        """)
        checks['eleves_sans_bulletins'] = cursor.fetchone()[0]
        
        # 6. Matières sans notes
        cursor.execute("""
            SELECT COUNT(*) 
            FROM matieres m 
            LEFT JOIN notes n ON m.id_matiere = n.id_matiere 
            WHERE n.id_matiere IS NULL
        """)
        checks['matieres_sans_notes'] = cursor.fetchone()[0]
        
        conn.close()
        
        # Calculer le score de cohérence
        total_issues = sum(checks.values())
        checks['score_coherence'] = max(0, 100 - (total_issues * 10))
        checks['total_problemes'] = total_issues
        
        print(f"✅ Validation de cohérence terminée - Score: {checks['score_coherence']}%")
        return checks
        
    except Exception as e:
        print(f"❌ Erreur lors de la validation de cohérence: {e}")
        import traceback
        traceback.print_exc()
        return {}

def repair_data_consistency() -> Dict[str, int]:
    """
    Répare les incohérences détectées dans les données
    """
    try:
        conn = connect_db()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return {}
        
        cursor = conn.cursor()
        repairs = {}
        
        # 1. Supprimer les notes orphelines (sans matière)
        cursor.execute("""
            DELETE FROM notes 
            WHERE id_matiere NOT IN (SELECT id_matiere FROM matieres)
        """)
        repairs['notes_orphelines_supprimees'] = cursor.rowcount
        
        # 2. Supprimer les notes orphelines (sans élève)
        cursor.execute("""
            DELETE FROM notes 
            WHERE id_eleve NOT IN (SELECT id_eleve FROM eleves)
        """)
        repairs['notes_sans_eleve_supprimees'] = cursor.rowcount
        
        # 3. Supprimer les bulletins orphelins (sans élève)
        cursor.execute("""
            DELETE FROM bulletins 
            WHERE id_eleve NOT IN (SELECT id_eleve FROM eleves)
        """)
        repairs['bulletins_orphelins_supprimes'] = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        total_repairs = sum(repairs.values())
        print(f"✅ Réparation terminée - {total_repairs} éléments nettoyés")
        return repairs
        
    except Exception as e:
        print(f"❌ Erreur lors de la réparation: {e}")
        import traceback
        traceback.print_exc()
        return {}
