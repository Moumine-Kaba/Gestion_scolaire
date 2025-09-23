"""
Contrôleur pour les calculs automatiques des bulletins avec SQL Server
Système intelligent de calcul des moyennes et classements
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import os
import sys
from datetime import datetime

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Import de la connexion SQL Server
from database.connection import get_db_connection

@dataclass
class NoteMatiere:
    """Note d'une matière avec coefficient"""
    id_matiere: int
    nom_matiere: str
    coefficient: float
    notes: List[float]  # Liste des notes (devoirs, contrôles, etc.)
    moyenne: float
    appreciation: str

@dataclass
class CalculBulletin:
    """Résultat du calcul d'un bulletin"""
    moyenne_generale: float
    matieres: List[NoteMatiere]
    rang_classe: int
    rang_niveau: int
    total_points: float
    total_coefficients: float
    appreciation_generale: str

class CalculBulletinController:
    """Contrôleur pour les calculs automatiques des bulletins avec SQL Server"""
    
    def __init__(self):
        self.connection = get_db_connection()
    
    def calculer_moyenne_matiere(self, notes: List[float], coefficient: float = 1.0) -> float:
        """Calcule la moyenne d'une matière"""
        if not notes:
            return 0.0
        
        # Moyenne simple pour l'instant, peut être étendue avec des pondérations
        moyenne = sum(notes) / len(notes)
        return round(moyenne, 2)
    
    def calculer_moyenne_generale(self, matieres: List[NoteMatiere]) -> Tuple[float, float, float]:
        """Calcule la moyenne générale pondérée"""
        total_points = 0.0
        total_coefficients = 0.0
        
        for matiere in matieres:
            points = matiere.moyenne * matiere.coefficient
            total_points += points
            total_coefficients += matiere.coefficient
        
        if total_coefficients == 0:
            return 0.0, 0.0, 0.0
        
        moyenne_generale = total_points / total_coefficients
        return round(moyenne_generale, 2), total_points, total_coefficients
    
    def generer_appreciation_matiere(self, moyenne: float) -> str:
        """Génère une appréciation automatique pour une matière"""
        if moyenne >= 16:
            return "Excellent travail ! Continue ainsi."
        elif moyenne >= 14:
            return "Très bon travail. Quelques efforts supplémentaires pour exceller."
        elif moyenne >= 12:
            return "Bon travail. Continue tes efforts pour progresser."
        elif moyenne >= 10:
            return "Travail satisfaisant. Des efforts supplémentaires sont nécessaires."
        elif moyenne >= 8:
            return "Travail insuffisant. Des efforts importants sont nécessaires."
        else:
            return "Travail très insuffisant. Un travail régulier et soutenu est indispensable."
    
    def generer_appreciation_generale(self, moyenne: float, rang: int, total_eleves: int) -> str:
        """Génère une appréciation générale automatique"""
        pourcentage_rang = (rang / total_eleves) * 100 if total_eleves > 0 else 0
        
        if moyenne >= 16:
            if pourcentage_rang <= 10:
                return f"Excellent élève ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Continue sur cette lancée exceptionnelle."
            else:
                return f"Très bon élève ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Excellent travail."
        elif moyenne >= 14:
            if pourcentage_rang <= 25:
                return f"Bon élève ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Continue tes efforts pour exceller."
            else:
                return f"Élève sérieux ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Bon travail."
        elif moyenne >= 12:
            return f"Élève appliqué ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Continue tes efforts."
        elif moyenne >= 10:
            return f"Élève en progression ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Des efforts supplémentaires sont nécessaires."
        elif moyenne >= 8:
            return f"Élève en difficulté ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Un travail régulier et soutenu est indispensable."
        else:
            return f"Élève en grande difficulté ! Moyenne de {moyenne:.2f}/20. Classé {rang}ème sur {total_eleves}. Un suivi particulier est nécessaire."
    
    def calculer_bulletin_complet(self, id_eleve: int, id_classe: int, id_periode: int) -> CalculBulletin:
        """Calcule un bulletin complet pour un élève"""
        try:
            cursor = self.connection.cursor()
            
            # Récupérer les notes de l'élève pour la période
            cursor.execute("""
                SELECT n.id_matiere, m.nom, m.coefficient, n.note, n.type_evaluation
                FROM notes n
                JOIN matieres m ON n.id_matiere = m.id
                WHERE n.id_eleve = ? AND n.id_periode = ?
                ORDER BY n.id_matiere, n.date_note
            """, (id_eleve, id_periode))
            
            notes_data = cursor.fetchall()
            
            # Grouper les notes par matière
            matieres_dict = {}
            for row in notes_data:
                id_matiere, nom_matiere, coefficient, note, type_eval = row
                
                if id_matiere not in matieres_dict:
                    matieres_dict[id_matiere] = {
                        'nom': nom_matiere,
                        'coefficient': coefficient,
                        'notes': []
                    }
                
                matieres_dict[id_matiere]['notes'].append(note)
            
            # Calculer les moyennes par matière
            matieres = []
            for id_matiere, data in matieres_dict.items():
                moyenne = self.calculer_moyenne_matiere(data['notes'], data['coefficient'])
                appreciation = self.generer_appreciation_matiere(moyenne)
                
                matieres.append(NoteMatiere(
                    id_matiere=id_matiere,
                    nom_matiere=data['nom'],
                    coefficient=data['coefficient'],
                    notes=data['notes'],
                    moyenne=moyenne,
                    appreciation=appreciation
                ))
            
            # Calculer la moyenne générale
            moyenne_generale, total_points, total_coefficients = self.calculer_moyenne_generale(matieres)
            
            # Calculer le rang dans la classe
            rang_classe = self.calculer_rang_classe(id_eleve, id_classe, id_periode, moyenne_generale)
            
            # Calculer le rang dans le niveau
            rang_niveau = self.calculer_rang_niveau(id_eleve, id_classe, id_periode, moyenne_generale)
            
            # Générer l'appréciation générale
            total_eleves_classe = self.get_total_eleves_classe(id_classe)
            appreciation_generale = self.generer_appreciation_generale(
                moyenne_generale, rang_classe, total_eleves_classe
            )
            
            return CalculBulletin(
                moyenne_generale=moyenne_generale,
                matieres=matieres,
                rang_classe=rang_classe,
                rang_niveau=rang_niveau,
                total_points=total_points,
                total_coefficients=total_coefficients,
                appreciation_generale=appreciation_generale
            )
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul du bulletin: {e}")
            return CalculBulletin(
                moyenne_generale=0.0,
                matieres=[],
                rang_classe=0,
                rang_niveau=0,
                total_points=0.0,
                total_coefficients=0.0,
                appreciation_generale="Erreur lors du calcul"
            )
    
    def calculer_rang_classe(self, id_eleve: int, id_classe: int, id_periode: int, moyenne_eleve: float) -> int:
        """Calcule le rang de l'élève dans sa classe"""
        try:
            cursor = self.connection.cursor()
            
            # Récupérer toutes les moyennes de la classe pour la période
            cursor.execute("""
                SELECT DISTINCT e.id, 
                       COALESCE((
                           SELECT AVG(n.note) 
                           FROM notes n 
                           WHERE n.id_eleve = e.id AND n.id_periode = ?
                       ), 0) as moyenne
                FROM eleves e
                WHERE e.id_classe = ?
                ORDER BY moyenne DESC
            """, (id_periode, id_classe))
            
            moyennes = cursor.fetchall()
            
            # Trouver le rang de l'élève
            for i, (eleve_id, moyenne) in enumerate(moyennes):
                if eleve_id == id_eleve:
                    return i + 1
            
            return len(moyennes)  # Si pas trouvé, dernier rang
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul du rang classe: {e}")
            return 0
    
    def calculer_rang_niveau(self, id_eleve: int, id_classe: int, id_periode: int, moyenne_eleve: float) -> int:
        """Calcule le rang de l'élève dans son niveau"""
        try:
            cursor = self.connection.cursor()
            
            # Récupérer le niveau de la classe
            cursor.execute("SELECT niveau FROM classes WHERE id = ?", (id_classe,))
            niveau_result = cursor.fetchone()
            
            if not niveau_result:
                return 0
            
            niveau = niveau_result[0]
            
            # Récupérer toutes les moyennes du niveau pour la période
            cursor.execute("""
                SELECT DISTINCT e.id, 
                       COALESCE((
                           SELECT AVG(n.note) 
                           FROM notes n 
                           WHERE n.id_eleve = e.id AND n.id_periode = ?
                       ), 0) as moyenne
                FROM eleves e
                JOIN classes c ON e.id_classe = c.id
                WHERE c.niveau = ?
                ORDER BY moyenne DESC
            """, (id_periode, niveau))
            
            moyennes = cursor.fetchall()
            
            # Trouver le rang de l'élève
            for i, (eleve_id, moyenne) in enumerate(moyennes):
                if eleve_id == id_eleve:
                    return i + 1
            
            return len(moyennes)  # Si pas trouvé, dernier rang
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul du rang niveau: {e}")
            return 0
    
    def get_total_eleves_classe(self, id_classe: int) -> int:
        """Récupère le nombre total d'élèves dans une classe"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM eleves WHERE id_classe = ?", (id_classe,))
            total = cursor.fetchone()[0]
            
            return total
            
        except Exception as e:
            print(f"❌ Erreur lors du comptage des élèves: {e}")
            return 0
    
    def generer_bulletins_classe(self, id_classe: int, id_periode: int, cree_par: str) -> List[int]:
        """Génère automatiquement tous les bulletins d'une classe"""
        try:
            cursor = self.connection.cursor()
            
            # Récupérer tous les élèves de la classe
            cursor.execute("SELECT id FROM eleves WHERE id_classe = ?", (id_classe,))
            eleves = cursor.fetchall()
            
            bulletins_ids = []
            
            for (id_eleve,) in eleves:
                # Calculer le bulletin de l'élève
                calcul = self.calculer_bulletin_complet(id_eleve, id_classe, id_periode)
                
                # Créer le bulletin dans la base
                cursor.execute("""
                    INSERT INTO bulletins_avances 
                    (id_eleve, id_classe, id_periode, moyenne_generale, rang_classe, rang_niveau,
                     total_eleves_classe, total_eleves_niveau, appreciation_generale, appreciation_conduct,
                     status, cree_par)
                    OUTPUT INSERTED.id
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_eleve, id_classe, id_periode, calcul.moyenne_generale,
                    calcul.rang_classe, calcul.rang_niveau,
                    self.get_total_eleves_classe(id_classe), 0,  # total_eleves_niveau à calculer
                    calcul.appreciation_generale, "",
                    "brouillon", cree_par
                ))
                
                bulletin_id = cursor.fetchone()[0]
                
                # Insérer les matières
                for matiere in calcul.matieres:
                    cursor.execute("""
                        INSERT INTO bulletin_matieres 
                        (id_bulletin, id_matiere, moyenne, coefficient, appreciation)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        bulletin_id, matiere.id_matiere, matiere.moyenne,
                        matiere.coefficient, matiere.appreciation
                    ))
                
                bulletins_ids.append(bulletin_id)
            
            self.connection.commit()
            return bulletins_ids
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des bulletins: {e}")
            self.connection.rollback()
            return []
    
    def recalculer_classements(self, id_classe: int, id_periode: int):
        """Recalcule tous les classements d'une classe"""
        try:
            cursor = self.connection.cursor()
            
            # Récupérer tous les bulletins de la classe
            cursor.execute("""
                SELECT id, moyenne_generale FROM bulletins_avances 
                WHERE id_classe = ? AND id_periode = ?
                ORDER BY moyenne_generale DESC
            """, (id_classe, id_periode))
            
            bulletins = cursor.fetchall()
            
            # Mettre à jour les rangs
            for i, (bulletin_id, moyenne) in enumerate(bulletins):
                rang = i + 1
                cursor.execute("""
                    UPDATE bulletins_avances 
                    SET rang_classe = ?, total_eleves_classe = ?, date_modification = GETDATE()
                    WHERE id = ?
                """, (rang, len(bulletins), bulletin_id))
            
            self.connection.commit()
            
        except Exception as e:
            print(f"❌ Erreur lors du recalcul des classements: {e}")
            self.connection.rollback()


