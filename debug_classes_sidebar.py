#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de debug pour la sidebar des classes
========================================
"""

import pyodbc

def test_classes_sidebar():
    """Test de debug pour la sidebar des classes"""
    print("🔍 Test de debug - Sidebar des classes...")
    
    try:
        # Connexion directe
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        # Test 1: Vérifier les classes disponibles
        print("📚 Test 1: Classes disponibles dans la base...")
        cursor.execute("SELECT nom_classe, niveau FROM classes ORDER BY niveau, nom_classe")
        classes = cursor.fetchall()
        
        print(f"   ✅ {len(classes)} classes trouvées:")
        for classe in classes:
            print(f"      - {classe[0]} ({classe[1]})")
        
        # Test 2: Organiser par niveau comme dans le code
        print("\n📖 Test 2: Organisation par niveau...")
        classes_par_niveau = {}
        for classe in classes:
            nom = classe[0]  # nom_classe
            niveau = classe[1]  # niveau
            if niveau not in classes_par_niveau:
                classes_par_niveau[niveau] = []
            classes_par_niveau[niveau].append(nom)
        
        niveaux_order = ["PRIMAIRE", "COLLÈGE", "LYCÉE"]
        for niveau in niveaux_order:
            if niveau in classes_par_niveau:
                print(f"   📖 {niveau}: {len(classes_par_niveau[niveau])} classes")
                for nom in classes_par_niveau[niveau]:
                    print(f"      - {nom}")
            else:
                print(f"   ❌ {niveau}: Aucune classe trouvée")
        
        conn.close()
        print("\n✅ Test de debug terminé!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

if __name__ == "__main__":
    test_classes_sidebar()

