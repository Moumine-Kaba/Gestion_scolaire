# -*- coding: utf-8 -*-
"""
Contrôleur pour les Matières du Système Éducatif Guinéen
EduManager+ - Gestion Centralisée des Matières par Niveau

Ce contrôleur fournit une interface unifiée pour gérer les matières
organisées selon le système éducatif guinéen.
"""

import os
import sys
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.academic.subjects.models.guinean_subject_model import (
    GuineanSubjectModel, GuineanSubjectRecord, get_guinean_subject_model
)
from src.modules.academic.subjects.models.guinean_subjects_structure import (
    GuineanSubjectsStructure, EducationLevel, SchoolGrade, LyceeSeries,
    get_guinean_subjects_structure, get_subjects_for_grade_name,
    get_available_grades, get_education_level_for_grade
)

class GuineanSubjectsController:
    """Contrôleur principal pour la gestion des matières guinéennes"""
    
    def __init__(self):
        self.model = get_guinean_subject_model()
        self.structure = get_guinean_subjects_structure()
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialise le système de matières guinéennes"""
        try:
            # S'assurer que les tables existent
            self.model._ensure_tables_exist()
            
            # Initialiser avec les données par défaut si nécessaire
            self.model.initialize_default_subjects()
            
            print("✅ Système de matières guinéennes initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation du système : {e}")
    
    # === MÉTHODES DE RÉCUPÉRATION DES DONNÉES ===
    
    def get_all_subjects(self) -> List[Dict]:
        """Récupère toutes les matières de tous les niveaux"""
        try:
            all_subjects = []
            
            # Récupérer par niveau
            for level in ["primaire", "college", "lycee"]:
                subjects = self.model.get_subjects_by_level(level)
                for subject in subjects:
                    all_subjects.append(self._subject_record_to_dict(subject))
            
            return all_subjects
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de toutes les matières : {e}")
            return []
    
    def get_subjects_by_level(self, level: str) -> List[Dict]:
        """Récupère les matières d'un niveau d'éducation spécifique"""
        try:
            subjects = self.model.get_subjects_by_level(level)
            return [self._subject_record_to_dict(subject) for subject in subjects]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières du niveau {level} : {e}")
            return []
    
    def get_subjects_by_grade(self, grade: str) -> List[Dict]:
        """Récupère les matières d'une classe spécifique"""
        try:
            subjects = self.model.get_subjects_by_grade(grade)
            return [self._subject_record_to_dict(subject) for subject in subjects]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières de la classe {grade} : {e}")
            return []
    
    def get_core_subjects_by_grade(self, grade: str) -> List[Dict]:
        """Récupère uniquement les matières fondamentales d'une classe"""
        try:
            subjects = self.model.get_core_subjects_by_grade(grade)
            return [self._subject_record_to_dict(subject) for subject in subjects]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières fondamentales de {grade} : {e}")
            return []
    
    def get_optional_subjects_by_grade(self, grade: str) -> List[Dict]:
        """Récupère uniquement les matières optionnelles d'une classe"""
        try:
            subjects = self.model.get_optional_subjects_by_grade(grade)
            return [self._subject_record_to_dict(subject) for subject in subjects]
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières optionnelles de {grade} : {e}")
            return []
    
    def get_subject_by_code(self, code: str) -> Optional[Dict]:
        """Récupère une matière par son code"""
        try:
            subject = self.model.get_subject_by_code(code)
            return self._subject_record_to_dict(subject) if subject else None
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la matière {code} : {e}")
            return None
    
    def search_subjects(self, query: str, level: str = None, grade: str = None) -> List[Dict]:
        """Recherche des matières par nom, description ou code"""
        try:
            subjects = self.model.search_subjects(query, level, grade)
            return [self._subject_record_to_dict(subject) for subject in subjects]
        except Exception as e:
            print(f"❌ Erreur lors de la recherche des matières : {e}")
            return []
    
    # === MÉTHODES D'INFORMATION ===
    
    def get_available_grades(self) -> List[str]:
        """Récupère la liste de toutes les classes disponibles"""
        try:
            return self.model.get_available_grades()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des classes : {e}")
            return []
    
    def get_education_levels(self) -> List[str]:
        """Récupère la liste des niveaux d'éducation"""
        try:
            return self.model.get_education_levels()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des niveaux : {e}")
            return []
    
    def get_education_level_for_grade(self, grade: str) -> str:
        """Détermine le niveau d'éducation pour une classe donnée"""
        return get_education_level_for_grade(grade)
    
    def get_statistics(self) -> Dict:
        """Récupère des statistiques complètes sur les matières"""
        try:
            return self.model.get_statistics()
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des statistiques : {e}")
            return {}
    
    # === MÉTHODES DE GESTION ===
    
    def add_custom_subject(self, subject_data: Dict) -> bool:
        """Ajoute une matière personnalisée"""
        try:
            # Validation des données
            if not self._validate_subject_data(subject_data):
                return False
            
            return self.model.add_custom_subject(subject_data)
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de la matière personnalisée : {e}")
            return False
    
    def update_subject(self, subject_id: int, subject_data: Dict) -> bool:
        """Met à jour une matière existante"""
        try:
            # Validation des données
            if not self._validate_subject_data(subject_data, is_update=True):
                return False
            
            return self.model.update_subject(subject_id, subject_data)
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de la matière : {e}")
            return False
    
    def deactivate_subject(self, subject_id: int) -> bool:
        """Désactive une matière (suppression logique)"""
        try:
            return self.model.deactivate_subject(subject_id)
        except Exception as e:
            print(f"❌ Erreur lors de la désactivation de la matière : {e}")
            return False
    
    # === MÉTHODES UTILITAIRES ===
    
    def _subject_record_to_dict(self, subject: GuineanSubjectRecord) -> Dict:
        """Convertit un enregistrement de matière en dictionnaire"""
        if not subject:
            return {}
        
        return {
            "id": subject.id,
            "code": subject.code,
            "name": subject.name,
            "description": subject.description,
            "coefficient": subject.coefficient,
            "education_level": subject.education_level,
            "grade": subject.grade,
            "series": subject.series,
            "is_optional": subject.is_optional,
            "is_core": subject.is_core,
            "is_active": subject.is_active,
            "date_created": subject.date_created,
            "date_updated": subject.date_updated
        }
    
    def _validate_subject_data(self, data: Dict, is_update: bool = False) -> bool:
        """Valide les données d'une matière"""
        try:
            # Champs obligatoires
            required_fields = ["name", "education_level", "grade"]
            for field in required_fields:
                if not data.get(field):
                    print(f"❌ Le champ '{field}' est obligatoire")
                    return False
            
            # Validation du coefficient
            coefficient = data.get("coefficient", 1.0)
            if not isinstance(coefficient, (int, float)) or coefficient <= 0:
                print("❌ Le coefficient doit être un nombre positif")
                return False
            
            # Validation du niveau d'éducation
            valid_levels = ["primaire", "college", "lycee"]
            if data.get("education_level") not in valid_levels:
                print(f"❌ Le niveau d'éducation doit être parmi : {valid_levels}")
                return False
            
            return True
        except Exception as e:
            print(f"❌ Erreur lors de la validation des données : {e}")
            return False
    
    # === MÉTHODES SPÉCIALISÉES POUR L'INTÉGRATION ===
    
    def get_subjects_for_form(self, grade: str) -> Tuple[List[Dict], List[Dict]]:
        """Récupère les matières organisées pour les formulaires (obligatoires + optionnelles)"""
        try:
            core_subjects = self.get_core_subjects_by_grade(grade)
            optional_subjects = self.get_optional_subjects_by_grade(grade)
            return core_subjects, optional_subjects
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières pour formulaire : {e}")
            return [], []
    
    def get_subjects_for_notes_entry(self, grade: str) -> List[Dict]:
        """Récupère les matières pour la saisie des notes (toutes les matières actives)"""
        try:
            return self.get_subjects_by_grade(grade)
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières pour notes : {e}")
            return []
    
    def get_subjects_for_bulletin(self, grade: str, include_optional: bool = False) -> List[Dict]:
        """Récupère les matières pour la génération de bulletins"""
        try:
            if include_optional:
                return self.get_subjects_by_grade(grade)
            else:
                return self.get_core_subjects_by_grade(grade)
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières pour bulletin : {e}")
            return []
    
    def get_subjects_for_timetable(self, grade: str) -> List[Dict]:
        """Récupère les matières pour la gestion des emplois du temps"""
        try:
            # Pour les emplois du temps, on prend toutes les matières sauf EPS si nécessaire
            subjects = self.get_subjects_by_grade(grade)
            # Filtrer EPS si nécessaire (à adapter selon les besoins)
            return subjects
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières pour emploi du temps : {e}")
            return []
    
    def get_grade_hierarchy(self) -> Dict[str, List[str]]:
        """Récupère la hiérarchie des classes par niveau"""
        try:
            hierarchy = {}
            grades = self.get_available_grades()
            
            for grade in grades:
                level = self.get_education_level_for_grade(grade)
                if level not in hierarchy:
                    hierarchy[level] = []
                hierarchy[level].append(grade)
            
            # Trier les classes dans chaque niveau
            for level in hierarchy:
                hierarchy[level].sort()
            
            return hierarchy
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la hiérarchie : {e}")
            return {}
    
    def export_subjects_structure(self, format_type: str = "dict") -> Dict:
        """Exporte la structure complète des matières"""
        try:
            if format_type == "dict":
                structure = {}
                
                # Récupérer par niveau
                for level in ["primaire", "college", "lycee"]:
                    level_data = {}
                    grades = [grade for grade in self.get_available_grades() 
                             if self.get_education_level_for_grade(grade) == level]
                    
                    for grade in grades:
                        subjects = self.get_subjects_by_grade(grade)
                        level_data[grade] = subjects
                    
                    structure[level] = level_data
                
                return structure
            else:
                print(f"❌ Format d'export non supporté : {format_type}")
                return {}
        except Exception as e:
            print(f"❌ Erreur lors de l'export de la structure : {e}")
            return {}
    
    def import_custom_subjects(self, subjects_data: List[Dict]) -> Tuple[int, int]:
        """Importe des matières personnalisées"""
        try:
            success_count = 0
            error_count = 0
            
            for subject_data in subjects_data:
                if self.add_custom_subject(subject_data):
                    success_count += 1
                else:
                    error_count += 1
            
            print(f"✅ Import terminé : {success_count} réussites, {error_count} erreurs")
            return success_count, error_count
        except Exception as e:
            print(f"❌ Erreur lors de l'import des matières : {e}")
            return 0, len(subjects_data)
    
    def reset_to_default_structure(self) -> bool:
        """Remet à zéro et réinitialise avec la structure par défaut"""
        try:
            # Désactiver toutes les matières existantes
            conn = self.model._connect()
            if conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE guinean_subjects SET is_active = 0")
                conn.commit()
                conn.close()
            
            # Réinitialiser avec les données par défaut
            return self.model.initialize_default_subjects()
        except Exception as e:
            print(f"❌ Erreur lors de la réinitialisation : {e}")
            return False
    
    def _subject_record_to_dict(self, subject_record) -> Dict:
        """Convertit un enregistrement de matière en dictionnaire"""
        try:
            if hasattr(subject_record, '__dict__'):
                # Si c'est un objet avec des attributs
                return {
                    'id': getattr(subject_record, 'id', None),
                    'code': getattr(subject_record, 'code', ''),
                    'name': getattr(subject_record, 'name', ''),
                    'description': getattr(subject_record, 'description', ''),
                    'coefficient': float(getattr(subject_record, 'coefficient', 1.0)),
                    'education_level': getattr(subject_record, 'education_level', ''),
                    'grade': getattr(subject_record, 'grade', ''),
                    'series': getattr(subject_record, 'series', ''),
                    'is_optional': bool(getattr(subject_record, 'is_optional', False)),
                    'is_core': bool(getattr(subject_record, 'is_core', True)),
                    'is_active': bool(getattr(subject_record, 'is_active', True)),
                    'date_created': getattr(subject_record, 'date_created', None),
                    'date_updated': getattr(subject_record, 'date_updated', None)
                }
            elif isinstance(subject_record, dict):
                # Si c'est déjà un dictionnaire
                return subject_record
            else:
                # Fallback
                return {
                    'id': None,
                    'code': '',
                    'name': str(subject_record),
                    'description': '',
                    'coefficient': 1.0,
                    'education_level': '',
                    'grade': '',
                    'series': '',
                    'is_optional': False,
                    'is_core': True,
                    'is_active': True,
                    'date_created': None,
                    'date_updated': None
                }
        except Exception as e:
            print(f"❌ Erreur conversion subject_record_to_dict: {e}")
            return {
                'id': None,
                'code': '',
                'name': 'Erreur',
                'description': '',
                'coefficient': 1.0,
                'education_level': '',
                'grade': '',
                'series': '',
                'is_optional': False,
                'is_core': True,
                'is_active': True,
                'date_created': None,
                'date_updated': None
            }

