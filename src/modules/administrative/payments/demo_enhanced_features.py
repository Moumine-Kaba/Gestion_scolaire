# -*- coding: utf-8 -*-
"""
Démonstration des Fonctionnalités Améliorées
EduManager+ - Système de Paiements Avancé

Ce script démontre toutes les nouvelles fonctionnalités du système de paiements.
"""

import os
import sys
from datetime import datetime, timedelta

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.modules.administrative.payments.controllers.enhanced_paiement_controller import (
    EnhancedPaiementController
)

def demo_types_frais():
    """Démonstration de la gestion des types de frais"""
    print("🎯 DÉMONSTRATION: Gestion des Types de Frais")
    print("=" * 50)
    
    controller = EnhancedPaiementController()
    
    # Récupérer tous les types de frais
    types_frais = controller.get_all_types_frais()
    
    print(f"📋 {len(types_frais)} types de frais disponibles:")
    print()
    
    for tf in types_frais:
        print(f"• {tf['nom']}")
        print(f"  💰 Montant: {tf['montant_standard']:,} GNF")
        print(f"  📅 Périodicité: {tf['periodicite']}")
        print(f"  🎓 Niveau: {tf['niveau_educatif']}")
        print(f"  ⚡ Obligatoire: {'Oui' if tf['est_obligatoire'] else 'Non'}")
        print(f"  ✅ Actif: {'Oui' if tf['est_actif'] else 'Non'}")
        print()
    
    # Ajouter un nouveau type de frais
    print("➕ Ajout d'un nouveau type de frais...")
    success = controller.add_type_frais(
        nom="Frais de stage",
        description="Frais pour les stages pratiques",
        montant_standard=75000,
        periodicite="ponctuel",
        niveau_educatif="lycee",
        est_obligatoire=False
    )
    
    if success:
        print("✅ Nouveau type de frais ajouté avec succès !")
    else:
        print("❌ Erreur lors de l'ajout du type de frais")
    
    print("\n" + "="*50)

def demo_echeancier():
    """Démonstration du système d'échéancier"""
    print("🎯 DÉMONSTRATION: Système d'Échéancier")
    print("=" * 50)
    
    controller = EnhancedPaiementController()
    
    # Récupérer le premier élève disponible
    from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
    
    eleves = get_all_eleves()
    if not eleves:
        print("⚠️ Aucun élève trouvé pour la démonstration")
        return
    
    # Prendre le premier élève
    premier_eleve = eleves[0]
    if isinstance(premier_eleve, (tuple, list)):
        eleve_id = premier_eleve[0]
        eleve_nom = f"{premier_eleve[1]} {premier_eleve[2]}"
    else:
        eleve_id = premier_eleve.get('id_eleve')
        eleve_nom = f"{premier_eleve.get('nom')} {premier_eleve.get('prenom')}"
    
    print(f"👤 Élève de démonstration: {eleve_nom} (ID: {eleve_id})")
    print()
    
    # Récupérer l'échéancier de l'élève
    echeancier = controller.get_echeancier_eleve(eleve_id)
    
    if echeancier:
        print(f"📅 Échéancier de {eleve_nom}:")
        print()
        
        total_montant = 0
        paiements_payes = 0
        
        for echeance in echeancier:
            statut_emoji = {
                'en_attente': '⏳',
                'paye': '✅',
                'en_retard': '⚠️',
                'annule': '❌'
            }.get(echeance['statut'], '❓')
            
            print(f"{statut_emoji} {echeance['type_frais_nom']}")
            print(f"   💰 Montant: {echeance['montant_final']:,} GNF")
            print(f"   📅 Échéance: {echeance['date_echeance']}")
            
            if echeance['date_paiement']:
                print(f"   💳 Paiement: {echeance['date_paiement']} ({echeance['mode_paiement']})")
            else:
                print(f"   💳 Paiement: Non effectué")
            
            if echeance['penalites'] > 0:
                print(f"   ⚠️ Pénalités: {echeance['penalites']:,} GNF")
            
            if echeance['nb_relances'] > 0:
                print(f"   📧 Relances: {echeance['nb_relances']}")
            
            print()
            
            total_montant += echeance['montant_final']
            if echeance['statut'] == 'paye':
                paiements_payes += 1
        
        print(f"📊 Résumé pour {eleve_nom}:")
        print(f"   💰 Total des échéances: {total_montant:,} GNF")
        print(f"   ✅ Paiements effectués: {paiements_payes}/{len(echeancier)}")
        print(f"   📈 Taux de paiement: {(paiements_payes/len(echeancier)*100):.1f}%")
    else:
        print(f"⚠️ Aucun échéancier trouvé pour {eleve_nom}")
        print("🔄 Génération automatique de l'échéancier...")
        
        if controller.generer_echeancier_eleve(eleve_id):
            print("✅ Échéancier généré avec succès !")
        else:
            print("❌ Erreur lors de la génération de l'échéancier")
    
    print("\n" + "="*50)

