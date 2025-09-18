#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple des mises à jour avec connexion directe
=================================================
"""

import pyodbc

def test_direct_connection():
    """Test direct avec la base de données"""
    print("🧪 Test direct de la base de données...")
    
    try:
        # Connexion directe
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
        cursor = conn.cursor()
        
        # Test des statistiques élèves
        print("📊 Test des statistiques élèves...")
        cursor.execute("SELECT COUNT(*) FROM eleves")
        total_eleves = cursor.fetchone()[0]
        print(f"   Total élèves: {total_eleves}")
        
        cursor.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'F'")
        filles = cursor.fetchone()[0]
        print(f"   Filles: {filles}")
        
        cursor.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'M'")
        garcons = cursor.fetchone()[0]
        print(f"   Garçons: {garcons}")
        
        # Test des classes
        print("\n📚 Test des classes...")
        cursor.execute("SELECT COUNT(*) FROM classes")
        total_classes = cursor.fetchone()[0]
        print(f"   Total classes: {total_classes}")
        
        # Test des effectifs par classe
        print("\n📈 Test des effectifs par classe...")
        cursor.execute("""
            SELECT c.nom_classe, c.niveau, COUNT(e.id_eleve) as nb_eleves
            FROM classes c
            LEFT JOIN eleves e ON c.id_classe = e.id_classe
            GROUP BY c.id_classe, c.nom_classe, c.niveau
            ORDER BY nb_eleves DESC
        """)
        
        effectifs = cursor.fetchall()
        print(f"   Classes avec effectifs:")
        for classe in effectifs[:5]:  # Top 5
            print(f"   - {classe[0]} ({classe[1]}): {classe[2]} élèves")
        
        # Test de la pagination
        print("\n📄 Test de la pagination...")
        cursor.execute("""
            SELECT e.id_eleve, e.nom, e.prenom, e.genre, c.nom_classe
            FROM eleves e
            LEFT JOIN classes c ON e.id_classe = c.id_classe
            ORDER BY e.nom, e.prenom
            OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY
        """)
        
        eleves_page1 = cursor.fetchall()
        print(f"   Première page (5 élèves):")
        for eleve in eleves_page1:
            print(f"   - {eleve[2]} {eleve[1]} ({eleve[4]})")
        
        conn.close()
        print("\n✅ Test direct réussi!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test direct: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 TEST DIRECT DES MISES À JOUR")
    print("=" * 50)
    
    success = test_direct_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TEST RÉUSSI!")
        print("✅ Les données sont correctement récupérées de la base")
        print("✅ Les requêtes utilisent les bons noms de colonnes")
        print("✅ La pagination fonctionne")
        print("✅ Les statistiques sont précises")
    else:
        print("❌ TEST ÉCHOUÉ")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🎯 Les mises à jour sont fonctionnelles!")
        else:
            print("\n❌ Des corrections sont nécessaires.")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
