#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contrôleur de gestion des salaires des professeurs
==================================================

Gestion complète des salaires, heures de cours et calculs de paie.
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

class SalaryController:
    """Contrôleur pour la gestion des salaires des professeurs"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            self.db_path = os.path.join(os.getcwd(), "database", "edumanager.db")
        else:
            self.db_path = db_path
    
    def get_connection(self):
        """Obtient une connexion à la base de données"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"❌ Erreur de connexion à la base de données: {e}")
            return None
    
    def calculate_salary(self, prof_id: int, mois: int, annee: int) -> Dict:
        """
        Calcule le salaire d'un professeur pour un mois donné
        
        Args:
            prof_id: ID du professeur
            mois: Mois (1-12)
            annee: Année
            
        Returns:
            Dict contenant le détail du calcul de salaire
        """
        conn = self.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Récupérer les informations du professeur
            cursor.execute("""
                SELECT salaire_horaire, heures_mensuelles, salaire_base, 
                       prime_performance, prime_anciennete, cotisations_sociales
                FROM professeurs 
                WHERE id_professeur = ?
            """, (prof_id,))
            
            prof_data = cursor.fetchone()
            if not prof_data:
                return {}
            
            # Récupérer les heures réelles travaillées ce mois
            cursor.execute("""
                SELECT COALESCE(SUM(nombre_heures), 0) as heures_travaillees
                FROM heures_cours 
                WHERE id_professeur = ? 
                AND strftime('%m', date_cours) = ? 
                AND strftime('%Y', date_cours) = ?
                AND statut = 'realise'
            """, (prof_id, f"{mois:02d}", str(annee)))
            
            heures_data = cursor.fetchone()
            heures_travaillees = heures_data['heures_travaillees'] if heures_data else 0
            
            # Calculs du salaire
            salaire_horaire = prof_data['salaire_horaire'] or 0
            salaire_base = prof_data['salaire_base'] or 0
            prime_performance = prof_data['prime_performance'] or 0
            prime_anciennete = prof_data['prime_anciennete'] or 0
            cotisations_sociales = prof_data['cotisations_sociales'] or 0
            
            # Salaire basé sur les heures
            salaire_heures = heures_travaillees * salaire_horaire
            
            # Salaire brut total
            salaire_brut = salaire_base + salaire_heures + prime_performance + prime_anciennete
            
            # Salaire net
            salaire_net = salaire_brut - cotisations_sociales
            
            return {
                'prof_id': prof_id,
                'mois': mois,
                'annee': annee,
                'heures_travaillees': heures_travaillees,
                'salaire_horaire': salaire_horaire,
                'salaire_base': salaire_base,
                'salaire_heures': salaire_heures,
                'prime_performance': prime_performance,
                'prime_anciennete': prime_anciennete,
                'salaire_brut': salaire_brut,
                'cotisations_sociales': cotisations_sociales,
                'salaire_net': salaire_net
            }
            
        except Exception as e:
            print(f"❌ Erreur calcul salaire: {e}")
            return {}
        finally:
            conn.close()
    
    def save_salary_record(self, salary_data: Dict) -> bool:
        """
        Sauvegarde un enregistrement de salaire dans l'historique
        
        Args:
            salary_data: Dictionnaire contenant les données du salaire
            
        Returns:
            bool: True si sauvegardé avec succès
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Vérifier si un enregistrement existe déjà pour ce mois/année
            cursor.execute("""
                SELECT id FROM historique_salaires 
                WHERE id_professeur = ? AND mois = ? AND annee = ?
            """, (salary_data['prof_id'], salary_data['mois'], salary_data['annee']))
            
            existing = cursor.fetchone()
            
            if existing:
                # Mettre à jour l'enregistrement existant
                cursor.execute("""
                    UPDATE historique_salaires SET
                        heures_travaillees = ?,
                        salaire_horaire = ?,
                        salaire_brut = ?,
                        prime_performance = ?,
                        prime_anciennete = ?,
                        cotisations_sociales = ?,
                        salaire_net = ?,
                        date_modification = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (
                    salary_data['heures_travaillees'],
                    salary_data['salaire_horaire'],
                    salary_data['salaire_brut'],
                    salary_data['prime_performance'],
                    salary_data['prime_anciennete'],
                    salary_data['cotisations_sociales'],
                    salary_data['salaire_net'],
                    existing['id']
                ))
            else:
                # Créer un nouvel enregistrement
                cursor.execute("""
                    INSERT INTO historique_salaires (
                        id_professeur, mois, annee, heures_travaillees,
                        salaire_horaire, salaire_brut, prime_performance,
                        prime_anciennete, cotisations_sociales, salaire_net
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    salary_data['prof_id'],
                    salary_data['mois'],
                    salary_data['annee'],
                    salary_data['heures_travaillees'],
                    salary_data['salaire_horaire'],
                    salary_data['salaire_brut'],
                    salary_data['prime_performance'],
                    salary_data['prime_anciennete'],
                    salary_data['cotisations_sociales'],
                    salary_data['salaire_net']
                ))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erreur sauvegarde salaire: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def add_course_hours(self, prof_id: int, date_cours: str, heure_debut: str, 
                        heure_fin: str, nombre_heures: float, id_classe: int = None, 
                        id_matiere: int = None, notes: str = "") -> bool:
        """
        Ajoute des heures de cours pour un professeur
        
        Args:
            prof_id: ID du professeur
            date_cours: Date du cours (YYYY-MM-DD)
            heure_debut: Heure de début (HH:MM)
            heure_fin: Heure de fin (HH:MM)
            nombre_heures: Nombre d'heures
            id_classe: ID de la classe (optionnel)
            id_matiere: ID de la matière (optionnel)
            notes: Notes additionnelles
            
        Returns:
            bool: True si ajouté avec succès
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO heures_cours (
                    id_professeur, id_classe, id_matiere, date_cours,
                    heure_debut, heure_fin, nombre_heures, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (prof_id, id_classe, id_matiere, date_cours, 
                  heure_debut, heure_fin, nombre_heures, notes))
            
            conn.commit()
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout heures cours: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def get_professor_hours(self, prof_id: int, mois: int = None, annee: int = None) -> List[Dict]:
        """
        Récupère les heures de cours d'un professeur
        
        Args:
            prof_id: ID du professeur
            mois: Mois (optionnel)
            annee: Année (optionnel)
            
        Returns:
            List[Dict]: Liste des heures de cours
        """
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT hc.*, p.nom, p.prenom
                FROM heures_cours hc
                JOIN professeurs p ON hc.id_professeur = p.id_professeur
                WHERE hc.id_professeur = ?
            """
            params = [prof_id]
            
            if mois and annee:
                query += " AND strftime('%m', hc.date_cours) = ? AND strftime('%Y', hc.date_cours) = ?"
                params.extend([f"{mois:02d}", str(annee)])
            
            query += " ORDER BY hc.date_cours DESC, hc.heure_debut"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ Erreur récupération heures: {e}")
            return []
        finally:
            conn.close()
    
    def get_salary_history(self, prof_id: int = None, mois: int = None, annee: int = None) -> List[Dict]:
        """
        Récupère l'historique des salaires
        
        Args:
            prof_id: ID du professeur (optionnel)
            mois: Mois (optionnel)
            annee: Année (optionnel)
            
        Returns:
            List[Dict]: Liste des enregistrements de salaire
        """
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            
            query = """
                SELECT hs.*, p.nom, p.prenom, p.matricule
                FROM historique_salaires hs
                JOIN professeurs p ON hs.id_professeur = p.id_professeur
                WHERE 1=1
            """
            params = []
            
            if prof_id:
                query += " AND hs.id_professeur = ?"
                params.append(prof_id)
            
            if mois:
                query += " AND hs.mois = ?"
                params.append(mois)
            
            if annee:
                query += " AND hs.annee = ?"
                params.append(annee)
            
            query += " ORDER BY hs.annee DESC, hs.mois DESC"
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            print(f"❌ Erreur récupération historique salaires: {e}")
            return []
        finally:
            conn.close()
    
    def get_salary_statistics(self, annee: int = None) -> Dict:
        """
        Récupère les statistiques des salaires
        
        Args:
            annee: Année (optionnel, défaut: année actuelle)
            
        Returns:
            Dict: Statistiques des salaires
        """
        if annee is None:
            annee = datetime.now().year
        
        conn = self.get_connection()
        if not conn:
            return {}
        
        try:
            cursor = conn.cursor()
            
            # Statistiques générales
            cursor.execute("""
                SELECT 
                    COUNT(*) as nombre_professeurs,
                    SUM(salaire_brut) as total_salaires_bruts,
                    SUM(salaire_net) as total_salaires_nets,
                    SUM(cotisations_sociales) as total_cotisations,
                    AVG(salaire_brut) as salaire_moyen_brut,
                    AVG(salaire_net) as salaire_moyen_net
                FROM historique_salaires hs
                WHERE hs.annee = ?
            """, (annee,))
            
            stats = dict(cursor.fetchone())
            
            # Top 5 des professeurs les mieux payés
            cursor.execute("""
                SELECT p.nom, p.prenom, AVG(hs.salaire_net) as salaire_moyen
                FROM historique_salaires hs
                JOIN professeurs p ON hs.id_professeur = p.id_professeur
                WHERE hs.annee = ?
                GROUP BY hs.id_professeur, p.nom, p.prenom
                ORDER BY salaire_moyen DESC
                LIMIT 5
            """, (annee,))
            
            stats['top_professeurs'] = [dict(row) for row in cursor.fetchall()]
            
            return stats
            
        except Exception as e:
            print(f"❌ Erreur récupération statistiques: {e}")
            return {}
        finally:
            conn.close()
    
    def update_professor_salary_info(self, prof_id: int, salary_info: Dict) -> bool:
        """
        Met à jour les informations de salaire d'un professeur
        
        Args:
            prof_id: ID du professeur
            salary_info: Dictionnaire contenant les nouvelles informations
            
        Returns:
            bool: True si mis à jour avec succès
        """
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Construire la requête de mise à jour dynamiquement
            fields = []
            values = []
            
            for key, value in salary_info.items():
                if key in ['salaire_horaire', 'heures_mensuelles', 'salaire_base', 
                          'prime_performance', 'prime_anciennete', 'cotisations_sociales',
                          'compte_bancaire', 'numero_cnss', 'numero_impot']:
                    fields.append(f"{key} = ?")
                    values.append(value)
            
            if fields:
                values.append(prof_id)
                query = f"UPDATE professeurs SET {', '.join(fields)}, date_modification = CURRENT_TIMESTAMP WHERE id_professeur = ?"
                
                cursor.execute(query, values)
                conn.commit()
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erreur mise à jour salaire: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

# Fonctions utilitaires pour faciliter l'utilisation
def calculate_monthly_salary(prof_id: int, mois: int, annee: int) -> Dict:
    """Calcule le salaire mensuel d'un professeur"""
    controller = SalaryController()
    return controller.calculate_salary(prof_id, mois, annee)

def save_monthly_salary(prof_id: int, mois: int, annee: int) -> bool:
    """Calcule et sauvegarde le salaire mensuel d'un professeur"""
    controller = SalaryController()
    salary_data = controller.calculate_salary(prof_id, mois, annee)
    if salary_data:
        return controller.save_salary_record(salary_data)
    return False

def get_all_professors_salary_summary(mois: int, annee: int) -> List[Dict]:
    """Récupère le résumé des salaires de tous les professeurs pour un mois donné"""
    controller = SalaryController()
    return controller.get_salary_history(mois=mois, annee=annee)
