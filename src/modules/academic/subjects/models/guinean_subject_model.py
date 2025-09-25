# -*- coding: utf-8 -*-
"""
Modèle de Base de Données pour les Matières du Système Éducatif Guinéen
EduManager+ - Intégration avec SQL Server

Ce module gère la persistance des matières organisées par niveau et série
selon le système éducatif guinéen.
"""

import os
import sys
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_db_connection
from .guinean_subjects_structure import (
    GuineanSubjectsStructure, EducationLevel, SchoolGrade, LyceeSeries,
    Subject, GradeSubjects, LyceeSeriesSubjects, get_guinean_subjects_structure
)

@dataclass
class GuineanSubjectRecord:
    """Enregistrement de matière dans la base de données"""
    id: int = None
    code: str = ""
    name: str = ""
    description: str = ""
    coefficient: float = 1.0
    education_level: str = ""  # "primaire", "college", "lycee"
    grade: str = ""  # "CP1", "7ème", "11ème Sciences Math", etc.
    series: str = ""  # Pour le lycée : "Sciences Mathématiques", etc.
    is_optional: bool = False
    is_core: bool = True
    is_active: bool = True
    date_created: datetime = None
    date_updated: datetime = None

class GuineanSubjectModel:
    """Modèle de base de données pour les matières guinéennes"""
    
    def __init__(self):
        self.structure = get_guinean_subjects_structure()
        self._ensure_tables_exist()
    
    def _connect(self):
        """Établit une connexion à la base de données"""
        try:
            conn = get_db_connection()
            return conn
        except Exception as e:
            print(f"❌ Erreur de connexion à la base de données : {e}")
            return None
    
    def _ensure_tables_exist(self):
        """Crée les tables nécessaires si elles n'existent pas"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Table principale des matières guinéennes
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'guinean_subjects')
                CREATE TABLE guinean_subjects (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    code NVARCHAR(100) NOT NULL UNIQUE,
                    name NVARCHAR(200) NOT NULL,
                    description NVARCHAR(500),
                    coefficient DECIMAL(3,2) DEFAULT 1.0,
                    education_level NVARCHAR(20) NOT NULL,
                    grade NVARCHAR(50) NOT NULL,
                    series NVARCHAR(100),
                    is_optional BIT DEFAULT 0,
                    is_core BIT DEFAULT 1,
                    is_active BIT DEFAULT 1,
                    date_created DATETIME DEFAULT GETDATE(),
                    date_updated DATETIME DEFAULT GETDATE()
                )
            """)
            
            # Index pour optimiser les recherches
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_guinean_subjects_level_grade')
                CREATE INDEX IX_guinean_subjects_level_grade 
                ON guinean_subjects (education_level, grade)
            """)
            
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_guinean_subjects_code')
                CREATE INDEX IX_guinean_subjects_code 
                ON guinean_subjects (code)
            """)
            
            conn.commit()
            conn.close()
            print("✅ Tables et index pour les matières guinéennes créés avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des tables : {e}")
            return False
    
    def initialize_default_subjects(self) -> bool:
        """Initialise la base de données avec toutes les matières du système guinéen"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            
            # Vérifier si des données existent déjà
            cursor.execute("SELECT COUNT(*) FROM guinean_subjects")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print("ℹ️ Des matières existent déjà dans la base de données")
                conn.close()
                return True
            
            # Insérer les matières du primaire
            self._insert_primaire_subjects(cursor)
            
            # Insérer les matières du collège
            self._insert_college_subjects(cursor)
            
            # Insérer les matières du lycée
            self._insert_lycee_subjects(cursor)
            
            conn.commit()
            conn.close()
            
            print("✅ Initialisation des matières guinéennes terminée avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'initialisation des matières : {e}")
            return False
    
    def _insert_primaire_subjects(self, cursor):
        """Insère les matières du primaire"""
        primaire_data = self.structure.get_subjects_by_level(EducationLevel.PRIMAIRE)
        
        for grade, grade_subjects in primaire_data.items():
            grade_name = grade.value
            
            # Matières obligatoires
            for subject in grade_subjects.subjects:
                unique_code = f"{subject.code}_{grade_name}"
                cursor.execute("""
                    INSERT INTO guinean_subjects 
                    (code, name, description, coefficient, education_level, grade, is_optional, is_core)
                    VALUES (?, ?, ?, ?, 'primaire', ?, ?, ?)
                """, (unique_code, subject.name, subject.description, subject.coefficient, 
                     grade_name, subject.is_optional, subject.is_core))
            
            # Matières optionnelles
            for subject in grade_subjects.optional_subjects:
                unique_code = f"{subject.code}_{grade_name}"
                cursor.execute("""
                    INSERT INTO guinean_subjects 
                    (code, name, description, coefficient, education_level, grade, is_optional, is_core)
                    VALUES (?, ?, ?, ?, 'primaire', ?, ?, ?)
                """, (unique_code, subject.name, subject.description, subject.coefficient, 
                     grade_name, subject.is_optional, subject.is_core))
    
    def _insert_college_subjects(self, cursor):
        """Insère les matières du collège"""
        college_data = self.structure.get_subjects_by_level(EducationLevel.COLLEGE)
        
        for grade, grade_subjects in college_data.items():
            grade_name = grade.value
            
            # Matières obligatoires
            for subject in grade_subjects.subjects:
                unique_code = f"{subject.code}_{grade_name}"
                cursor.execute("""
                    INSERT INTO guinean_subjects 
                    (code, name, description, coefficient, education_level, grade, is_optional, is_core)
                    VALUES (?, ?, ?, ?, 'college', ?, ?, ?)
                """, (unique_code, subject.name, subject.description, subject.coefficient, 
                     grade_name, subject.is_optional, subject.is_core))
            
            # Matières optionnelles
            for subject in grade_subjects.optional_subjects:
                unique_code = f"{subject.code}_{grade_name}"
                cursor.execute("""
                    INSERT INTO guinean_subjects 
                    (code, name, description, coefficient, education_level, grade, is_optional, is_core)
                    VALUES (?, ?, ?, ?, 'college', ?, ?, ?)
                """, (unique_code, subject.name, subject.description, subject.coefficient, 
                     grade_name, subject.is_optional, subject.is_core))
    
    def _insert_lycee_subjects(self, cursor):
        """Insère les matières du lycée"""
        lycee_data = self.structure.get_subjects_by_level(EducationLevel.LYCEE)
        
        for series, series_subjects in lycee_data.items():
            series_name = series.value
            
            # Matières communes (11ème et 12ème)
            for grade_suffix in ["11ème", "12ème"]:
                grade_name = f"{grade_suffix} {series_name}"
                
                # Matières communes
                for subject in series_subjects.core_subjects:
                    unique_code = f"{subject.code}_{grade_suffix}_{series_name.replace(' ', '_')}"
                    cursor.execute("""
                        INSERT INTO guinean_subjects 
                        (code, name, description, coefficient, education_level, grade, series, is_optional, is_core)
                        VALUES (?, ?, ?, ?, 'lycee', ?, ?, ?, ?)
                    """, (unique_code, subject.name, subject.description, subject.coefficient, 
                         grade_name, series_name, subject.is_optional, subject.is_core))
                
                # Matières spécialisées
                for subject in series_subjects.specialized_subjects:
                    unique_code = f"{subject.code}_{grade_suffix}_{series_name.replace(' ', '_')}"
                    cursor.execute("""
                        INSERT INTO guinean_subjects 
                        (code, name, description, coefficient, education_level, grade, series, is_optional, is_core)
                        VALUES (?, ?, ?, ?, 'lycee', ?, ?, ?, ?)
                    """, (unique_code, subject.name, subject.description, subject.coefficient, 
                         grade_name, series_name, subject.is_optional, subject.is_core))
                
                # Matières optionnelles
                for subject in series_subjects.optional_subjects:
                    unique_code = f"{subject.code}_{grade_suffix}_{series_name.replace(' ', '_')}"
                    cursor.execute("""
                        INSERT INTO guinean_subjects 
                        (code, name, description, coefficient, education_level, grade, series, is_optional, is_core)
                        VALUES (?, ?, ?, ?, 'lycee', ?, ?, ?, ?)
                    """, (unique_code, subject.name, subject.description, subject.coefficient, 
                         grade_name, series_name, subject.is_optional, subject.is_core))
    
    def get_subjects_by_level(self, level: str) -> List[GuineanSubjectRecord]:
        """Récupère toutes les matières d'un niveau d'éducation"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE education_level = ? AND is_active = 1
                ORDER BY grade, is_core DESC, name
            """, (level,))
            
            rows = cursor.fetchall()
            subjects = []
            
            for row in rows:
                subject = GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
                subjects.append(subject)
            
            conn.close()
            return subjects
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières par niveau : {e}")
            return []
    
    def get_subjects_by_grade(self, grade: str) -> List[GuineanSubjectRecord]:
        """Récupère toutes les matières d'une classe spécifique"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE grade = ? AND is_active = 1
                ORDER BY is_core DESC, coefficient DESC, name
            """, (grade,))
            
            rows = cursor.fetchall()
            subjects = []
            
            for row in rows:
                subject = GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
                subjects.append(subject)
            
            conn.close()
            return subjects
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières par classe : {e}")
            return []
    
    def get_core_subjects_by_grade(self, grade: str) -> List[GuineanSubjectRecord]:
        """Récupère uniquement les matières fondamentales d'une classe"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE grade = ? AND is_core = 1 AND is_active = 1
                ORDER BY coefficient DESC, name
            """, (grade,))
            
            rows = cursor.fetchall()
            subjects = []
            
            for row in rows:
                subject = GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
                subjects.append(subject)
            
            conn.close()
            return subjects
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières fondamentales : {e}")
            return []
    
    def get_optional_subjects_by_grade(self, grade: str) -> List[GuineanSubjectRecord]:
        """Récupère uniquement les matières optionnelles d'une classe"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE grade = ? AND is_optional = 1 AND is_active = 1
                ORDER BY name
            """, (grade,))
            
            rows = cursor.fetchall()
            subjects = []
            
            for row in rows:
                subject = GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
                subjects.append(subject)
            
            conn.close()
            return subjects
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des matières optionnelles : {e}")
            return []
    
    def get_subject_by_code(self, code: str) -> Optional[GuineanSubjectRecord]:
        """Récupère une matière par son code"""
        try:
            conn = self._connect()
            if not conn:
                return None
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE code = ? AND is_active = 1
            """, (code,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
            return None
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la matière par code : {e}")
            return None
    
    def search_subjects(self, query: str, level: str = None, grade: str = None) -> List[GuineanSubjectRecord]:
        """Recherche des matières par nom ou description"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            
            # Construire la requête dynamiquement
            sql = """
                SELECT id, code, name, description, coefficient, education_level, 
                       grade, series, is_optional, is_core, is_active, date_created, date_updated
                FROM guinean_subjects 
                WHERE (name LIKE ? OR description LIKE ? OR code LIKE ?) AND is_active = 1
            """
            params = [f"%{query}%", f"%{query}%", f"%{query}%"]
            
            if level:
                sql += " AND education_level = ?"
                params.append(level)
            
            if grade:
                sql += " AND grade = ?"
                params.append(grade)
            
            sql += " ORDER BY education_level, grade, is_core DESC, name"
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            subjects = []
            for row in rows:
                subject = GuineanSubjectRecord(
                    id=row[0],
                    code=row[1],
                    name=row[2],
                    description=row[3] or "",
                    coefficient=float(row[4]),
                    education_level=row[5],
                    grade=row[6],
                    series=row[7] or "",
                    is_optional=bool(row[8]),
                    is_core=bool(row[9]),
                    is_active=bool(row[10]),
                    date_created=row[11],
                    date_updated=row[12]
                )
                subjects.append(subject)
            
            conn.close()
            return subjects
            
        except Exception as e:
            print(f"❌ Erreur lors de la recherche des matières : {e}")
            return []
    
    def get_available_grades(self) -> List[str]:
        """Récupère la liste de toutes les classes disponibles"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT grade, education_level
                FROM guinean_subjects 
                WHERE is_active = 1
                GROUP BY grade, education_level
                ORDER BY 
                    CASE 
                        WHEN education_level = 'primaire' THEN 1
                        WHEN education_level = 'college' THEN 2
                        WHEN education_level = 'lycee' THEN 3
                        ELSE 4
                    END,
                    grade
            """)
            
            rows = cursor.fetchall()
            grades = [row[0] for row in rows]
            
            conn.close()
            return grades
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des classes : {e}")
            return []
    
    def get_education_levels(self) -> List[str]:
        """Récupère la liste des niveaux d'éducation"""
        try:
            conn = self._connect()
            if not conn:
                return []
            
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT education_level 
                FROM guinean_subjects 
                WHERE is_active = 1
                ORDER BY 
                    CASE 
                        WHEN education_level = 'primaire' THEN 1
                        WHEN education_level = 'college' THEN 2
                        WHEN education_level = 'lycee' THEN 3
                        ELSE 4
                    END
            """)
            
            rows = cursor.fetchall()
            levels = [row[0] for row in rows]
            
            conn.close()
            return levels
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des niveaux : {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Récupère des statistiques sur les matières"""
        try:
            conn = self._connect()
            if not conn:
                return {}
            
            cursor = conn.cursor()
            
            # Statistiques générales
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_subjects,
                    COUNT(DISTINCT grade) as total_grades,
                    COUNT(DISTINCT education_level) as total_levels,
                    AVG(coefficient) as avg_coefficient
                FROM guinean_subjects 
                WHERE is_active = 1
            """)
            
            stats_row = cursor.fetchone()
            
            # Statistiques par niveau
            cursor.execute("""
                SELECT 
                    education_level,
                    COUNT(*) as subject_count,
                    COUNT(DISTINCT grade) as grade_count
                FROM guinean_subjects 
                WHERE is_active = 1
                GROUP BY education_level
                ORDER BY 
                    CASE 
                        WHEN education_level = 'primaire' THEN 1
                        WHEN education_level = 'college' THEN 2
                        WHEN education_level = 'lycee' THEN 3
                        ELSE 4
                    END
            """)
            
            level_stats = []
            for row in cursor.fetchall():
                level_stats.append({
                    "level": row[0],
                    "subject_count": row[1],
                    "grade_count": row[2]
                })
            
            conn.close()
            
            return {
                "total_subjects": stats_row[0],
                "total_grades": stats_row[1],
                "total_levels": stats_row[2],
                "average_coefficient": float(stats_row[3]) if stats_row[3] else 0.0,
                "by_level": level_stats
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des statistiques : {e}")
            return {}
    
    def add_custom_subject(self, subject_data: Dict) -> bool:
        """Ajoute une matière personnalisée"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO guinean_subjects 
                (code, name, description, coefficient, education_level, grade, series, is_optional, is_core)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                subject_data.get('code', ''),
                subject_data.get('name', ''),
                subject_data.get('description', ''),
                subject_data.get('coefficient', 1.0),
                subject_data.get('education_level', ''),
                subject_data.get('grade', ''),
                subject_data.get('series', ''),
                subject_data.get('is_optional', False),
                subject_data.get('is_core', True)
            ))
            
            conn.commit()
            conn.close()
            print(f"✅ Matière personnalisée '{subject_data.get('name')}' ajoutée avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ajout de la matière personnalisée : {e}")
            return False
    
    def update_subject(self, subject_id: int, subject_data: Dict) -> bool:
        """Met à jour une matière existante"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE guinean_subjects 
                SET name = ?, description = ?, coefficient = ?, 
                    is_optional = ?, is_core = ?, date_updated = GETDATE()
                WHERE id = ?
            """, (
                subject_data.get('name', ''),
                subject_data.get('description', ''),
                subject_data.get('coefficient', 1.0),
                subject_data.get('is_optional', False),
                subject_data.get('is_core', True),
                subject_id
            ))
            
            conn.commit()
            conn.close()
            print(f"✅ Matière #{subject_id} mise à jour avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la mise à jour de la matière : {e}")
            return False
    
    def deactivate_subject(self, subject_id: int) -> bool:
        """Désactive une matière (suppression logique)"""
        try:
            conn = self._connect()
            if not conn:
                return False
            
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE guinean_subjects 
                SET is_active = 0, date_updated = GETDATE()
                WHERE id = ?
            """, (subject_id,))
            
            conn.commit()
            conn.close()
            print(f"✅ Matière #{subject_id} désactivée avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la désactivation de la matière : {e}")
            return False

# Instance globale pour l'utilisation dans l'application
guinean_subject_model = GuineanSubjectModel()

def get_guinean_subject_model() -> GuineanSubjectModel:
    """Retourne l'instance globale du modèle de matières guinéennes"""
    return guinean_subject_model