def demo_statistiques():
    """Démonstration des statistiques avancées"""
    print("🎯 DÉMONSTRATION: Statistiques Avancées")
    print("=" * 50)
    
    controller = EnhancedPaiementController()
    
    # Récupérer les statistiques générales
    stats = controller.get_statistiques_paiements()
    
    if stats:
        print(f"📊 Statistiques pour l'année scolaire {stats['annee_scolaire']}:")
        print()
        
        print(f"📋 Échéances totales: {stats['total_echeances']}")
        print(f"✅ Paiements effectués: {stats['payees']}")
        print(f"⏳ En attente: {stats['en_attente']}")
        print(f"⚠️ En retard: {stats['en_retard']}")
        print()
        
        print(f"💰 Montant total attendu: {stats['montant_total']:,} GNF")
        print(f"💳 Montant recouvré: {stats['montant_recouvre']:,} GNF")
        print(f"📈 Taux de recouvrement: {stats['taux_recouvrement']:.1f}%")
        print(f"⚖️ Pénalités appliquées: {stats['total_penalites']:,} GNF")
        print()
        
        # Statistiques par type de frais
        if stats['stats_par_type']:
            print("📋 Statistiques par type de frais:")
            for stat_type in stats['stats_par_type'][:5]:  # Top 5
                taux_recouvrement = (stat_type['montant_recouvre'] / stat_type['montant_total'] * 100) if stat_type['montant_total'] > 0 else 0
                print(f"   • {stat_type['type_frais']}")
                print(f"     💰 {stat_type['montant_recouvre']:,} / {stat_type['montant_total']:,} GNF ({taux_recouvrement:.1f}%)")
                print(f"     📊 {stat_type['payees']}/{stat_type['nb_echeances']} échéances payées")
            print()
        
        # Statistiques par classe
        if stats['stats_par_classe']:
            print("🏫 Statistiques par classe:")
            for stat_classe in stats['stats_par_classe'][:5]:  # Top 5
                taux_recouvrement = (stat_classe['montant_recouvre'] / stat_classe['montant_total'] * 100) if stat_classe['montant_total'] > 0 else 0
                print(f"   • {stat_classe['classe_nom']} ({stat_classe['nb_eleves']} élèves)")
                print(f"     💰 {stat_classe['montant_recouvre']:,} / {stat_classe['montant_total']:,} GNF ({taux_recouvrement:.1f}%)")
            print()
    else:
        print("⚠️ Aucune statistique disponible")
    
    # Échéances en retard
    echeances_retard = controller.get_echeances_en_retard()
    
    if echeances_retard:
        print(f"⚠️ {len(echeances_retard)} échéances en retard:")
        print()
        
        total_penalites = 0
        for echeance in echeances_retard[:5]:  # Top 5
            print(f"👤 {echeance['eleve_nom']} {echeance['eleve_prenom']} ({echeance['classe_nom']})")
            print(f"   📅 Échéance: {echeance['date_echeance']}")
            print(f"   ⏰ Retard: {echeance['jours_retard']} jours")
            print(f"   💰 Montant: {echeance['montant_final']:,} GNF")
            print(f"   ⚖️ Pénalités: {echeance['penalites']:,} GNF")
            print(f"   📧 Relances: {echeance['nb_relances']}")
            print(f"   📋 Type: {echeance['type_frais_nom']}")
            print()
            
            total_penalites += echeance['penalites']
        
        print(f"💰 Total des pénalités en retard: {total_penalites:,} GNF")
    else:
        print("✅ Aucune échéance en retard")
    
    print("\n" + "="*50)

def demo_rapport_tresorerie():
    """Démonstration du rapport de trésorerie"""
    print("🎯 DÉMONSTRATION: Rapport de Trésorerie")
    print("=" * 50)
    
    controller = EnhancedPaiementController()
    
    # Générer un rapport pour les 30 derniers jours
    date_fin = datetime.now().date()
    date_debut = date_fin - timedelta(days=30)
    
    rapport = controller.get_rapport_tresorerie(
        date_debut.strftime('%Y-%m-%d'),
        date_fin.strftime('%Y-%m-%d')
    )
    
    if rapport:
        print(f"📊 Rapport de trésorerie du {rapport['periode']['debut']} au {rapport['periode']['fin']}:")
        print()
        
        print(f"💰 Total des recettes: {rapport['total_recettes']:,} GNF")
        print(f"📅 Période: {len(rapport['recettes_par_jour'])} jours avec des recettes")
        print()
        
        # Recettes par jour (top 5)
        if rapport['recettes_par_jour']:
            print("📈 Top 5 des meilleurs jours:")
            for recette in sorted(rapport['recettes_par_jour'], key=lambda x: x['montant'], reverse=True)[:5]:
                print(f"   • {recette['date']}: {recette['montant']:,} GNF")
            print()
        
        # Recettes par mode de paiement
        if rapport['recettes_par_mode']:
            print("💳 Recettes par mode de paiement:")
            for mode in rapport['recettes_par_mode']:
                pourcentage = (mode['montant_total'] / rapport['total_recettes'] * 100) if rapport['total_recettes'] > 0 else 0
                print(f"   • {mode['mode_paiement']}")
                print(f"     💰 {mode['montant_total']:,} GNF ({pourcentage:.1f}%)")
                print(f"     📊 {mode['nb_paiements']} paiements")
            print()
    else:
        print("⚠️ Aucun rapport de trésorerie disponible pour cette période")
    
    print("\n" + "="*50)

