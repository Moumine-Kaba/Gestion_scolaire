"""
Modèle avancé pour la gestion des bulletins scolaires avec SQL Server
Système professionnel avec périodes, calculs automatiques et classements
"""

import pyodbc
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import os
import sys

# Ajouter le chemin racine pour les imports
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
sys.path.insert(0, root_path)

# Import de la connexion SQL Server
from database.connection import get_db_connection

class PeriodeType(Enum):
    """Types de périodes scolaires"""
    TRIMESTRE = "trimestre"
    SEMESTRE = "semestre"
    ANNEE = "annee"
    CUSTOM = "custom"

class BulletinStatus(Enum):
    """Statuts des bulletins"""
    BROUILLON = "brouillon"
    VALIDE = "valide"
    APPROUVE = "approuve"
    ARCHIVE = "archive"

@dataclass
class PeriodeScolaire:
    """Période scolaire avec dates et type"""
    id: int
    nom: str
    type_periode: PeriodeType
    date_debut: date
    date_fin: date
    annee_scolaire: str
    actif: bool = True

@dataclass
class MatiereBulletin:
    """Matière avec coefficient et notes"""
    id_matiere: int
    nom_matiere: str
    coefficient: float
    moyenne: float
    appreciation: str
    rang_matiere: int

@dataclass
class BulletinAvance:
    """Bulletin scolaire complet avec toutes les données"""
    id: int
    id_eleve: int
    eleve_nom: str
    eleve_prenom: str
    id_classe: int
    classe_nom: str
    id_periode: int
    periode_nom: str
    periode_type: str
    annee_scolaire: str
    
    # Données académiques
    matieres: List[MatiereBulletin]
    moyenne_generale: float
    rang_classe: int
    rang_niveau: int
    total_eleves_classe: int
    total_eleves_niveau: int
    
    # Appréciations
    appreciation_generale: str
    appreciation_conduct: str
    
    # Métadonnées
    status: BulletinStatus
    date_creation: datetime
    date_modification: datetime
    cree_par: str
    valide_par: Optional[str]
    date_validation: Optional[datetime]

