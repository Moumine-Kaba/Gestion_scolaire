#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier et corriger l'organisation des niveaux scolaires
===================================================================
"""

import pyodbc

def check_current_classes():
    """Vérifie les classes actuelles dans la base"""
    print("🔍 Vérification des classes actuelles...")
    
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        cursor.execute("SELECT nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        classes = cursor.fetchall()
        
        print(f"📚 {len(classes)} classes trouvées:")
        for classe in classes:
            print(f"   - {classe[0]} ({classe[1]})")
        
        conn.close()
        return classes
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def update_class_levels():
    """Met à jour les niveaux des classes selon le système français"""
    print("\n🔄 Mise à jour des niveaux scolaires...")
    
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        # Mapping des classes vers les bons niveaux
        level_mapping = {
            # Primaire (1° à 6°)
            "1°": "Primaire",
            "2°": "Primaire", 
            "3°": "Primaire",
            "4°": "Primaire",
            "5°": "Primaire",
            "6°": "Primaire",
            
            # Collège (7° à 10°)
            "7°": "Collège",
            "8°": "Collège",
            "9°": "Collège", 
            "10°": "Collège",
            
            # Lycée (11°, 12°, TSE, TSM, TSS, 1°)
            "11° SE": "Lycée",
            "11° SM": "Lycée", 
            "11° SS": "Lycée",
            "12° SE": "Lycée",
            "12° SM": "Lycée",
            "12° SS": "Lycée",
            "TSE": "Lycée",
            "TSM": "Lycée",
            "TSS": "Lycée",
            "1°": "Lycée"  # 1° est en fait Terminale au lycée
        }
        
        # Mettre à jour chaque classe
        for nom_classe, nouveau_niveau in level_mapping.items():
            cursor.execute("UPDATE classes SET niveau = ? WHERE nom_classe = ?", (nouveau_niveau, nom_classe))
            print(f"   ✅ {nom_classe} → {nouveau_niveau}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Mise à jour terminée!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur mise à jour: {e}")
        return False

def verify_update():
    """Vérifie que la mise à jour a bien fonctionné"""
    print("\n🔍 Vérification de la mise à jour...")
    
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        cursor.execute("SELECT nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        classes = cursor.fetchall()
        
        # Organiser par niveau
        niveaux = {}
        for classe in classes:
            niveau = classe[1]
            if niveau not in niveaux:
                niveaux[niveau] = []
            niveaux[niveau].append(classe[0])
        
        print("📚 Organisation par niveau:")
        for niveau in ["Primaire", "Collège", "Lycée"]:
            if niveau in niveaux:
                print(f"   📖 {niveau}: {len(niveaux[niveau])} classes")
                for classe in niveaux[niveau]:
                    print(f"      - {classe}")
            else:
                print(f"   ❌ {niveau}: Aucune classe")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎓 CORRECTION DE L'ORGANISATION DES NIVEAUX SCOLAIRES")
    print("=" * 60)
    
    # Vérifier l'état actuel
    classes = check_current_classes()
    if not classes:
        return False
    
    # Mettre à jour les niveaux
    if not update_class_levels():
        return False
    
    # Vérifier la mise à jour
    if not verify_update():
        return False
    
    print("\n🎉 ORGANISATION CORRIGÉE AVEC SUCCÈS!")
    print("✅ Primaire: 1° à 6°")
    print("✅ Collège: 7° à 10°") 
    print("✅ Lycée: 11°, 12°, TSE, TSM, TSS, 1°")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Échec de la correction")
            exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        exit(1)

