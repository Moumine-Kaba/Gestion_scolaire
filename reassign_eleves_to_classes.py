#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour réassigner les élèves aux classes
"""

import os
import sys

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
    """Récupère toutes les classes"""
    try:
        conn = _connect()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("SELECT id_classe, nom_classe FROM classes ORDER BY nom_classe")
        rows = cursor.fetchall()
        
        classes = []
        for row in rows:
            classes.append({'id': row[0], 'nom': row[1]})
        
        conn.close()
        return classes
        
    except Exception as e:
        print(f"❌ Erreur récupération classes: {e}")
        return []

def get_all_eleves():
    """Récupère tous les élèves"""
    try:
        conn = _connect()
        if not conn:
            return []
            
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_eleve, nom, prenom, id_classe, date_naissance, genre
            FROM eleves 
            ORDER BY nom, prenom
        """)
        rows = cursor.fetchall()
        
        eleves = []
        for row in rows:
            eleves.append({
                'id': row[0],
                'nom': row[1],
                'prenom': row[2],
                'id_classe': row[3],
                'date_naissance': row[4],
                'genre': row[5]
            })
        
        conn.close()
        return eleves
        
    except Exception as e:
        print(f"❌ Erreur récupération élèves: {e}")
        return []

def assign_eleve_to_class(eleve_id, classe_id):
    """Assigne un élève à une classe"""
    try:
        conn = _connect()
        if not conn:
            return False
            
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE eleves 
            SET id_classe = ?
            WHERE id_eleve = ?
        """, (classe_id, eleve_id))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur assignation élève {eleve_id}: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎓 Réassignation des élèves aux classes")
    print("=" * 50)
    
    # Récupérer les classes et élèves
    classes = get_all_classes()
    eleves = get_all_eleves()
    
    if not classes:
        print("❌ Aucune classe trouvée")
        return
        
    if not eleves:
        print("❌ Aucun élève trouvé")
        return
    
    print(f"📚 {len(classes)} classes trouvées:")
    for i, classe in enumerate(classes):
        print(f"  {i+1}. {classe['nom']}")
    
    print(f"\n👨‍🎓 {len(eleves)} élèves trouvés")
    
    # Afficher les élèves non assignés
    eleves_non_assignes = [e for e in eleves if e['id_classe'] is None]
    eleves_assignes = [e for e in eleves if e['id_classe'] is not None]
    
    print(f"📊 Statut actuel:")
    print(f"  - Élèves assignés: {len(eleves_assignes)}")
    print(f"  - Élèves non assignés: {len(eleves_non_assignes)}")
    
    if eleves_non_assignes:
        print(f"\n🔍 Élèves non assignés:")
        for eleve in eleves_non_assignes[:10]:  # Afficher les 10 premiers
            print(f"  - {eleve['nom']} {eleve['prenom']}")
        if len(eleves_non_assignes) > 10:
            print(f"  ... et {len(eleves_non_assignes) - 10} autres")
    
    print(f"\n💡 Instructions:")
    print("1. Lancez l'application: python main.py")
    print("2. Allez dans la section 'Élèves'")
    print("3. Cliquez sur 'Ajouter Élève' ou modifiez un élève existant")
    print("4. Dans le formulaire, sélectionnez la classe dans le champ 'Classe'")
    print("5. Sauvegardez pour assigner l'élève à la classe")
    
    print(f"\n🎯 Alternative rapide:")
    print("Vous pouvez aussi utiliser la vue des classes pour voir combien d'élèves")
    print("sont assignés à chaque classe (le compteur s'affiche sur les cartes)")

if __name__ == "__main__":
    main()
