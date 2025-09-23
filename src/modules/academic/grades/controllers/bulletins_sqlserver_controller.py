"""
Contrôleur principal pour la gestion des bulletins avec SQL Server
Interface entre les modèles, vues et la logique métier
"""

from typing import List, Dict, Optional, Tuple
from datetime import datetime, date
import os
import sys

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Import de la connexion SQL Server
from database.connection import get_db_connection

# Import des modèles et contrôleurs
from .models.bulletin_sqlserver_model import (
    BulletinAdvancedModel, BulletinAvance, PeriodeScolaire, 
    PeriodeType, BulletinStatus, MatiereBulletin
)
from .controllers.calcul_bulletin_sqlserver_controller import (
    CalculBulletinController, CalculBulletin, NoteMatiere
)

class BulletinsController:
    """Contrôleur principal pour la gestion des bulletins avec SQL Server"""
    
    def __init__(self):
        self.connection = get_db_connection()
        self.bulletin_model = BulletinAdvancedModel()
        self.calcul_controller = CalculBulletinController()
    
    # ===== GESTION DES PÉRIODES =====
    
    def creer_periode_scolaire(self, nom: str, type_periode: str, 
                              date_debut: date, date_fin: date, 
                              annee_scolaire: str) -> int:
        """Crée une nouvelle période scolaire"""
        periode = PeriodeScolaire(
            id=0,  # Sera assigné par la base
            nom=nom,
            type_periode=PeriodeType(type_periode),
            date_debut=date_debut,
            date_fin=date_fin,
            annee_scolaire=annee_scolaire
        )
        
        return self.bulletin_model.create_periode(periode)
    
    def get_periodes_actives(self) -> List[PeriodeScolaire]:
        """Récupère toutes les périodes actives"""
        return self.bulletin_model.get_periodes_actives()
    
    def get_periode_by_id(self, periode_id: int) -> Optional[PeriodeScolaire]:
        """Récupère une période par son ID"""
        periodes = self.get_periodes_actives()
        for periode in periodes:
            if periode.id == periode_id:
                return periode
        return None
    
    # ===== GESTION DES BULLETINS =====
    
    def generer_bulletins_classe(self, id_classe: int, id_periode: int, 
                                cree_par: str) -> List[int]:
        """Génère automatiquement tous les bulletins d'une classe"""
        return self.calcul_controller.generer_bulletins_classe(
            id_classe, id_periode, cree_par
        )
    
    def get_bulletins_classe(self, id_classe: int, id_periode: int = None) -> List[BulletinAvance]:
        """Récupère les bulletins d'une classe"""
        return self.bulletin_model.get_bulletins_by_classe(id_classe, id_periode)
    
    def get_bulletin_eleve(self, id_eleve: int, id_periode: int) -> Optional[BulletinAvance]:
        """Récupère le bulletin d'un élève pour une période"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT b.id, b.id_eleve, e.nom, e.prenom, b.id_classe, c.nom,
                       b.id_periode, p.nom, p.type_periode, p.annee_scolaire,
                       b.moyenne_generale, b.rang_classe, b.rang_niveau,
                       b.total_eleves_classe, b.total_eleves_niveau,
                       b.appreciation_generale, b.appreciation_conduct,
                       b.status, b.date_creation, b.date_modification,
                       b.cree_par, b.valide_par, b.date_validation
                FROM bulletins_avances b
                JOIN eleves e ON b.id_eleve = e.id
                JOIN classes c ON b.id_classe = c.id
                JOIN periodes_scolaires p ON b.id_periode = p.id
                WHERE b.id_eleve = ? AND b.id_periode = ?
            """, (id_eleve, id_periode))
            
            row = cursor.fetchone()
            if not row:
                return None
            
            # Récupérer les matières
            cursor.execute("""
                SELECT bm.id_matiere, m.nom, bm.moyenne, bm.coefficient, 
                       bm.appreciation, bm.rang_matiere
                FROM bulletin_matieres bm
                JOIN matieres m ON bm.id_matiere = m.id
                WHERE bm.id_bulletin = ?
                ORDER BY bm.rang_matiere
            """, (row[0],))
            
            matieres = []
            for mat_row in cursor.fetchall():
                matieres.append(MatiereBulletin(
                    id_matiere=mat_row[0],
                    nom_matiere=mat_row[1],
                    moyenne=mat_row[2],
                    coefficient=mat_row[3],
                    appreciation=mat_row[4] or "",
                    rang_matiere=mat_row[5] or 0
                ))
            
            return BulletinAvance(
                id=row[0],
                id_eleve=row[1],
                eleve_nom=row[2],
                eleve_prenom=row[3],
                id_classe=row[4],
                classe_nom=row[5],
                id_periode=row[6],
                periode_nom=row[7],
                periode_type=row[8],
                annee_scolaire=row[9],
                matieres=matieres,
                moyenne_generale=row[10],
                rang_classe=row[11] or 0,
                rang_niveau=row[12] or 0,
                total_eleves_classe=row[13] or 0,
                total_eleves_niveau=row[14] or 0,
                appreciation_generale=row[15] or "",
                appreciation_conduct=row[16] or "",
                status=BulletinStatus(row[17]),
                date_creation=row[18],
                date_modification=row[19],
                cree_par=row[20],
                valide_par=row[21],
                date_validation=row[22]
            )
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du bulletin: {e}")
            return None
    
    def recalculer_bulletin(self, id_eleve: int, id_classe: int, id_periode: int) -> BulletinAvance:
        """Recalcule un bulletin pour un élève"""
        try:
            # Calculer le nouveau bulletin
            calcul = self.calcul_controller.calculer_bulletin_complet(
                id_eleve, id_classe, id_periode
            )
            
            # Mettre à jour en base
            cursor = self.connection.cursor()
            
            # Supprimer l'ancien bulletin
            cursor.execute("DELETE FROM bulletins_avances WHERE id_eleve = ? AND id_periode = ?", 
                          (id_eleve, id_periode))
            
            # Créer le nouveau bulletin
            cursor.execute("""
                INSERT INTO bulletins_avances 
                (id_eleve, id_classe, id_periode, moyenne_generale, rang_classe, rang_niveau,
                 total_eleves_classe, total_eleves_niveau, appreciation_generale, appreciation_conduct,
                 status, cree_par, date_modification)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_eleve, id_classe, id_periode, calcul.moyenne_generale,
                calcul.rang_classe, calcul.rang_niveau,
                self.calcul_controller.get_total_eleves_classe(id_classe), 0,
                calcul.appreciation_generale, "",
                "brouillon", "SYSTEM", datetime.now()
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
            
            self.connection.commit()
            
            # Recalculer les classements
            self.calcul_controller.recalculer_classements(id_classe, id_periode)
            
            return self.get_bulletin_eleve(id_eleve, id_periode)
            
        except Exception as e:
            print(f"❌ Erreur lors du recalcul du bulletin: {e}")
            self.connection.rollback()
            return None
    
    # ===== STATISTIQUES ET RAPPORTS =====
    
    def get_statistiques_classe(self, id_classe: int, id_periode: int = None) -> Dict:
        """Calcule les statistiques d'une classe"""
        return self.bulletin_model.get_statistiques_classe(id_classe, id_periode)
    
    def get_statistiques_globales(self, id_periode: int = None) -> Dict:
        """Calcule les statistiques globales de l'établissement"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT COUNT(*), AVG(moyenne_generale), MIN(moyenne_generale), MAX(moyenne_generale)
                FROM bulletins_avances
            """
            
            params = []
            if id_periode:
                query += " WHERE id_periode = ?"
                params.append(id_periode)
            
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            total_bulletins = row[0] or 0
            moyenne_generale = row[1] or 0
            moins_bonne_moyenne = row[2] or 0
            meilleure_moyenne = row[3] or 0
            
            # Calculer le taux de réussite
            query_reussite = """
                SELECT COUNT(*) FROM bulletins_avances WHERE moyenne_generale >= 10
            """
            if id_periode:
                query_reussite += " AND id_periode = ?"
            
            cursor.execute(query_reussite, params)
            bulletins_reussite = cursor.fetchone()[0] or 0
            
            taux_reussite = (bulletins_reussite / total_bulletins * 100) if total_bulletins > 0 else 0
            
            return {
                'total_bulletins': total_bulletins,
                'moyenne_generale': round(moyenne_generale, 2),
                'meilleure_moyenne': round(meilleure_moyenne, 2),
                'moins_bonne_moyenne': round(moins_bonne_moyenne, 2),
                'taux_reussite': round(taux_reussite, 2),
                'bulletins_reussite': bulletins_reussite
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques globales: {e}")
            return {
                'total_bulletins': 0,
                'moyenne_generale': 0,
                'meilleure_moyenne': 0,
                'moins_bonne_moyenne': 0,
                'taux_reussite': 0,
                'bulletins_reussite': 0
            }
    
    def get_top_eleves(self, limite: int = 10, id_periode: int = None) -> List[Dict]:
        """Récupère le top des élèves"""
        try:
            cursor = self.connection.cursor()
            
            query = """
                SELECT e.nom, e.prenom, c.nom, b.moyenne_generale, b.rang_classe
                FROM bulletins_avances b
                JOIN eleves e ON b.id_eleve = e.id
                JOIN classes c ON b.id_classe = c.id
            """
            
            params = []
            if id_periode:
                query += " WHERE b.id_periode = ?"
                params.append(id_periode)
            
            query += " ORDER BY b.moyenne_generale DESC"
            
            # SQL Server utilise TOP au lieu de LIMIT
            query = query.replace("ORDER BY b.moyenne_generale DESC", f"ORDER BY b.moyenne_generale DESC")
            query = f"SELECT TOP {limite} * FROM ({query}) AS top_query"
            
            cursor.execute(query, params)
            
            top_eleves = []
            for row in cursor.fetchall():
                top_eleves.append({
                    'nom': row[0],
                    'prenom': row[1],
                    'classe': row[2],
                    'moyenne': row[3],
                    'rang': row[4]
                })
            
            return top_eleves
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du top élèves: {e}")
            return []
    
    def get_evolution_eleve(self, id_eleve: int, annee_scolaire: str) -> List[Dict]:
        """Récupère l'évolution d'un élève sur l'année"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT p.nom, p.type_periode, b.moyenne_generale, b.rang_classe, b.total_eleves_classe
                FROM bulletins_avances b
                JOIN periodes_scolaires p ON b.id_periode = p.id
                WHERE b.id_eleve = ? AND p.annee_scolaire = ?
                ORDER BY p.date_debut
            """, (id_eleve, annee_scolaire))
            
            evolution = []
            for row in cursor.fetchall():
                evolution.append({
                    'periode': row[0],
                    'type_periode': row[1],
                    'moyenne': row[2],
                    'rang': row[3],
                    'total_eleves': row[4]
                })
            
            return evolution
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de l'évolution: {e}")
            return []
    
    # ===== VALIDATION ET WORKFLOW =====
    
    def valider_bulletin(self, bulletin_id: int, valide_par: str) -> bool:
        """Valide un bulletin"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                UPDATE bulletins_avances 
                SET status = 'valide', valide_par = ?, date_validation = GETDATE(), date_modification = GETDATE()
                WHERE id = ?
            """, (valide_par, bulletin_id))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la validation: {e}")
            self.connection.rollback()
            return False
    
    def approuver_bulletin(self, bulletin_id: int, approuve_par: str) -> bool:
        """Approuve un bulletin"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                UPDATE bulletins_avances 
                SET status = 'approuve', valide_par = ?, date_validation = GETDATE(), date_modification = GETDATE()
                WHERE id = ?
            """, (approuve_par, bulletin_id))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'approbation: {e}")
            self.connection.rollback()
            return False
    
    def archiver_bulletin(self, bulletin_id: int) -> bool:
        """Archive un bulletin"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                UPDATE bulletins_avances 
                SET status = 'archive', date_modification = GETDATE()
                WHERE id = ?
            """, (bulletin_id,))
            
            self.connection.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'archivage: {e}")
            self.connection.rollback()
            return False
    
    # ===== EXPORT ET RAPPORTS =====
    
    def exporter_bulletins_classe(self, id_classe: int, id_periode: int, format: str = "pdf") -> str:
        """Exporte les bulletins d'une classe"""
        # Cette fonction sera implémentée avec le système d'export
        bulletins = self.get_bulletins_classe(id_classe, id_periode)
        
        if format == "pdf":
            return self._generer_pdf_bulletins(bulletins)
        elif format == "excel":
            return self._generer_excel_bulletins(bulletins)
        else:
            raise ValueError("Format non supporté")
    
    def _generer_pdf_bulletins(self, bulletins: List[BulletinAvance]) -> str:
        """Génère un PDF des bulletins"""
        # Implémentation à venir avec reportlab
        return "bulletin_classe.pdf"
    
    def _generer_excel_bulletins(self, bulletins: List[BulletinAvance]) -> str:
        """Génère un Excel des bulletins"""
        # Implémentation à venir avec openpyxl
        return "bulletin_classe.xlsx"


