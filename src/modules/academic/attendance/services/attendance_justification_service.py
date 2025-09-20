# Service de gestion des justificatifs d'absence
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path
from ..controllers.attendance_controller import AttendanceController

class AttendanceJustificationService:
    """Service de gestion des justificatifs d'absence"""
    
    def __init__(self):
        self.attendance_controller = AttendanceController()
        self.justifications_folder = "data/justifications"  # Dossier de stockage
        self.allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx']
        self.max_file_size = 10 * 1024 * 1024  # 10MB max
    
    def upload_justification(self, eleve_id: int, classe_id: int, date: str, 
                           file_path: str, justification_type: str = "medical") -> bool:
        """Upload un justificatif d'absence"""
        try:
            # Vérifier le fichier
            if not self._validate_file(file_path):
                return False
            
            # Créer le dossier de destination
            dest_folder = self._create_student_folder(eleve_id)
            
            # Générer le nom du fichier
            file_extension = Path(file_path).suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"justification_{date}_{justification_type}_{timestamp}{file_extension}"
            
            # Copier le fichier
            dest_path = os.path.join(dest_folder, filename)
            shutil.copy2(file_path, dest_path)
            
            # Mettre à jour la base de données
            self._update_attendance_with_justification(eleve_id, classe_id, date, dest_path)
            
            print(f"✅ Justificatif uploadé : {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur upload justificatif: {e}")
            return False
    
    def get_student_justifications(self, eleve_id: int) -> List[Dict]:
        """Récupère tous les justificatifs d'un élève"""
        try:
            justifications = []
            student_folder = self._get_student_folder(eleve_id)
            
            if os.path.exists(student_folder):
                for filename in os.listdir(student_folder):
                    if filename.startswith("justification_"):
                        file_path = os.path.join(student_folder, filename)
                        file_info = self._parse_justification_filename(filename)
                        
                        justifications.append({
                            'filename': filename,
                            'file_path': file_path,
                            'date': file_info['date'],
                            'type': file_info['type'],
                            'upload_date': datetime.fromtimestamp(os.path.getctime(file_path)),
                            'size': os.path.getsize(file_path)
                        })
            
            return sorted(justifications, key=lambda x: x['upload_date'], reverse=True)
            
        except Exception as e:
            print(f"❌ Erreur récupération justificatifs: {e}")
            return []
    
    def validate_justification(self, eleve_id: int, justification_id: str, 
                            validator_id: int, status: str, comment: str = "") -> bool:
        """Valide ou rejette un justificatif"""
        try:
            # Logique de validation
            validation_data = {
                'justification_id': justification_id,
                'eleve_id': eleve_id,
                'validator_id': validator_id,
                'status': status,  # 'approved', 'rejected', 'pending'
                'comment': comment,
                'validation_date': datetime.now()
            }
            
            # Sauvegarder la validation (à implémenter selon la structure DB)
            print(f"✅ Justificatif {status} par validateur {validator_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur validation justificatif: {e}")
            return False
    
    def get_pending_justifications(self) -> List[Dict]:
        """Récupère tous les justificatifs en attente de validation"""
        try:
            pending = []
            
            # Parcourir tous les dossiers d'élèves
            base_folder = Path(self.justifications_folder)
            if base_folder.exists():
                for student_folder in base_folder.iterdir():
                    if student_folder.is_dir():
                        eleve_id = int(student_folder.name)
                        
                        # Récupérer les justificatifs non validés
                        justifications = self.get_student_justifications(eleve_id)
                        for justification in justifications:
                            if not self._is_justification_validated(justification['filename']):
                                justification['eleve_id'] = eleve_id
                                pending.append(justification)
            
            return pending
            
        except Exception as e:
            print(f"❌ Erreur justificatifs en attente: {e}")
            return []
    
    def generate_justification_report(self, start_date: str, end_date: str) -> Dict:
        """Génère un rapport des justificatifs sur une période"""
        try:
            report = {
                'periode': f"{start_date} à {end_date}",
                'total_justifications': 0,
                'approved': 0,
                'rejected': 0,
                'pending': 0,
                'by_type': {},
                'by_student': {}
            }
            
            # Analyser tous les justificatifs
            base_folder = Path(self.justifications_folder)
            if base_folder.exists():
                for student_folder in base_folder.iterdir():
                    if student_folder.is_dir():
                        eleve_id = int(student_folder.name)
                        justifications = self.get_student_justifications(eleve_id)
                        
                        for justification in justifications:
                            if self._is_in_period(justification['date'], start_date, end_date):
                                report['total_justifications'] += 1
                                
                                # Compter par statut
                                status = self._get_justification_status(justification['filename'])
                                report[status] += 1
                                
                                # Compter par type
                                justification_type = justification['type']
                                report['by_type'][justification_type] = report['by_type'].get(justification_type, 0) + 1
                                
                                # Compter par élève
                                student_name = f"Élève {eleve_id}"  # À récupérer depuis la DB
                                report['by_student'][student_name] = report['by_student'].get(student_name, 0) + 1
            
            return report
            
        except Exception as e:
            print(f"❌ Erreur rapport justificatifs: {e}")
            return {}
    
    def _validate_file(self, file_path: str) -> bool:
        """Valide un fichier avant upload"""
        try:
            # Vérifier l'existence
            if not os.path.exists(file_path):
                print("❌ Fichier introuvable")
                return False
            
            # Vérifier l'extension
            file_extension = Path(file_path).suffix.lower()
            if file_extension not in self.allowed_extensions:
                print(f"❌ Extension non autorisée : {file_extension}")
                return False
            
            # Vérifier la taille
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                print(f"❌ Fichier trop volumineux : {file_size} bytes")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur validation fichier: {e}")
            return False
    
    def _create_student_folder(self, eleve_id: int) -> str:
        """Crée le dossier de stockage pour un élève"""
        student_folder = os.path.join(self.justifications_folder, str(eleve_id))
        os.makedirs(student_folder, exist_ok=True)
        return student_folder
    
    def _get_student_folder(self, eleve_id: int) -> str:
        """Récupère le dossier de stockage d'un élève"""
        return os.path.join(self.justifications_folder, str(eleve_id))
    
    def _parse_justification_filename(self, filename: str) -> Dict:
        """Parse le nom de fichier pour extraire les informations"""
        try:
            # Format : justification_YYYY-MM-DD_type_timestamp.ext
            parts = filename.replace('.', '_').split('_')
            if len(parts) >= 4:
                return {
                    'date': f"{parts[1]}-{parts[2]}-{parts[3]}",
                    'type': parts[4] if len(parts) > 4 else 'unknown'
                }
            return {'date': 'unknown', 'type': 'unknown'}
        except:
            return {'date': 'unknown', 'type': 'unknown'}
    
    def _update_attendance_with_justification(self, eleve_id: int, classe_id: int, 
                                            date: str, justification_path: str):
        """Met à jour l'enregistrement de présence avec le chemin du justificatif"""
        try:
            # Mettre à jour le statut et ajouter le chemin du justificatif
            attendance = self.attendance_controller.get_attendance_for_date_and_class(classe_id, date)
            
            if eleve_id in attendance:
                # Mettre à jour l'existant
                self.attendance_controller.update_attendance(
                    eleve_id, classe_id, date, "Justifié", f"Justificatif: {justification_path}"
                )
            else:
                # Créer un nouvel enregistrement
                from ..models.attendance_model import AttendanceModel
                attendance_model = AttendanceModel(
                    eleve_id=eleve_id,
                    classe_id=classe_id,
                    date=date,
                    statut="Justifié",
                    commentaire=f"Justificatif: {justification_path}"
                )
                self.attendance_controller.add_attendance(attendance_model)
                
        except Exception as e:
            print(f"❌ Erreur mise à jour avec justificatif: {e}")
    
    def _is_justification_validated(self, filename: str) -> bool:
        """Vérifie si un justificatif a été validé"""
        # Logique de vérification de validation
        # À implémenter selon la structure de la base de données
        return False
    
    def _get_justification_status(self, filename: str) -> str:
        """Récupère le statut de validation d'un justificatif"""
        # Logique de récupération du statut
        # À implémenter selon la structure de la base de données
        return 'pending'
    
    def _is_in_period(self, date_str: str, start_date: str, end_date: str) -> bool:
        """Vérifie si une date est dans la période donnée"""
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            start_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_obj = datetime.strptime(end_date, "%Y-%m-%d")
            return start_obj <= date_obj <= end_obj
        except:
            return False