class BulletinAdvancedModel:
    """Modèle avancé pour la gestion des bulletins avec SQL Server"""
    
    def __init__(self):
        self.connection = get_db_connection()
        self.init_tables()
    
    def init_tables(self):
        """Initialise les tables nécessaires dans SQL Server"""
        try:
            cursor = self.connection.cursor()
            
            # Table des périodes scolaires
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='periodes_scolaires' AND xtype='U')
                CREATE TABLE periodes_scolaires (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    nom NVARCHAR(100) NOT NULL,
                    type_periode NVARCHAR(20) NOT NULL,
                    date_debut DATE NOT NULL,
                    date_fin DATE NOT NULL,
                    annee_scolaire NVARCHAR(20) NOT NULL,
                    actif BIT DEFAULT 1,
                    created_at DATETIME2 DEFAULT GETDATE()
                )
            """)
            
            # Table des bulletins avancés
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='bulletins_avances' AND xtype='U')
                CREATE TABLE bulletins_avances (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    id_eleve INT NOT NULL,
                    id_classe INT NOT NULL,
                    id_periode INT NOT NULL,
                    moyenne_generale DECIMAL(5,2) NOT NULL,
                    rang_classe INT,
                    rang_niveau INT,
                    total_eleves_classe INT,
                    total_eleves_niveau INT,
                    appreciation_generale NVARCHAR(MAX),
                    appreciation_conduct NVARCHAR(MAX),
                    status NVARCHAR(20) DEFAULT 'brouillon',
                    date_creation DATETIME2 DEFAULT GETDATE(),
                    date_modification DATETIME2 DEFAULT GETDATE(),
                    cree_par NVARCHAR(100) NOT NULL,
                    valide_par NVARCHAR(100),
                    date_validation DATETIME2,
                    FOREIGN KEY (id_eleve) REFERENCES eleves (id),
                    FOREIGN KEY (id_classe) REFERENCES classes (id),
                    FOREIGN KEY (id_periode) REFERENCES periodes_scolaires (id)
                )
            """)
            
            # Table des matières par bulletin
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='bulletin_matieres' AND xtype='U')
                CREATE TABLE bulletin_matieres (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    id_bulletin INT NOT NULL,
                    id_matiere INT NOT NULL,
                    moyenne DECIMAL(5,2) NOT NULL,
                    coefficient DECIMAL(3,2) DEFAULT 1.0,
                    appreciation NVARCHAR(MAX),
                    rang_matiere INT,
                    FOREIGN KEY (id_bulletin) REFERENCES bulletins_avances (id),
                    FOREIGN KEY (id_matiere) REFERENCES matieres (id)
                )
            """)
            
            # Index pour améliorer les performances
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_bulletins_eleve')
                CREATE INDEX idx_bulletins_eleve ON bulletins_avances (id_eleve)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_bulletins_classe')
                CREATE INDEX idx_bulletins_classe ON bulletins_avances (id_classe)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_bulletins_periode')
                CREATE INDEX idx_bulletins_periode ON bulletins_avances (id_periode)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_bulletins_status')
                CREATE INDEX idx_bulletins_status ON bulletins_avances (status)
            """)
            
            self.connection.commit()
            print("✅ Tables des bulletins avancés créées avec succès")
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des tables: {e}")
            self.connection.rollback()
    
    def create_periode(self, periode: PeriodeScolaire) -> int:
        """Crée une nouvelle période scolaire"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                INSERT INTO periodes_scolaires 
                (nom, type_periode, date_debut, date_fin, annee_scolaire, actif)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                periode.nom, 
                periode.type_periode.value, 
                periode.date_debut, 
                periode.date_fin, 
                periode.annee_scolaire,
                periode.actif
            ))
            
            periode_id = cursor.fetchone()[0]
            self.connection.commit()
            
            return periode_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la période: {e}")
            self.connection.rollback()
            return None
    
    def get_periodes_actives(self) -> List[PeriodeScolaire]:
        """Récupère toutes les périodes actives"""
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("""
                SELECT id, nom, type_periode, date_debut, date_fin, annee_scolaire, actif
                FROM periodes_scolaires 
                WHERE actif = 1
                ORDER BY date_debut
            """)
            
            periodes = []
            for row in cursor.fetchall():
                periodes.append(PeriodeScolaire(
                    id=row[0],
                    nom=row[1],
                    type_periode=PeriodeType(row[2]),
                    date_debut=row[3],
                    date_fin=row[4],
                    annee_scolaire=row[5],
                    actif=bool(row[6])
                ))
            
            return periodes
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des périodes: {e}")
            return []
    
    def create_bulletin(self, bulletin: BulletinAvance) -> int:
        """Crée un nouveau bulletin"""
        try:
            cursor = self.connection.cursor()
            
            # Insérer le bulletin principal
            cursor.execute("""
                INSERT INTO bulletins_avances 
                (id_eleve, id_classe, id_periode, moyenne_generale, rang_classe, rang_niveau,
                 total_eleves_classe, total_eleves_niveau, appreciation_generale, appreciation_conduct,
                 status, cree_par)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                bulletin.id_eleve, bulletin.id_classe, bulletin.id_periode,
                bulletin.moyenne_generale, bulletin.rang_classe, bulletin.rang_niveau,
                bulletin.total_eleves_classe, bulletin.total_eleves_niveau,
                bulletin.appreciation_generale, bulletin.appreciation_conduct,
                bulletin.status.value, bulletin.cree_par
            ))
            
            bulletin_id = cursor.fetchone()[0]
            
            # Insérer les matières
            for matiere in bulletin.matieres:
                cursor.execute("""
                    INSERT INTO bulletin_matieres 
                    (id_bulletin, id_matiere, moyenne, coefficient, appreciation, rang_matiere)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    bulletin_id, matiere.id_matiere, matiere.moyenne,
                    matiere.coefficient, matiere.appreciation, matiere.rang_matiere
                ))
            
            self.connection.commit()
            return bulletin_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la création du bulletin: {e}")
            self.connection.rollback()
            return None
    
    def get_bulletins_by_classe(self, id_classe: int, id_periode: int = None) -> List[BulletinAvance]:
        """Récupère les bulletins d'une classe"""
        try:
            cursor = self.connection.cursor()
            
            query = """
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
                WHERE b.id_classe = ?
            """
            
            params = [id_classe]
            if id_periode:
                query += " AND b.id_periode = ?"
                params.append(id_periode)
            
            query += " ORDER BY b.moyenne_generale DESC"
            
            cursor.execute(query, params)
            
            bulletins = []
            for row in cursor.fetchall():
                # Récupérer les matières pour ce bulletin
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
                
                bulletins.append(BulletinAvance(
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
                ))
            
            return bulletins
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des bulletins: {e}")
            return []
    
    def calculer_classement_classe(self, id_classe: int, id_periode: int):
        """Calcule le classement des élèves dans une classe"""
        try:
            bulletins = self.get_bulletins_by_classe(id_classe, id_periode)
            
            # Trier par moyenne décroissante
            bulletins.sort(key=lambda x: x.moyenne_generale, reverse=True)
            
            # Mettre à jour les rangs
            cursor = self.connection.cursor()
            
            for i, bulletin in enumerate(bulletins):
                rang = i + 1
                cursor.execute("""
                    UPDATE bulletins_avances 
                    SET rang_classe = ?, total_eleves_classe = ?, date_modification = GETDATE()
                    WHERE id = ?
                """, (rang, len(bulletins), bulletin.id))
            
            self.connection.commit()
            return bulletins
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul du classement: {e}")
            self.connection.rollback()
            return []
    
    def get_statistiques_classe(self, id_classe: int, id_periode: int = None) -> Dict:
        """Calcule les statistiques d'une classe"""
        try:
            bulletins = self.get_bulletins_by_classe(id_classe, id_periode)
            
            if not bulletins:
                return {
                    'total_eleves': 0,
                    'moyenne_classe': 0,
                    'meilleure_moyenne': 0,
                    'moins_bonne_moyenne': 0,
                    'taux_reussite': 0,
                    'distribution': {}
                }
            
            moyennes = [b.moyenne_generale for b in bulletins]
            
            # Distribution des notes
            distribution = {
                'excellent': len([m for m in moyennes if m >= 16]),
                'bien': len([m for m in moyennes if 14 <= m < 16]),
                'assez_bien': len([m for m in moyennes if 12 <= m < 14]),
                'passable': len([m for m in moyennes if 10 <= m < 12]),
                'insuffisant': len([m for m in moyennes if m < 10])
            }
            
            return {
                'total_eleves': len(bulletins),
                'moyenne_classe': sum(moyennes) / len(moyennes),
                'meilleure_moyenne': max(moyennes),
                'moins_bonne_moyenne': min(moyennes),
                'taux_reussite': len([m for m in moyennes if m >= 10]) / len(moyennes) * 100,
                'distribution': distribution
            }
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques: {e}")
            return {
                'total_eleves': 0,
                'moyenne_classe': 0,
                'meilleure_moyenne': 0,
                'moins_bonne_moyenne': 0,
                'taux_reussite': 0,
                'distribution': {}
            }


