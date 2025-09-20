# Modèle de données pour les présences
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class AttendanceModel:
    """Modèle de données pour une présence"""
    
    def __init__(self, eleve_id: int, classe_id: int, date: str, 
                 statut: str = "Présent", commentaire: str = "", 
                 justificatif_path: str = ""):
        self.eleve_id = eleve_id
        self.classe_id = classe_id
        self.date = date
        self.statut = statut
        self.commentaire = commentaire
        self.justificatif_path = justificatif_path
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convertit le modèle en dictionnaire"""
        return {
            'eleve_id': self.eleve_id,
            'classe_id': self.classe_id,
            'date': self.date,
            'statut': self.statut,
            'commentaire': self.commentaire,
            'justificatif_path': self.justificatif_path,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AttendanceModel':
        """Crée un modèle à partir d'un dictionnaire"""
        return cls(
            eleve_id=data.get('eleve_id'),
            classe_id=data.get('classe_id'),
            date=data.get('date'),
            statut=data.get('statut', 'Présent'),
            commentaire=data.get('commentaire', ''),
            justificatif_path=data.get('justificatif_path', '')
        )

class AttendanceStatsModel:
    """Modèle pour les statistiques de présence"""
    
    def __init__(self, total_jours: int = 0, presents: int = 0, 
                 absents: int = 0, retards: int = 0, justifies: int = 0):
        self.total_jours = total_jours
        self.presents = presents
        self.absents = absents
        self.retards = retards
        self.justifies = justifies
    
    @property
    def taux_presence(self) -> float:
        """Calcule le taux de présence"""
        if self.total_jours == 0:
            return 0.0
        return (self.presents / self.total_jours) * 100
    
    @property
    def taux_absence(self) -> float:
        """Calcule le taux d'absence"""
        if self.total_jours == 0:
            return 0.0
        return (self.absents / self.total_jours) * 100
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'total_jours': self.total_jours,
            'presents': self.presents,
            'absents': self.absents,
            'retards': self.retards,
            'justifies': self.justifies,
            'taux_presence': self.taux_presence,
            'taux_absence': self.taux_absence
        }

class AttendanceHistoryModel:
    """Modèle pour l'historique des présences"""
    
    def __init__(self, eleve_id: int, eleve_nom: str, classe_nom: str,
                 date: str, statut: str, commentaire: str = ""):
        self.eleve_id = eleve_id
        self.eleve_nom = eleve_nom
        self.classe_nom = classe_nom
        self.date = date
        self.statut = statut
        self.commentaire = commentaire
    
    def to_dict(self) -> Dict:
        """Convertit en dictionnaire"""
        return {
            'eleve_id': self.eleve_id,
            'eleve_nom': self.eleve_nom,
            'classe_nom': self.classe_nom,
            'date': self.date,
            'statut': self.statut,
            'commentaire': self.commentaire
        }