def demo_remises():
    """Démonstration de la gestion des remises"""
    print("🎯 DÉMONSTRATION: Gestion des Remises")
    print("=" * 50)
    
    controller = EnhancedPaiementController()
    
    # Récupérer le premier élève pour la démo
    from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
    
    eleves = get_all_eleves()
    if not eleves:
        print("⚠️ Aucun élève trouvé pour la démonstration")
        return
    
    eleve = eleves[0]
    if isinstance(eleve, (tuple, list)):
        eleve_id = eleve[0]
        eleve_nom = f"{eleve[1]} {eleve[2]}"
    else:
        eleve_id = eleve.get('id_eleve')
        eleve_nom = f"{eleve.get('nom')} {eleve.get('prenom')}"
    
    print(f"👤 Élève de démonstration: {eleve_nom} (ID: {eleve_id})")
    print()
    
    # Récupérer les remises de l'élève
    remises = controller.get_remises_eleve(eleve_id)
    
    if remises:
        print(f"🎓 Remises pour {eleve_nom}:")
        print()
        
        for remise in remises:
            statut_emoji = {
                'actif': '✅',
                'inactif': '❌',
                'expire': '⏰'
            }.get(remise['statut'], '❓')
            
            print(f"{statut_emoji} {remise['type_remise'].upper()}")
            print(f"   📋 Motif: {remise['motif']}")
            
            if remise['pourcentage']:
                print(f"   📊 Réduction: {remise['pourcentage']}%")
            elif remise['montant_fixe']:
                print(f"   💰 Réduction: {remise['montant_fixe']:,} GNF")
            
            print(f"   📅 Période: {remise['date_debut']} - {remise['date_fin'] or 'Illimitée'}")
            
            if remise['approbateur']:
                print(f"   ✅ Approuvé par: {remise['approbateur']}")
            
            print()
    else:
        print(f"ℹ️ Aucune remise trouvée pour {eleve_nom}")
        
        # Ajouter une remise de démonstration
        print("➕ Ajout d'une remise de démonstration...")
        
        success = controller.ajouter_remise(
            eleve_id=eleve_id,
            type_remise="reduction",
            motif="Famille nombreuse - 3 enfants dans l'école",
            pourcentage=10.0,
            date_debut=datetime.now().date(),
            date_fin=(datetime.now() + timedelta(days=365)).date(),
            approbateur="Directeur de l'école"
        )
        
        if success:
            print("✅ Remise de démonstration ajoutée avec succès !")
        else:
            print("❌ Erreur lors de l'ajout de la remise")
    
    print("\n" + "="*50)

def main():
    """Fonction principale de démonstration"""
    print("🎪 DÉMONSTRATION DU SYSTÈME DE PAIEMENTS AMÉLIORÉ")
    print("=" * 60)
    print("EduManager+ - Fonctionnalités Avancées")
    print("=" * 60)
    
    try:
        # Vérifier que le contrôleur fonctionne
        controller = EnhancedPaiementController()
        print("✅ Contrôleur initialisé avec succès")
        print()
        
        # Démonstrations
        demos = [
            ("Gestion des Types de Frais", demo_types_frais),
            ("Système d'Échéancier", demo_echeancier),
            ("Statistiques Avancées", demo_statistiques),
            ("Rapport de Trésorerie", demo_rapport_tresorerie),
            ("Gestion des Remises", demo_remises)
        ]
        
        for demo_name, demo_func in demos:
            print(f"\n🎬 {demo_name}")
            print("=" * len(demo_name) + 2)
            try:
                demo_func()
            except Exception as e:
                print(f"❌ Erreur dans la démonstration {demo_name}: {e}")
                continue
        
        print("\n" + "="*60)
        print("🎉 DÉMONSTRATION TERMINÉE")
        print("="*60)
        print("✅ Toutes les fonctionnalités du système amélioré ont été démontrées.")
        print()
        print("🚀 Le système de paiements EduManager+ est maintenant prêt !")
        print()
        print("📋 Fonctionnalités disponibles:")
        print("   • Gestion complète des types de frais")
        print("   • Échéanciers automatiques par élève")
        print("   • Système de remises et bourses")
        print("   • Pénalités automatiques de retard")
        print("   • Rapports financiers détaillés")
        print("   • Statistiques en temps réel")
        print("   • Interface moderne et intuitive")
        print()
        print("💡 Pour utiliser le système, lancez l'application EduManager+")
        print("   et accédez au module Paiements.")
        
    except Exception as e:
        print(f"❌ Erreur critique: {e}")
        print("⚠️ Vérifiez que la base de données est correctement configurée.")

if __name__ == "__main__":
    main()

