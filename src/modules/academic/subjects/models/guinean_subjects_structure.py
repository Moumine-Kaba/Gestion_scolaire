# -*- coding: utf-8 -*-
"""
Structure des Matières du Système Éducatif Guinéen
EduManager+ - Organisation par Niveaux et Séries

Ce module définit la structure complète des matières selon le système éducatif guinéen :
- Primaire (CP1 → CM2)
- Collège (7ème → 10ème année)
- Lycée (11ème → 12ème année) avec séries spécialisées
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class EducationLevel(Enum):
    """Niveaux d'éducation du système guinéen"""
    PRIMAIRE = "primaire"
    COLLEGE = "college"
    LYCEE = "lycee"

class SchoolGrade(Enum):
    """Classes du système éducatif guinéen"""
    # Primaire
    CP1 = "CP1"
    CP2 = "CP2"
    CE1 = "CE1"
    CE2 = "CE2"
    CM1 = "CM1"
    CM2 = "CM2"
    
    # Collège
    SEPT = "7ème"
    HUIT = "8ème"
    NEUF = "9ème"
    DIX = "10ème"
    
    # Lycée
    ONZE = "11ème"
    DOUZE = "12ème"

class LyceeSeries(Enum):
    """Séries du lycée guinéen"""
    SCIENCES_MATH = "Sciences Mathématiques"
    SCIENCES_EXPERIMENTALES = "Sciences Expérimentales"
    LETTRES_SOCIALES = "Lettres / Sciences Sociales"
    TECHNIQUE = "Technique / Professionnelle"

@dataclass
class Subject:
    """Représente une matière scolaire"""
    code: str
    name: str
    description: str = ""
    coefficient: float = 1.0
    is_optional: bool = False
    is_core: bool = True  # Matière fondamentale
    prerequisites: List[str] = None
    
    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []

@dataclass
class GradeSubjects:
    """Matières pour une classe spécifique"""
    grade: SchoolGrade
    subjects: List[Subject]
    optional_subjects: List[Subject] = None
    
    def __post_init__(self):
        if self.optional_subjects is None:
            self.optional_subjects = []

@dataclass
class LyceeSeriesSubjects:
    """Matières pour une série du lycée"""
    series: LyceeSeries
    core_subjects: List[Subject]  # Matières communes
    specialized_subjects: List[Subject]  # Matières spécifiques à la série
    optional_subjects: List[Subject] = None
    
    def __post_init__(self):
        if self.optional_subjects is None:
            self.optional_subjects = []

