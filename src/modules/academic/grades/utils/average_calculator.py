#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module centralisé pour les calculs de moyennes cohérents
Utilisé par les vues notes et bulletins pour assurer la cohérence
"""

import sys
import os
from typing import List, Dict, Any, Tuple

# Ajouter le chemin racine
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if root_path not in sys.path:
    sys.path.append(root_path)

def calculate_student_average_consistent(student_id: int) -> Tuple[float, Dict[str, Any]]:
    """
    Calcule la moyenne générale d'un élève de manière cohérente
    Utilise la même logique que les bulletins : moyennes par matière puis moyenne générale
    
    Returns:
        Tuple[moyenne_generale, details_calcul]
    """
    try:
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            return 0.0, {"error": "Pas de connexion à la base"}
        
        cursor = conn.cursor()
        
        # Calculer la moyenne par matière avec les vrais coefficients
        cursor.execute("""
            SELECT 
                n.id_matiere,
                m.nom_matiere,
                m.coefficient as matiere_coefficient,
                SUM(n.note * n.coefficient) / SUM(n.coefficient) as moyenne_ponderee,
                SUM(n.coefficient) as total_coefficients_notes,
                COUNT(n.id_note) as nombre_notes
            FROM notes n
            LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
            WHERE n.id_eleve = ? AND n.note > 0
            GROUP BY n.id_matiere, m.nom_matiere, m.coefficient
            ORDER BY m.nom_matiere
        """, (student_id,))
        
        matieres_calcul = cursor.fetchall()
        
        total_points = 0
        total_coefficients = 0
        matieres_details = []
        
        for matiere in matieres_calcul:
            matiere_id = matiere[0]
            nom_matiere = matiere[1]
            coef_matiere = float(matiere[2]) if matiere[2] else 1.0
            moyenne_ponderee = float(matiere[3]) if matiere[3] else 0
            total_coef_notes = float(matiere[4]) if matiere[4] else 0
            nombre_notes = int(matiere[5]) if matiere[5] else 0
            
            if moyenne_ponderee > 0:
                points = moyenne_ponderee * coef_matiere
                total_points += points
                total_coefficients += coef_matiere
            
            matieres_details.append({
                'id_matiere': matiere_id,
                'nom_matiere': nom_matiere,
                'coefficient': coef_matiere,
                'moyenne_matiere': moyenne_ponderee,
                'nombre_notes': nombre_notes,
                'points': points if moyenne_ponderee > 0 else 0
            })
        
        moyenne_generale = round(total_points / total_coefficients, 2) if total_coefficients > 0 else 0
        
        conn.close()
        
        return moyenne_generale, {
            'total_points': total_points,
            'total_coefficients': total_coefficients,
            'matieres': matieres_details,
            'nombre_matieres': len(matieres_details)
        }
        
    except Exception as e:
        print(f"❌ Erreur calcul moyenne cohérente: {e}")
        return 0.0, {"error": str(e)}

def calculate_student_notes_stats(student_id: int) -> Dict[str, Any]:
    """
    Calcule les statistiques des notes d'un élève (meilleure, pire, nombre)
    Compatible avec la vue des notes
    
    Returns:
        Dict avec meilleure_note, pire_note, nombre_notes, moyenne_generale
    """
    try:
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            return {"meilleure_note": 0, "pire_note": 0, "nombre_notes": 0, "moyenne_generale": 0}
        
        cursor = conn.cursor()
        
        # Récupérer toutes les notes de l'élève
        cursor.execute("""
            SELECT 
                n.note,
                n.coefficient
            FROM notes n
            WHERE n.id_eleve = ? AND n.note > 0
            ORDER BY n.note DESC
        """, (student_id,))
        
        notes = cursor.fetchall()
        
        if not notes:
            conn.close()
            return {"meilleure_note": 0, "pire_note": 0, "nombre_notes": 0, "moyenne_generale": 0}
        
        # Calculer les statistiques
        meilleure_note = float(notes[0][0]) if notes else 0
        pire_note = float(notes[-1][0]) if notes else 0
        nombre_notes = len(notes)
        
        # Calculer la moyenne générale cohérente
        moyenne_generale, _ = calculate_student_average_consistent(student_id)
        
        conn.close()
        
        return {
            "meilleure_note": meilleure_note,
            "pire_note": pire_note,
            "nombre_notes": nombre_notes,
            "moyenne_generale": moyenne_generale
        }
        
    except Exception as e:
        print(f"❌ Erreur calcul stats notes: {e}")
        return {"meilleure_note": 0, "pire_note": 0, "nombre_notes": 0, "moyenne_generale": 0}

def get_student_subjects_with_averages(student_id: int) -> List[Dict[str, Any]]:
    """
    Récupère les matières d'un élève avec leurs moyennes calculées de manière cohérente
    Compatible avec les bulletins
    
    Returns:
        List des matières avec leurs moyennes et coefficients
    """
    try:
        _, details = calculate_student_average_consistent(student_id)
        
        if "error" in details:
            return []
        
        return details.get("matieres", [])
        
    except Exception as e:
        print(f"❌ Erreur récupération matières: {e}")
        return []