# Instance globale pour l'utilisation dans l'application
guinean_subjects_controller = GuineanSubjectsController()

def get_guinean_subjects_controller() -> GuineanSubjectsController:
    """Retourne l'instance globale du contrôleur de matières guinéennes"""
    return guinean_subjects_controller

# === FONCTIONS UTILITAIRES POUR L'INTÉGRATION ===

def get_subjects_for_grade(grade: str) -> List[Dict]:
    """Fonction utilitaire pour récupérer les matières d'une classe"""
    controller = get_guinean_subjects_controller()
    return controller.get_subjects_by_grade(grade)

def get_core_subjects_for_grade(grade: str) -> List[Dict]:
    """Fonction utilitaire pour récupérer les matières fondamentales d'une classe"""
    controller = get_guinean_subjects_controller()
    return controller.get_core_subjects_by_grade(grade)

def get_optional_subjects_for_grade(grade: str) -> List[Dict]:
    """Fonction utilitaire pour récupérer les matières optionnelles d'une classe"""
    controller = get_guinean_subjects_controller()
    return controller.get_optional_subjects_by_grade(grade)

def search_subjects_by_name(query: str) -> List[Dict]:
    """Fonction utilitaire pour rechercher des matières par nom"""
    controller = get_guinean_subjects_controller()
    return controller.search_subjects(query)

def get_all_available_grades() -> List[str]:
    """Fonction utilitaire pour récupérer toutes les classes"""
    controller = get_guinean_subjects_controller()
    return controller.get_available_grades()

def get_grade_education_level(grade: str) -> str:
    """Fonction utilitaire pour déterminer le niveau d'une classe"""
    controller = get_guinean_subjects_controller()
    return controller.get_education_level_for_grade(grade)
