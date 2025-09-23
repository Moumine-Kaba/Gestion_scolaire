#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script automatique pour assigner les élèves aux classes de manière équilibrée
"""

import os
import sys
import random

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.connection import get_db_connection

def _connect():
    """Crée une connexion à la base de données"""
    conn = get_db_connection()
    return conn

def get_all_classes():
    """Récupère toutes les classes avec leurs capacités"""
    try:
        conn = _connect()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_classe, nom_classe, niveau, capacite 
            FROM classes 
            ORDER BY 
                CASE niveau
                    WHEN 'Primaire' THEN 1
                    WHEN 'Collège' THEN 2
                    WHEN 'Lycée' THEN 3
                    WHEN 'Terminale' THEN 4
                    ELSE 5
                END,
                nom_classe
        """)
        rows = cursor.fetchall()
        
        classes = []
        for row in rows:
            classes.append({
                'id': row[0], 
                'nom': row[1], 
                'niveau': row[2],
                'capacite': row[3] or 50  # Capacité par défaut si NULL
            })
        
        conn.close()
        return classes
        
    except Exception as e:
        print(f"❌ Erreur récupération classes: {e}")
        return []

def get_all_eleves():
    """Récupère tous les élèves non assignés"""
    try:
        conn = _connect()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_eleve, nom, prenom, date_naissance, genre
            FROM eleves 
            WHERE id_classe IS NULL
            ORDER BY nom, prenom
        """)
        rows = cursor.fetchall()
        
        eleves = []
        for row in rows:
            eleves.append({
                'id': row[0],
                'nom': row[1],
                'prenom': row[2],
                'date_naissance': row[3],
                'genre': row[4]
            })
        
        conn.close()
        return eleves
        
    except Exception as e:
        print(f"❌ Erreur récupération élèves: {e}")
        return []

def assign_eleves_to_classes(classes, eleves):
    """Assigne les élèves aux classes de manière équilibrée"""
    try:
        conn = _connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        
        # Calculer la répartition équilibrée
        total_eleves = len(eleves)
        total_capacite = sum(classe['capacite'] for classe in classes)
        
        print(f"📊 Répartition calculée:")
        print(f"  - Total élèves: {total_eleves}")
        print(f"  - Total capacité: {total_capacite}")
        
        if total_eleves > total_capacite:
            print(f"⚠️ Attention: Plus d'élèves ({total_eleves}) que de capacité totale ({total_capacite})")
            print("   Les élèves seront assignés jusqu'à la capacité maximale")
        
        # Répartir les élèves selon les capacités
        eleves_assignes = 0
        eleves_list = eleves.copy()
        random.shuffle(eleves_list)  # Mélanger pour une distribution aléatoire
        
        for classe in classes:
            capacite_classe = classe['capacite']
            eleves_classe = eleves_list[eleves_assignes:eleves_assignes + capacite_classe]
            
            print(f"📚 {classe['nom']} ({classe['niveau']}): {len(eleves_classe)} élèves")
            
            # Assigner les élèves à cette classe
            for eleve in eleves_classe:
                cursor.execute("""
                    UPDATE eleves 
                    SET id_classe = ?
                    WHERE id_eleve = ?
                """, (classe['id'], eleve['id']))
            
            eleves_assignes += len(eleves_classe)
            
            # Si on a assigné tous les élèves, s'arrêter
            if eleves_assignes >= len(eleves_list):
                break
        
        conn.commit()
        conn.close()
        
        print(f"✅ {eleves_assignes} élèves assignés avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur assignation: {e}")
        return False

def show_final_stats():
    """Affiche les statistiques finales"""
    try:
        conn = _connect()
        if not conn:
            return
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                c.nom_classe,
                c.niveau,
                c.capacite,
                COUNT(e.id_eleve) as effectif_reel
            FROM classes c
            LEFT JOIN eleves e ON c.id_classe = e.id_classe
            GROUP BY c.id_classe, c.nom_classe, c.niveau, c.capacite
            ORDER BY 
                CASE c.niveau
                    WHEN 'Primaire' THEN 1
                    WHEN 'Collège' THEN 2
                    WHEN 'Lycée' THEN 3
                    WHEN 'Terminale' THEN 4
                    ELSE 5
                END,
                c.nom_classe
        """)
        rows = cursor.fetchall()
        
        print(f"\n📊 Statistiques finales par classe:")
        print("=" * 60)
        print(f"{'Classe':<15} {'Niveau':<10} {'Effectif':<8} {'Capacité':<8} {'%':<5}")
        print("-" * 60)
        
        total_eleves = 0
        for row in rows:
            nom, niveau, capacite, effectif = row
            pourcentage = (effectif / capacite * 100) if capacite > 0 else 0
            print(f"{nom:<15} {niveau:<10} {effectif:<8} {capacite:<8} {pourcentage:.1f}%")
            total_eleves += effectif
        
        print("-" * 60)
        print(f"{'TOTAL':<15} {'':<10} {total_eleves:<8} {sum(row[2] for row in rows):<8}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur statistiques: {e}")

def main():
    """Fonction principale"""
    print("🎓 Assignation automatique des élèves aux classes")
    print("=" * 60)
    
    # Récupérer les classes et élèves
    print("📚 Récupération des classes...")
    classes = get_all_classes()
    
    print("👨‍🎓 Récupération des élèves...")
    eleves = get_all_eleves()
    
    if not classes:
        print("❌ Aucune classe trouvée")
        return
        
    if not eleves:
        print("✅ Tous les élèves sont déjà assignés!")
        return
    
    print(f"\n📋 Résumé:")
    print(f"  - Classes disponibles: {len(classes)}")
    print(f"  - Élèves à assigner: {len(eleves)}")
    
    # Afficher les classes
    print(f"\n📚 Classes disponibles:")
    for classe in classes:
        print(f"  - {classe['nom']} ({classe['niveau']}) - Capacité: {classe['capacite']}")
    
    # Demander confirmation
    print(f"\n⚠️ Cette opération va assigner {len(eleves)} élèves aux classes.")
    response = input("Continuer? (o/N): ").lower().strip()
    
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Opération annulée")
        return
    
    # Assigner les élèves
    print(f"\n🔄 Assignation en cours...")
    if assign_eleves_to_classes(classes, eleves):
        show_final_stats()
        print(f"\n🎉 Assignation terminée avec succès!")
        print(f"💡 Vous pouvez maintenant lancer l'application pour voir les résultats.")
    else:
        print(f"\n❌ Erreur lors de l'assignation")

if __name__ == "__main__":
    main()
