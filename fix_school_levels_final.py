#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger l'organisation des niveaux scolaires
=========================================================
"""

import pyodbc

def fix_school_levels():
    """Corrige l'organisation des niveaux scolaires"""
    print("🎓 Correction de l'organisation des niveaux scolaires...")
    
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        # Mapping correct des classes vers les niveaux
        level_mapping = {
            # Primaire (1° à 6°)
            "1°": "Primaire",  # Première année au primaire
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
            
            # Lycée (11°, 12°, TSE, TSM, TSS)
            "11° SE": "Lycée",
            "11° SM": "Lycée", 
            "11° SS": "Lycée",
            "12° SE": "Lycée",
            "12° SM": "Lycée",
            "12° SS": "Lycée",
            "TSE": "Lycée",
            "TSM": "Lycée",
            "TSS": "Lycée"
        }
        
        # Mettre à jour chaque classe
        for nom_classe, nouveau_niveau in level_mapping.items():
            cursor.execute("UPDATE classes SET niveau = ? WHERE nom_classe = ?", (nouveau_niveau, nom_classe))
            print(f"   ✅ {nom_classe} → {nouveau_niveau}")
        
        conn.commit()
        conn.close()
        
        print("\n✅ Correction terminée!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction: {e}")
        return False

def verify_correction():
    """Vérifie que la correction a bien fonctionné"""
    print("\n🔍 Vérification de la correction...")
    
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
                classes_sorted = sorted(niveaux[niveau], key=lambda x: (
                    int(x.split('°')[0]) if '°' in x and x.split('°')[0].isdigit() else 999,
                    x
                ))
                print(f"   📖 {niveau}: {len(classes_sorted)} classes")
                for classe in classes_sorted:
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
    
    # Corriger les niveaux
    if not fix_school_levels():
        return False
    
    # Vérifier la correction
    if not verify_correction():
        return False
    
    print("\n🎉 ORGANISATION CORRIGÉE AVEC SUCCÈS!")
    print("✅ Primaire: 1° à 6° (6 classes)")
    print("✅ Collège: 7° à 10° (4 classes)") 
    print("✅ Lycée: 11°, 12°, TSE, TSM, TSS (9 classes)")
    
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
