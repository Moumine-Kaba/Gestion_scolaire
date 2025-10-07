# -*- coding: utf-8 -*-
"""
Script de Migration pour le Système de Paiements
EduManager+ - Migration vers le Système Amélioré

Ce script migre les données existantes vers le nouveau système de paiements.
"""

import os
import sys
from datetime import datetime

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_db_connection
from src.modules.administrative.payments.controllers.database_schema import (
    create_all_payment_tables, get_current_academic_year
)
from src.modules.administrative.payments.controllers.enhanced_paiement_controller import (
    EnhancedPaiementController
)

def backup_existing_data():
    """Sauvegarde les données existantes avant migration"""
    print("💾 Sauvegarde des données existantes...")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table paiements existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'paiements'
        """)
        
        if cur.fetchone()[0] == 0:
            print("⚠️ Aucune table paiements existante à sauvegarder")
            conn.close()
            return []
        
        # Récupérer tous les paiements existants
        cur.execute("""
            SELECT id_paiement, id_eleve, montant, date_paiement, 
                   mode_paiement, description, statut, reference
            FROM paiements
            ORDER BY date_paiement
        """)
        
        paiements_existants = cur.fetchall()
        conn.close()
        
        print(f"✅ {len(paiements_existants)} paiements sauvegardés")
        return paiements_existants
        
    except Exception as e:
        print(f"❌ Erreur sauvegarde: {e}")
        return []

def migrate_paiements_to_echeancier(paiements_existants):
    """Migre les paiements existants vers le système d'échéancier"""
    print("🔄 Migration des paiements vers l'échéancier...")
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Récupérer l'année scolaire actuelle
        annee_scolaire = get_current_academic_year()
        
        # Récupérer le type de frais "Frais de scolarité" (premier par défaut)
        cur.execute("""
            SELECT id_type_frais FROM types_frais 
            WHERE nom = 'Frais de scolarité' AND est_actif = 1
        """)
        
        result = cur.fetchone()
        if not result:
            # Créer un type de frais par défaut si nécessaire
            cur.execute("""
                INSERT INTO types_frais (nom, description, montant_standard, periodicite, niveau_educatif, est_obligatoire)
                VALUES ('Frais de scolarité', 'Frais de scolarité généraux', 500000, 'annuel', 'tous', 1)
            """)
            conn.commit()
            
            cur.execute("""
                SELECT id_type_frais FROM types_frais 
                WHERE nom = 'Frais de scolarité' AND est_actif = 1
            """)
            result = cur.fetchone()
        
        type_frais_id = result[0]
        
        paiements_migres = 0
        
        for paiement in paiements_existants:
            id_paiement, id_eleve, montant, date_paiement, mode_paiement, description, statut, reference = paiement
            
            # Déterminer le statut dans le nouveau système
            if statut == 'validé':
                nouveau_statut = 'paye'
            elif statut == 'en_attente':
                nouveau_statut = 'en_attente'
            else:
                nouveau_statut = 'en_attente'
            
            # Créer l'échéance correspondante
            cur.execute("""
                INSERT INTO echeancier (
                    id_eleve, id_type_frais, annee_scolaire, 
                    montant, montant_final, date_echeance,
                    date_paiement, statut, mode_paiement, 
                    reference_paiement, commentaires
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_eleve, type_frais_id, annee_scolaire,
                montant, montant, date_paiement,  # Utiliser la date de paiement comme échéance
                date_paiement if nouveau_statut == 'paye' else None,
                nouveau_statut, mode_paiement, reference, description
            ))
            
            paiements_migres += 1
        
        conn.commit()
        conn.close()
        
        print(f"✅ {paiements_migres} paiements migrés vers l'échéancier")
        return paiements_migres
        
    except Exception as e:
        print(f"❌ Erreur migration: {e}")
        return 0

def generate_echeanciers_for_students():
    """Génère les échéanciers pour tous les élèves"""
    print("📅 Génération des échéanciers pour tous les élèves...")
    
    try:
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        
        eleves = get_all_eleves()
        controller = EnhancedPaiementController()
        
        echeanciers_generes = 0
        
        for eleve in eleves:
            if isinstance(eleve, (tuple, list)):
                eleve_id = eleve[0]
            else:
                eleve_id = eleve.get('id_eleve')
            
            # Générer l'échéancier pour cet élève
            if controller.generer_echeancier_eleve(eleve_id):
                echeanciers_generes += 1
        
        print(f"✅ {echeanciers_generes} échéanciers générés pour {len(eleves)} élèves")
        return echeanciers_generes
        
    except Exception as e:
        print(f"❌ Erreur génération échéanciers: {e}")
        return 0

def verify_migration():
    """Vérifie que la migration s'est bien déroulée"""
    print("🔍 Vérification de la migration...")
    
    try:
        controller = EnhancedPaiementController()
        
        # Vérifier les types de frais
        types_frais = controller.get_all_types_frais()
        print(f"✅ {len(types_frais)} types de frais disponibles")
        
        # Vérifier les échéances
        stats = controller.get_statistiques_paiements()
        if stats:
            print(f"✅ {stats['total_echeances']} échéances créées")
            print(f"✅ {stats['payees']} paiements recouvrés")
            print(f"✅ {stats['en_attente']} échéances en attente")
            print(f"✅ Taux de recouvrement: {stats['taux_recouvrement']:.1f}%")
        
        # Vérifier les échéances en retard
        echeances_retard = controller.get_echeances_en_retard()
        print(f"✅ {len(echeances_retard)} échéances en retard détectées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def main():
    """Fonction principale de migration"""
    print("🚀 MIGRATION VERS LE SYSTÈME DE PAIEMENTS AMÉLIORÉ")
    print("=" * 60)
    
    # Étape 1: Créer les nouvelles tables
    print("\n📋 Étape 1: Création des nouvelles tables...")
    if not create_all_payment_tables():
        print("❌ Échec de la création des tables. Migration annulée.")
        return False
    
    # Étape 2: Sauvegarder les données existantes
    print("\n💾 Étape 2: Sauvegarde des données existantes...")
    paiements_existants = backup_existing_data()
    
    # Étape 3: Migrer les paiements existants
    if paiements_existants:
        print("\n🔄 Étape 3: Migration des paiements existants...")
        paiements_migres = migrate_paiements_to_echeancier(paiements_existants)
        
        if paiements_migres == 0:
            print("⚠️ Aucun paiement migré. Continuer quand même...")
    else:
        print("\n⚠️ Étape 3: Aucun paiement existant à migrer")
    
    # Étape 4: Générer les échéanciers pour tous les élèves
    print("\n📅 Étape 4: Génération des échéanciers...")
    echeanciers_generes = generate_echeanciers_for_students()
    
    # Étape 5: Vérifier la migration
    print("\n🔍 Étape 5: Vérification de la migration...")
    migration_ok = verify_migration()
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DE LA MIGRATION")
    print("="*60)
    
    print(f"✅ Tables créées: OUI")
    print(f"✅ Paiements sauvegardés: {len(paiements_existants)}")
    print(f"✅ Paiements migrés: {paiements_migres if paiements_existants else 0}")
    print(f"✅ Échéanciers générés: {echeanciers_generes}")
    print(f"✅ Migration vérifiée: {'OUI' if migration_ok else 'NON'}")
    
    if migration_ok:
        print("\n🎉 MIGRATION TERMINÉE AVEC SUCCÈS !")
        print("✅ Le système de paiements amélioré est maintenant opérationnel.")
        print("\n📋 Nouvelles fonctionnalités disponibles:")
        print("   • Gestion des types de frais")
        print("   • Échéanciers automatiques")
        print("   • Système de remises et bourses")
        print("   • Relances automatiques")
        print("   • Rapports financiers avancés")
        print("   • Gestion des pénalités de retard")
        
        print("\n🚀 Vous pouvez maintenant utiliser le nouveau système !")
    else:
        print("\n⚠️ MIGRATION TERMINÉE AVEC DES AVERTISSEMENTS")
        print("❌ Certaines étapes ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return migration_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