class GuineanSubjectsStructure:
    """Structure complète des matières du système éducatif guinéen"""
    
    def __init__(self):
        self._structure = self._build_complete_structure()
    
    def _build_complete_structure(self) -> Dict[EducationLevel, Dict]:
        """Construit la structure complète des matières"""
        return {
            EducationLevel.PRIMAIRE: self._build_primaire_subjects(),
            EducationLevel.COLLEGE: self._build_college_subjects(),
            EducationLevel.LYCEE: self._build_lycee_subjects()
        }
    
    def _build_primaire_subjects(self) -> Dict[SchoolGrade, GradeSubjects]:
        """Matières du primaire (CP1 → CM2)"""
        # Matières communes à tous les niveaux du primaire
        common_subjects = [
            Subject("FR", "Français", "Langue française et communication", 4.0, False, True),
            Subject("MATH", "Mathématiques", "Calcul, géométrie et résolution de problèmes", 4.0, False, True),
            Subject("SCIOBS", "Sciences d'observation", "Découverte du monde naturel", 2.0, False, True),
            Subject("ECM", "Éducation civique et morale", "Civisme et valeurs morales", 2.0, False, True),
            Subject("ARTS", "Éducation artistique", "Dessin, musique et activités créatives", 1.5, False, False),
            Subject("EPS", "Éducation physique", "Activités physiques et sportives", 1.5, False, False),
        ]
        
        # Matières optionnelles selon l'école
        optional_subjects = [
            Subject("ANG", "Anglais", "Initiation à la langue anglaise", 1.0, True, False)
        ]
        
        primaire_structure = {}
        for grade in [SchoolGrade.CP1, SchoolGrade.CP2, SchoolGrade.CE1, 
                     SchoolGrade.CE2, SchoolGrade.CM1, SchoolGrade.CM2]:
            primaire_structure[grade] = GradeSubjects(
                grade=grade,
                subjects=common_subjects.copy(),
                optional_subjects=optional_subjects.copy()
            )
        
        return primaire_structure
    
    def _build_college_subjects(self) -> Dict[SchoolGrade, GradeSubjects]:
        """Matières du collège (7ème → 10ème année)"""
        # Matières communes à tous les niveaux du collège
        common_subjects = [
            Subject("FR", "Français", "Langue française, littérature et expression", 4.0, False, True),
            Subject("MATH", "Mathématiques", "Algèbre, géométrie et analyse", 4.0, False, True),
            Subject("ANG", "Anglais", "Langue anglaise et communication", 3.0, False, True),
            Subject("HISTGEO", "Histoire-Géographie", "Histoire du monde et géographie", 3.0, False, True),
            Subject("PHYSCHIM", "Physique-Chimie", "Sciences physiques et chimie", 3.0, False, True),
            Subject("BIO", "Biologie / SVT", "Sciences de la vie et de la terre", 2.5, False, True),
            Subject("ECM", "Éducation civique et morale", "Civisme, citoyenneté et éthique", 2.0, False, True),
            Subject("EPS", "Éducation physique", "Activités physiques et sportives", 2.0, False, False),
            Subject("TECH", "Technologie / Arts pratiques", "Technologies et arts appliqués", 2.0, False, False),
        ]
        
        # Matières optionnelles selon l'établissement
        optional_subjects = [
            Subject("ESP", "Espagnol", "Langue espagnole", 2.0, True, False),
            Subject("INFO", "Informatique", "Bureautique et bases de l'informatique", 2.0, True, False)
        ]
        
        college_structure = {}
        for grade in [SchoolGrade.SEPT, SchoolGrade.HUIT, SchoolGrade.NEUF, SchoolGrade.DIX]:
            college_structure[grade] = GradeSubjects(
                grade=grade,
                subjects=common_subjects.copy(),
                optional_subjects=optional_subjects.copy()
            )
        
        return college_structure
    
    def _build_lycee_subjects(self) -> Dict[LyceeSeries, LyceeSeriesSubjects]:
        """Matières du lycée (11ème → 12ème année) par série"""
        
        # Matières communes à toutes les séries
        common_subjects = [
            Subject("FR", "Français", "Langue française et littérature", 4.0, False, True),
            Subject("ANG", "Anglais", "Langue anglaise avancée", 3.0, False, True),
            Subject("ECM", "Éducation civique et morale", "Civisme et philosophie politique", 2.0, False, True),
            Subject("EPS", "Éducation physique", "Activités physiques et sportives", 1.5, False, False),
        ]
        
        # Série Sciences Mathématiques
        sciences_math_subjects = [
            Subject("MATH", "Mathématiques", "Mathématiques approfondies", 5.0, False, True),
            Subject("PHYS", "Physique", "Physique générale et appliquée", 4.0, False, True),
            Subject("CHIM", "Chimie", "Chimie générale et organique", 3.5, False, True),
        ]
        sciences_math_optionals = [
            Subject("INFO", "Informatique", "Programmation et algorithmique", 3.0, True, False),
            Subject("BIO", "Biologie", "Biologie optionnelle", 2.5, True, False),
        ]
        
        # Série Sciences Expérimentales
        sciences_exp_subjects = [
            Subject("BIO", "Biologie", "Biologie approfondie", 5.0, False, True),
            Subject("CHIM", "Chimie", "Chimie générale et organique", 4.0, False, True),
            Subject("PHYS", "Physique", "Physique générale", 3.5, False, True),
            Subject("MATH", "Mathématiques", "Mathématiques appliquées", 3.0, False, True),
        ]
        sciences_exp_optionals = [
            Subject("GEO", "Géologie", "Sciences de la terre", 2.5, True, False),
        ]
        
        # Série Lettres / Sciences Sociales
        lettres_subjects = [
            Subject("PHILO", "Philosophie", "Philosophie et logique", 4.0, False, True),
            Subject("HISTGEO", "Histoire-Géographie", "Histoire et géographie approfondies", 4.0, False, True),
            Subject("MATH", "Mathématiques", "Mathématiques appliquées", 2.5, False, True),
        ]
        lettres_optionals = [
            Subject("ECO", "Économie", "Économie générale", 3.0, True, False),
            Subject("ESP", "Espagnol", "Langue espagnole avancée", 3.0, True, False),
            Subject("ART", "Arts plastiques", "Arts et expression", 2.5, True, False),
        ]
        
        # Série Technique / Professionnelle
        technique_subjects = [
            Subject("TECH", "Technologie", "Technologies spécialisées", 5.0, False, True),
            Subject("MATH", "Mathématiques", "Mathématiques techniques", 3.0, False, True),
            Subject("PHYS", "Physique", "Physique appliquée", 3.0, False, True),
        ]
        technique_optionals = [
            Subject("INFO", "Informatique", "Informatique appliquée", 3.5, True, False),
            Subject("GEST", "Gestion", "Gestion et comptabilité", 3.0, True, False),
        ]
        
        return {
            LyceeSeries.SCIENCES_MATH: LyceeSeriesSubjects(
                series=LyceeSeries.SCIENCES_MATH,
                core_subjects=common_subjects.copy(),
                specialized_subjects=sciences_math_subjects,
                optional_subjects=sciences_math_optionals
            ),
            LyceeSeries.SCIENCES_EXPERIMENTALES: LyceeSeriesSubjects(
                series=LyceeSeries.SCIENCES_EXPERIMENTALES,
                core_subjects=common_subjects.copy(),
                specialized_subjects=sciences_exp_subjects,
                optional_subjects=sciences_exp_optionals
            ),
            LyceeSeries.LETTRES_SOCIALES: LyceeSeriesSubjects(
                series=LyceeSeries.LETTRES_SOCIALES,
                core_subjects=common_subjects.copy(),
                specialized_subjects=lettres_subjects,
                optional_subjects=lettres_optionals
            ),
            LyceeSeries.TECHNIQUE: LyceeSeriesSubjects(
                series=LyceeSeries.TECHNIQUE,
                core_subjects=common_subjects.copy(),
                specialized_subjects=technique_subjects,
                optional_subjects=technique_optionals
            )
        }
    
    def get_subjects_by_level(self, level: EducationLevel) -> Dict:
        """Récupère les matières par niveau d'éducation"""
        return self._structure.get(level, {})
    
    def get_subjects_by_grade(self, grade: SchoolGrade) -> Optional[GradeSubjects]:
        """Récupère les matières pour une classe spécifique"""
        if grade in [g for g in SchoolGrade if g.value in ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"]]:
            return self._structure[EducationLevel.PRIMAIRE].get(grade)
        elif grade in [g for g in SchoolGrade if g.value in ["7ème", "8ème", "9ème", "10ème"]]:
            return self._structure[EducationLevel.COLLEGE].get(grade)
        return None
    
    def get_subjects_by_series(self, series: LyceeSeries) -> Optional[LyceeSeriesSubjects]:
        """Récupère les matières pour une série du lycée"""
        return self._structure[EducationLevel.LYCEE].get(series)
    
    def get_all_subjects_for_grade(self, grade: SchoolGrade) -> List[Subject]:
        """Récupère toutes les matières (obligatoires + optionnelles) pour une classe"""
        grade_subjects = self.get_subjects_by_grade(grade)
        if grade_subjects:
            all_subjects = grade_subjects.subjects.copy()
            all_subjects.extend(grade_subjects.optional_subjects)
            return all_subjects
        return []
    
    def get_all_subjects_for_series(self, series: LyceeSeries) -> List[Subject]:
        """Récupère toutes les matières pour une série du lycée"""
        series_subjects = self.get_subjects_by_series(series)
        if series_subjects:
            all_subjects = series_subjects.core_subjects.copy()
            all_subjects.extend(series_subjects.specialized_subjects)
            all_subjects.extend(series_subjects.optional_subjects)
            return all_subjects
        return []
    
    def get_core_subjects_only(self, grade: SchoolGrade) -> List[Subject]:
        """Récupère uniquement les matières fondamentales pour une classe"""
        grade_subjects = self.get_subjects_by_grade(grade)
        if grade_subjects:
            return [s for s in grade_subjects.subjects if s.is_core]
        return []
    
    def get_optional_subjects_only(self, grade: SchoolGrade) -> List[Subject]:
        """Récupère uniquement les matières optionnelles pour une classe"""
        grade_subjects = self.get_subjects_by_grade(grade)
        if grade_subjects:
            return grade_subjects.optional_subjects
        return []
    
    def get_subject_by_code(self, code: str) -> Optional[Subject]:
        """Recherche une matière par son code"""
        for level_data in self._structure.values():
            if isinstance(level_data, dict):
                for grade_data in level_data.values():
                    if isinstance(grade_data, (GradeSubjects, LyceeSeriesSubjects)):
                        # Chercher dans les matières principales
                        for subject in grade_data.subjects:
                            if subject.code == code:
                                return subject
                        # Chercher dans les matières optionnelles
                        for subject in grade_data.optional_subjects:
                            if subject.code == code:
                                return subject
                        # Pour le lycée, chercher aussi dans les matières spécialisées
                        if hasattr(grade_data, 'specialized_subjects'):
                            for subject in grade_data.specialized_subjects:
                                if subject.code == code:
                                    return subject
        return None
    
    def get_statistics(self) -> Dict:
        """Retourne des statistiques sur la structure des matières"""
        stats = {
            "primaire": {
                "grades_count": len(self._structure[EducationLevel.PRIMAIRE]),
                "total_subjects": 0
            },
            "college": {
                "grades_count": len(self._structure[EducationLevel.COLLEGE]),
                "total_subjects": 0
            },
            "lycee": {
                "series_count": len(self._structure[EducationLevel.LYCEE]),
                "total_subjects": 0
            }
        }
        
        # Compter les matières pour chaque niveau
        for grade_data in self._structure[EducationLevel.PRIMAIRE].values():
            stats["primaire"]["total_subjects"] += len(grade_data.subjects)
        
        for grade_data in self._structure[EducationLevel.COLLEGE].values():
            stats["college"]["total_subjects"] += len(grade_data.subjects)
        
        for series_data in self._structure[EducationLevel.LYCEE].values():
            stats["lycee"]["total_subjects"] += len(series_data.core_subjects) + len(series_data.specialized_subjects)
        
        return stats

# Instance globale pour l'utilisation dans l'application
GUINEAN_SUBJECTS = GuineanSubjectsStructure()

def get_guinean_subjects_structure() -> GuineanSubjectsStructure:
    """Retourne l'instance globale de la structure des matières guinéennes"""
    return GUINEAN_SUBJECTS

# Fonctions utilitaires pour l'intégration
def get_subjects_for_grade_name(grade_name: str) -> List[Dict]:
    """Retourne les matières pour un nom de classe (ex: 'CM1', '9ème', '11ème Sciences Math')"""
    try:
        # Primaire et Collège
        if grade_name in [g.value for g in SchoolGrade]:
            grade = SchoolGrade(grade_name)
            subjects = GUINEAN_SUBJECTS.get_all_subjects_for_grade(grade)
            return [{"code": s.code, "name": s.name, "description": s.description, 
                    "coefficient": s.coefficient, "is_optional": s.is_optional, "is_core": s.is_core} 
                   for s in subjects]
        
        # Lycée avec série
        elif "11ème" in grade_name or "12ème" in grade_name:
            # Extraire la série du nom
            for series in LyceeSeries:
                if series.value in grade_name:
                    subjects = GUINEAN_SUBJECTS.get_all_subjects_for_series(series)
                    return [{"code": s.code, "name": s.name, "description": s.description,
                            "coefficient": s.coefficient, "is_optional": s.is_optional, "is_core": s.is_core}
                           for s in subjects]
        
        return []
    except Exception as e:
        print(f"Erreur lors de la récupération des matières pour {grade_name}: {e}")
        return []

def get_available_grades() -> List[str]:
    """Retourne la liste de toutes les classes disponibles"""
    grades = []
    
    # Primaire
    for grade in SchoolGrade:
        if grade.value in ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"]:
            grades.append(grade.value)
    
    # Collège
    for grade in SchoolGrade:
        if grade.value in ["7ème", "8ème", "9ème", "10ème"]:
            grades.append(grade.value)
    
    # Lycée
    for series in LyceeSeries:
        grades.append(f"11ème {series.value}")
        grades.append(f"12ème {series.value}")
    
    return grades

def get_education_level_for_grade(grade_name: str) -> str:
    """Détermine le niveau d'éducation pour une classe donnée"""
    if grade_name in ["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"]:
        return "primaire"
    elif grade_name in ["7ème", "8ème", "9ème", "10ème"]:
        return "college"
    elif "11ème" in grade_name or "12ème" in grade_name:
        return "lycee"
    return "inconnu"
