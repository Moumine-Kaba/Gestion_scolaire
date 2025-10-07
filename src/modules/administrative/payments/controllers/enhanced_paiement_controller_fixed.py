# -*- coding: utf-8 -*-
"""
Contrôleur Amélioré pour le Module Paiements - VERSION CORRIGÉE
EduManager+ - Gestion Complète des Paiements Scolaires

Ce contrôleur étend les fonctionnalités de base avec :
- Gestion des types de frais
- Échéancier automatique
- Système de remises et bourses
- Relances automatiques
- Rapports financiers avancés

VERSION CORRIGÉE avec les bons noms de colonnes de la base de données
"""

from database.connection import get_db_connection
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

class EnhancedPaiementController:
    """Contrôleur amélioré pour la gestion des paiements"""
    
    def __init__(self):
        self.current_academic_year = self._get_current_academic_year()
    
    def _get_current_academic_year(self) -> str:
        """Retourne l'année scolaire actuelle"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # En Guinée, l'année scolaire commence en octobre
        if current_month >= 10:
            return f"{current_year}-{current_year + 1}"
        else:
            return f"{current_year - 1}-{current_year}"
    
    # ========== GESTION DES TYPES DE FRAIS ==========
    
    def get_all_types_frais(self) -> List[Dict]:
        """Récupère tous les types de frais"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT id_type_frais, nom, description, montant_standard, 
                       periodicite, niveau_educatif, est_obligatoire, est_actif,
                       date_creation, date_modification
                FROM types_frais 
                ORDER BY nom
            """)
            
            types_frais = []
            for row in cur.fetchall():
                types_frais.append({
                    'id': row[0],
                    'nom': row[1],
                    'description': row[2],
                    'montant_standard': float(row[3]),
                    'periodicite': row[4],
                    'niveau_educatif': row[5],
                    'est_obligatoire': bool(row[6]),
                    'est_actif': bool(row[7]),
                    'date_creation': row[8],
                    'date_modification': row[9]
                })
            
            conn.close()
            return types_frais
            
        except Exception as e:
            print(f"❌ Erreur récupération types de frais: {e}")
            return []
    
    def add_type_frais(self, nom: str, description: str, montant_standard: float, 
                      periodicite: str, niveau_educatif: str = "tous", 
                      est_obligatoire: bool = True) -> bool:
        """Ajoute un nouveau type de frais"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                INSERT INTO types_frais (nom, description, montant_standard, periodicite, 
                                       niveau_educatif, est_obligatoire)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, description, montant_standard, periodicite, niveau_educatif, est_obligatoire))
            
            conn.commit()
            conn.close()
            print(f"✅ Type de frais '{nom}' ajouté avec succès")
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout type de frais: {e}")
            return False
    
    def update_type_frais(self, type_frais_id: int, **kwargs) -> bool:
        """Met à jour un type de frais"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Construire la requête dynamiquement
            set_clauses = []
            values = []
            
            for key, value in kwargs.items():
                if key in ['nom', 'description', 'montant_standard', 'periodicite', 'niveau_educatif', 'est_obligatoire', 'est_actif']:
                    set_clauses.append(f"{key} = ?")
                    values.append(value)
            
            if set_clauses:
                set_clauses.append("date_modification = GETDATE()")
                values.append(type_frais_id)
                
                query = f"UPDATE types_frais SET {', '.join(set_clauses)} WHERE id_type_frais = ?"
                cur.execute(query, values)
                
                conn.commit()
                conn.close()
                print(f"✅ Type de frais {type_frais_id} mis à jour")
                return True
            
            return False
            
        except Exception as e:
            print(f"❌ Erreur mise à jour type de frais: {e}")
            return False
    
    # ========== GESTION DE L'ÉCHÉANCIER ==========
    
    def get_echeancier_eleve(self, eleve_id: int, annee_scolaire: str = None) -> List[Dict]:
        """Récupère l'échéancier d'un élève"""
        if not annee_scolaire:
            annee_scolaire = self.current_academic_year
            
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT e.id_echeance, e.id_eleve, e.id_type_frais, e.annee_scolaire, 
                       e.trimestre, e.montant, e.montant_remise, e.montant_final,
                       e.date_echeance, e.date_paiement, e.statut, e.mode_paiement,
                       e.reference_paiement, e.penalites, e.nb_relances,
                       e.derniere_relance, e.commentaires,
                       tf.nom as type_frais_nom, tf.periodicite,
                       el.nom as eleve_nom, el.prenom as eleve_prenom
                FROM echeancier e
                JOIN types_frais tf ON e.id_type_frais = tf.id_type_frais
                JOIN eleves el ON e.id_eleve = el.id_eleve
                WHERE e.id_eleve = ? AND e.annee_scolaire = ?
                ORDER BY e.date_echeance ASC
            """, (eleve_id, annee_scolaire))
            
            echeances = []
            for row in cur.fetchall():
                echeances.append({
                    'id_echeance': row[0],
                    'id_eleve': row[1],
                    'id_type_frais': row[2],
                    'annee_scolaire': row[3],
                    'trimestre': row[4],
                    'montant': float(row[5]),
                    'montant_remise': float(row[6]) if row[6] else 0,
                    'montant_final': float(row[7]),
                    'date_echeance': row[8],
                    'date_paiement': row[9],
                    'statut': row[10],
                    'mode_paiement': row[11],
                    'reference_paiement': row[12],
                    'penalites': float(row[13]) if row[13] else 0,
                    'nb_relances': row[14],
                    'derniere_relance': row[15],
                    'commentaires': row[16],
                    'type_frais_nom': row[17],
                    'periodicite': row[18],
                    'eleve_nom': row[19],
                    'eleve_prenom': row[20]
                })
            
            conn.close()
            return echeances
            
        except Exception as e:
            print(f"❌ Erreur récupération échéancier: {e}")
            return []
    
    def get_echeances_en_retard(self) -> List[Dict]:
        """Récupère toutes les échéances en retard"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            today = datetime.now().date()
            cur.execute("""
                SELECT e.id_echeance, e.id_eleve, e.date_echeance, e.montant_final,
                       e.penalites, e.nb_relances, e.derniere_relance,
                       tf.nom as type_frais_nom,
                       el.nom as eleve_nom, el.prenom as eleve_prenom,
                       c.nom_classe as classe_nom
                FROM echeancier e
                JOIN types_frais tf ON e.id_type_frais = tf.id_type_frais
                JOIN eleves el ON e.id_eleve = el.id_eleve
                JOIN classes c ON el.id_classe = c.id_classe
                WHERE e.date_echeance < ? AND e.statut = 'en_attente'
                ORDER BY e.date_echeance ASC
            """, (today,))
            
            echeances_retard = []
            for row in cur.fetchall():
                jours_retard = (today - row[2]).days
                echeances_retard.append({
                    'id_echeance': row[0],
                    'id_eleve': row[1],
                    'date_echeance': row[2],
                    'jours_retard': jours_retard,
                    'montant_final': float(row[3]),
                    'penalites': float(row[4]) if row[4] else 0,
                    'nb_relances': row[5],
                    'derniere_relance': row[6],
                    'type_frais_nom': row[7],
                    'eleve_nom': row[8],
                    'eleve_prenom': row[9],
                    'classe_nom': row[10]
                })
            
            conn.close()
            return echeances_retard
            
        except Exception as e:
            print(f"❌ Erreur récupération échéances en retard: {e}")
            return []
    
    def generer_echeancier_eleve(self, eleve_id: int, annee_scolaire: str = None) -> bool:
        """Génère l'échéancier pour un élève"""
        if not annee_scolaire:
            annee_scolaire = self.current_academic_year
            
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Vérifier si l'échéancier existe déjà
            cur.execute("""
                SELECT COUNT(*) FROM echeancier 
                WHERE id_eleve = ? AND annee_scolaire = ?
            """, (eleve_id, annee_scolaire))
            
            if cur.fetchone()[0] > 0:
                print(f"⚠️ Échéancier déjà existant pour l'élève {eleve_id}")
                conn.close()
                return False
            
            # Récupérer les informations de l'élève
            cur.execute("""
                SELECT id_eleve, nom, prenom, id_classe
                FROM eleves 
                WHERE id_eleve = ?
            """, (eleve_id,))
            eleve = cur.fetchone()
            
            if not eleve:
                print(f"❌ Élève {eleve_id} non trouvé")
                conn.close()
                return False
            
            # Récupérer le niveau de la classe
            cur.execute("""
                SELECT niveau FROM classes WHERE id_classe = ?
            """, (eleve[3],))
            classe_info = cur.fetchone()
            niveau_eleve = classe_info[0] if classe_info else "tous"
            
            # Récupérer les types de frais applicables
            cur.execute("""
                SELECT id_type_frais, nom, montant_standard, periodicite, niveau_educatif
                FROM types_frais 
                WHERE est_actif = 1 AND (niveau_educatif = 'tous' OR niveau_educatif LIKE ?)
            """, (f"%{niveau_eleve}%",))
            
            types_frais = cur.fetchall()
            echeances_created = 0
            
            for tf_id, nom, montant, periodicite, niveau in types_frais:
                if periodicite == "annuel":
                    date_echeance = f"{annee_scolaire.split('-')[0]}-10-01"
                    cur.execute("""
                        INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, 
                                              montant, montant_final, date_echeance)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (eleve_id, tf_id, annee_scolaire, montant, montant, date_echeance))
                    echeances_created += 1
                    
                elif periodicite == "trimestriel":
                    dates_trimestres = [
                        f"{annee_scolaire.split('-')[0]}-10-01",  # 1er trimestre
                        f"{annee_scolaire.split('-')[0]}-12-15",  # 2ème trimestre
                        f"{annee_scolaire.split('-')[1]}-03-01"   # 3ème trimestre
                    ]
                    
                    for i, date_echeance in enumerate(dates_trimestres, 1):
                        cur.execute("""
                            INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, 
                                                  trimestre, montant, montant_final, date_echeance)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (eleve_id, tf_id, annee_scolaire, i, montant, montant, date_echeance))
                        echeances_created += 1
                        
                elif periodicite == "mensuel":
                    # Octobre à Décembre
                    for mois in range(10, 13):
                        date_echeance = f"{annee_scolaire.split('-')[0]}-{mois:02d}-01"
                        cur.execute("""
                            INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, 
                                                  montant, montant_final, date_echeance)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (eleve_id, tf_id, annee_scolaire, montant, montant, date_echeance))
                        echeances_created += 1
                    
                    # Janvier à Juin
                    for mois in range(1, 7):
                        date_echeance = f"{annee_scolaire.split('-')[1]}-{mois:02d}-01"
                        cur.execute("""
                            INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, 
                                                  montant, montant_final, date_echeance)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (eleve_id, tf_id, annee_scolaire, montant, montant, date_echeance))
                        echeances_created += 1
            
            conn.commit()
            conn.close()
            print(f"✅ {echeances_created} échéances générées pour l'élève {eleve_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur génération échéancier: {e}")
            return False
    
    def enregistrer_paiement_echeance(self, echeance_id: int, mode_paiement: str, 
                                    reference_paiement: str = None) -> bool:
        """Enregistre un paiement pour une échéance"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Générer une référence si non fournie
            if not reference_paiement:
                reference_paiement = f"PAY{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            today = datetime.now().date()
            
            cur.execute("""
                UPDATE echeancier 
                SET date_paiement = ?, statut = 'paye', mode_paiement = ?, 
                    reference_paiement = ?, date_modification = GETDATE()
                WHERE id_echeance = ?
            """, (today, mode_paiement, reference_paiement, echeance_id))
            
            # Créer aussi un enregistrement dans la table paiements pour compatibilité
            cur.execute("""
                SELECT id_eleve, montant_final FROM echeancier WHERE id_echeance = ?
            """, (echeance_id,))
            echeance_info = cur.fetchone()
            
            if echeance_info:
                cur.execute("""
                    INSERT INTO paiements (id_eleve, montant, date_paiement, mode_paiement, 
                                         statut, reference)
                    VALUES (?, ?, ?, ?, 'validé', ?)
                """, (echeance_info[0], echeance_info[1], today, mode_paiement, reference_paiement))
            
            conn.commit()
            conn.close()
            print(f"✅ Paiement enregistré pour l'échéance {echeance_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur enregistrement paiement: {e}")
            return False
    
    # ========== GESTION DES REMISES ==========
    
    def get_remises_eleve(self, eleve_id: int) -> List[Dict]:
        """Récupère les remises d'un élève"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT r.id_remise, r.id_eleve, r.id_type_frais, r.type_remise,
                       r.pourcentage, r.montant_fixe, r.montant_maximum,
                       r.date_debut, r.date_fin, r.statut, r.motif,
                       r.justificatifs, r.approbateur, r.date_approbation,
                       r.commentaires,
                       tf.nom as type_frais_nom,
                       el.nom as eleve_nom, el.prenom as eleve_prenom
                FROM remises r
                LEFT JOIN types_frais tf ON r.id_type_frais = tf.id_type_frais
                JOIN eleves el ON r.id_eleve = el.id_eleve
                WHERE r.id_eleve = ?
                ORDER BY r.date_debut DESC
            """, (eleve_id,))
            
            remises = []
            for row in cur.fetchall():
                remises.append({
                    'id_remise': row[0],
                    'id_eleve': row[1],
                    'id_type_frais': row[2],
                    'type_remise': row[3],
                    'pourcentage': float(row[4]) if row[4] else None,
                    'montant_fixe': float(row[5]) if row[5] else None,
                    'montant_maximum': float(row[6]) if row[6] else None,
                    'date_debut': row[7],
                    'date_fin': row[8],
                    'statut': row[9],
                    'motif': row[10],
                    'justificatifs': row[11],
                    'approbateur': row[12],
                    'date_approbation': row[13],
                    'commentaires': row[14],
                    'type_frais_nom': row[15],
                    'eleve_nom': row[16],
                    'eleve_prenom': row[17]
                })
            
            conn.close()
            return remises
            
        except Exception as e:
            print(f"❌ Erreur récupération remises: {e}")
            return []
    
    def ajouter_remise(self, eleve_id: int, type_remise: str, motif: str,
                      pourcentage: float = None, montant_fixe: float = None,
                      montant_maximum: float = None, date_debut: str = None,
                      date_fin: str = None, type_frais_id: int = None,
                      justificatifs: str = None, approbateur: str = None) -> bool:
        """Ajoute une nouvelle remise"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            if not date_debut:
                date_debut = datetime.now().date()
            
            cur.execute("""
                INSERT INTO remises (id_eleve, id_type_frais, type_remise, pourcentage,
                                   montant_fixe, montant_maximum, date_debut, date_fin,
                                   motif, justificatifs, approbateur)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (eleve_id, type_frais_id, type_remise, pourcentage, montant_fixe,
                  montant_maximum, date_debut, date_fin, motif, justificatifs, approbateur))
            
            conn.commit()
            conn.close()
            print(f"✅ Remise ajoutée pour l'élève {eleve_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur ajout remise: {e}")
            return False
    
    # ========== RAPPORTS FINANCIERS ==========
    
    def get_statistiques_paiements(self, annee_scolaire: str = None) -> Dict:
        """Récupère les statistiques des paiements"""
        if not annee_scolaire:
            annee_scolaire = self.current_academic_year
            
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Statistiques générales
            cur.execute("""
                SELECT 
                    COUNT(*) as total_echeances,
                    SUM(CASE WHEN statut = 'paye' THEN 1 ELSE 0 END) as payees,
                    SUM(CASE WHEN statut = 'en_attente' THEN 1 ELSE 0 END) as en_attente,
                    SUM(CASE WHEN statut = 'en_retard' THEN 1 ELSE 0 END) as en_retard,
                    SUM(CASE WHEN statut = 'paye' THEN montant_final ELSE 0 END) as montant_recouvre,
                    SUM(montant_final) as montant_total,
                    SUM(penalites) as total_penalites
                FROM echeancier 
                WHERE annee_scolaire = ?
            """, (annee_scolaire,))
            
            stats = cur.fetchone()
            
            # Statistiques par type de frais
            cur.execute("""
                SELECT tf.nom, 
                       COUNT(*) as nb_echeances,
                       SUM(CASE WHEN e.statut = 'paye' THEN 1 ELSE 0 END) as payees,
                       SUM(CASE WHEN e.statut = 'paye' THEN e.montant_final ELSE 0 END) as montant_recouvre,
                       SUM(e.montant_final) as montant_total
                FROM echeancier e
                JOIN types_frais tf ON e.id_type_frais = tf.id_type_frais
                WHERE e.annee_scolaire = ?
                GROUP BY tf.id_type_frais, tf.nom
                ORDER BY montant_total DESC
            """, (annee_scolaire,))
            
            stats_par_type = []
            for row in cur.fetchall():
                stats_par_type.append({
                    'type_frais': row[0],
                    'nb_echeances': row[1],
                    'payees': row[2],
                    'montant_recouvre': float(row[3]),
                    'montant_total': float(row[4])
                })
            
            # Statistiques par classe - CORRIGÉ avec les bons noms de colonnes
            cur.execute("""
                SELECT c.nom_classe as classe_nom, 
                       COUNT(*) as nb_eleves,
                       SUM(CASE WHEN e.statut = 'paye' THEN e.montant_final ELSE 0 END) as montant_recouvre,
                       SUM(e.montant_final) as montant_total
                FROM echeancier e
                JOIN eleves el ON e.id_eleve = el.id_eleve
                JOIN classes c ON el.id_classe = c.id_classe
                WHERE e.annee_scolaire = ?
                GROUP BY c.id_classe, c.nom_classe
                ORDER BY montant_recouvre DESC
            """, (annee_scolaire,))
            
            stats_par_classe = []
            for row in cur.fetchall():
                stats_par_classe.append({
                    'classe_nom': row[0],
                    'nb_eleves': row[1],
                    'montant_recouvre': float(row[2]),
                    'montant_total': float(row[3])
                })
            
            conn.close()
            
            return {
                'annee_scolaire': annee_scolaire,
                'total_echeances': stats[0],
                'payees': stats[1],
                'en_attente': stats[2],
                'en_retard': stats[3],
                'montant_recouvre': float(stats[4]) if stats[4] else 0,
                'montant_total': float(stats[5]) if stats[5] else 0,
                'total_penalites': float(stats[6]) if stats[6] else 0,
                'taux_recouvrement': (float(stats[4]) / float(stats[5]) * 100) if stats[5] and stats[5] > 0 else 0,
                'stats_par_type': stats_par_type,
                'stats_par_classe': stats_par_classe
            }
            
        except Exception as e:
            print(f"❌ Erreur calcul statistiques: {e}")
            return {}
    
    def get_rapport_tresorerie(self, date_debut: str, date_fin: str) -> Dict:
        """Génère un rapport de trésorerie"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Recettes
            cur.execute("""
                SELECT 
                    DATE(date_paiement) as date_paiement,
                    SUM(montant_final + penalites) as montant_total
                FROM echeancier 
                WHERE date_paiement BETWEEN ? AND ? AND statut = 'paye'
                GROUP BY DATE(date_paiement)
                ORDER BY date_paiement
            """, (date_debut, date_fin))
            
            recettes = []
            total_recettes = 0
            for row in cur.fetchall():
                recettes.append({
                    'date': row[0],
                    'montant': float(row[1])
                })
                total_recettes += float(row[1])
            
            # Recettes par mode de paiement
            cur.execute("""
                SELECT mode_paiement, COUNT(*) as nb_paiements, SUM(montant_final + penalites) as montant_total
                FROM echeancier 
                WHERE date_paiement BETWEEN ? AND ? AND statut = 'paye'
                GROUP BY mode_paiement
                ORDER BY montant_total DESC
            """, (date_debut, date_fin))
            
            recettes_par_mode = []
            for row in cur.fetchall():
                recettes_par_mode.append({
                    'mode_paiement': row[0],
                    'nb_paiements': row[1],
                    'montant_total': float(row[2])
                })
            
            conn.close()
            
            return {
                'periode': {'debut': date_debut, 'fin': date_fin},
                'total_recettes': total_recettes,
                'recettes_par_jour': recettes,
                'recettes_par_mode': recettes_par_mode
            }
            
        except Exception as e:
            print(f"❌ Erreur génération rapport trésorerie: {e}")
            return {}
    
    # ========== FONCTIONS UTILITAIRES ==========
    
    def calculer_penalites_retard(self, echeance_id: int) -> float:
        """Calcule les pénalités pour un retard de paiement"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            cur.execute("""
                SELECT date_echeance, montant_final FROM echeancier WHERE id_echeance = ?
            """, (echeance_id,))
            
            result = cur.fetchone()
            if not result:
                return 0
            
            date_echeance, montant = result
            today = datetime.now().date()
            jours_retard = (today - date_echeance).days
            
            if jours_retard <= 0:
                return 0
            
            # Pénalité de 1% par jour de retard, maximum 20% du montant
            penalite_pourcentage = min(jours_retard * 1, 20)  # 1% par jour, max 20%
            penalite_montant = (montant * penalite_pourcentage) / 100
            
            conn.close()
            return penalite_montant
            
        except Exception as e:
            print(f"❌ Erreur calcul pénalités: {e}")
            return 0
    
    def appliquer_penalites_retard(self) -> int:
        """Applique automatiquement les pénalités de retard"""
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Récupérer les échéances en retard non pénalisées
            cur.execute("""
                SELECT id_echeance, date_echeance, montant_final 
                FROM echeancier 
                WHERE date_echeance < CAST(GETDATE() AS DATE) 
                AND statut = 'en_attente' 
                AND penalites = 0
            """)
            
            echeances_retard = cur.fetchall()
            penalites_appliquees = 0
            
            for echeance_id, date_echeance, montant in echeances_retard:
                penalite = self.calculer_penalites_retard(echeance_id)
                if penalite > 0:
                    cur.execute("""
                        UPDATE echeancier 
                        SET penalites = ?, statut = 'en_retard', date_modification = GETDATE()
                        WHERE id_echeance = ?
                    """, (penalite, echeance_id))
                    penalites_appliquees += 1
            
            conn.commit()
            conn.close()
            
            print(f"✅ {penalites_appliquees} pénalités appliquées")
            return penalites_appliquees
            
        except Exception as e:
            print(f"❌ Erreur application pénalités: {e}")
            return 0

# ========== FONCTIONS DE COMPATIBILITÉ ==========

def get_all_paiements_enhanced(eleve_id=None):
    """Version améliorée de get_all_paiements"""
    controller = EnhancedPaiementController()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        if eleve_id:
            cur.execute("""
                SELECT p.id_paiement, p.id_eleve, p.montant, p.date_paiement, 
                       p.mode_paiement, p.description, p.statut, p.reference,
                       el.nom, el.prenom, c.nom_classe as classe_nom
                FROM paiements p
                JOIN eleves el ON p.id_eleve = el.id_eleve
                LEFT JOIN classes c ON el.id_classe = c.id_classe
                WHERE p.id_eleve = ? 
                ORDER BY p.date_paiement DESC
            """, (eleve_id,))
        else:
            cur.execute("""
                SELECT p.id_paiement, p.id_eleve, p.montant, p.date_paiement, 
                       p.mode_paiement, p.description, p.statut, p.reference,
                       el.nom, el.prenom, c.nom_classe as classe_nom
                FROM paiements p
                JOIN eleves el ON p.id_eleve = el.id_eleve
                LEFT JOIN classes c ON el.id_classe = c.id_classe
                ORDER BY p.date_paiement DESC
            """)
        
        rows = cur.fetchall()
        conn.close()
        return rows
        
    except Exception as e:
        print(f"❌ Erreur récupération paiements: {e}")
        return []

# Instance globale du contrôleur
enhanced_controller = EnhancedPaiementController()

if __name__ == "__main__":
    # Test du contrôleur
    controller = EnhancedPaiementController()
    
    # Test des statistiques
    stats = controller.get_statistiques_paiements()
    print("📊 Statistiques:", json.dumps(stats, indent=2, default=str))
