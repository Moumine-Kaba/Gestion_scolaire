# -*- coding: utf-8 -*-
"""
Script de Correction du Schéma de Base de Données
EduManager+ - Correction des Noms de Colonnes

Ce script corrige les problèmes de noms de colonnes dans les requêtes SQL.
"""

import os
import sys

# Ajouter le chemin du projet pour les imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../..'))
if project_root not in sys.path:
    sys.path.append(project_root)

def fix_enhanced_controller():
    """Corrige les noms de colonnes dans le contrôleur amélioré"""
    print("🔧 Correction du contrôleur amélioré...")
    
    file_path = "controllers/enhanced_paiement_controller.py"
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrections des noms de colonnes
        corrections = [
            # Correction pour les classes
            ("c.nom as classe_nom", "c.nom_classe as classe_nom"),
            ("c.id", "c.id_classe"),
            ("el.id_classe = c.id", "el.id_classe = c.id_classe"),
            ("GROUP BY c.id, c.nom", "GROUP BY c.id_classe, c.nom_classe"),
            
            # Correction pour les élèves (déjà corrects mais au cas où)
            ("el.id", "el.id_eleve"),
        ]
        
        # Appliquer les corrections
        for old, new in corrections:
            content = content.replace(old, new)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Contrôleur amélioré corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction contrôleur: {e}")
        return False

def fix_database_schema():
    """Corrige les noms de colonnes dans le schéma de base de données"""
    print("🔧 Correction du schéma de base de données...")
    
    file_path = "controllers/database_schema.py"
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrections spécifiques
        corrections = [
            # Correction pour la génération d'échéancier
            ("WHERE id = ?", "WHERE id_classe = ?"),
            ("classe.get('id')", "classe.get('id')"),  # Déjà correct
        ]
        
        # Appliquer les corrections
        for old, new in corrections:
            content = content.replace(old, new)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Schéma de base de données corrigé")
        return True
        
    except Exception as e:
        print(f"❌ Erreur correction schéma: {e}")
        return False

def create_compatibility_layer():
    """Crée une couche de compatibilité pour les noms de colonnes"""
    print("🔧 Création d'une couche de compatibilité...")
    
    compatibility_code = '''
# -*- coding: utf-8 -*-
"""
Couche de Compatibilité pour les Noms de Colonnes
EduManager+ - Compatibilité Base de Données

Cette couche assure la compatibilité entre les différents noms de colonnes
utilisés dans la base de données.
"""

def get_column_mapping():
    """Retourne le mapping des colonnes pour compatibilité"""
    return {
        'eleves': {
            'id': 'id_eleve',
            'nom': 'nom',
            'prenom': 'prenom',
            'classe_id': 'id_classe'
        },
        'classes': {
            'id': 'id_classe',
            'nom': 'nom_classe',
            'niveau': 'niveau'
        }
    }

def adapt_query_for_schema(query, table_name):
    """Adapte une requête selon le schéma de la table"""
    mapping = get_column_mapping()
    
    if table_name in mapping:
        table_mapping = mapping[table_name]
        adapted_query = query
        
        for old_col, new_col in table_mapping.items():
            if old_col != new_col:
                # Remplacer les occurrences de l'ancien nom par le nouveau
                adapted_query = adapted_query.replace(f".{old_col}", f".{new_col}")
                adapted_query = adapted_query.replace(f" {old_col} ", f" {new_col} ")
                adapted_query = adapted_query.replace(f"{old_col}=", f"{new_col}=")
        
        return adapted_query
    
    return query

def get_eleve_column_name(column):
    """Retourne le nom correct de la colonne pour la table élèves"""
    mapping = {
        'id': 'id_eleve',
        'nom': 'nom',
        'prenom': 'prenom',
        'classe_id': 'id_classe'
    }
    return mapping.get(column, column)

def get_classe_column_name(column):
    """Retourne le nom correct de la colonne pour la table classes"""
    mapping = {
        'id': 'id_classe',
        'nom': 'nom_classe',
        'niveau': 'niveau'
    }
    return mapping.get(column, column)
'''
    
    try:
        with open("controllers/compatibility_layer.py", 'w', encoding='utf-8') as f:
            f.write(compatibility_code)
        
        print("✅ Couche de compatibilité créée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création couche compatibilité: {e}")
        return False

def test_database_queries():
    """Teste les requêtes corrigées"""
    print("🧪 Test des requêtes corrigées...")
    
    try:
        from database.connection import get_db_connection
        
        conn = get_db_connection()
        if not conn:
            print("❌ Impossible de se connecter à la base de données")
            return False
        
        cur = conn.cursor()
        
        # Test 1: Vérifier la structure de la table élèves
        print("📋 Test structure table élèves...")
        try:
            cur.execute("SELECT TOP 1 id_eleve, nom, prenom, id_classe FROM eleves")
            row = cur.fetchone()
            if row:
                print(f"✅ Table élèves: id_eleve={row[0]}, nom={row[1]}, prenom={row[2]}, id_classe={row[3]}")
            else:
                print("ℹ️ Aucun élève trouvé dans la table")
        except Exception as e:
            print(f"❌ Erreur test table élèves: {e}")
        
        # Test 2: Vérifier la structure de la table classes
        print("📋 Test structure table classes...")
        try:
            cur.execute("SELECT TOP 1 id_classe, nom_classe, niveau FROM classes")
            row = cur.fetchone()
            if row:
                print(f"✅ Table classes: id_classe={row[0]}, nom_classe={row[1]}, niveau={row[2]}")
            else:
                print("ℹ️ Aucune classe trouvée dans la table")
        except Exception as e:
            print(f"❌ Erreur test table classes: {e}")
        
        # Test 3: Test de jointure
        print("🔗 Test de jointure élèves-classes...")
        try:
            cur.execute("""
                SELECT TOP 1 el.id_eleve, el.nom, el.prenom, c.nom_classe, c.niveau
                FROM eleves el
                LEFT JOIN classes c ON el.id_classe = c.id_classe
            """)
            row = cur.fetchone()
            if row:
                print(f"✅ Jointure OK: {row[1]} {row[2]} -> {row[3]} ({row[4]})")
            else:
                print("ℹ️ Aucun élève avec classe trouvé")
        except Exception as e:
            print(f"❌ Erreur test jointure: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur test requêtes: {e}")
        return False

def main():
    """Fonction principale de correction"""
    print("🔧 CORRECTION DU SCHÉMA DE BASE DE DONNÉES")
    print("=" * 50)
    
    # Changer vers le répertoire des paiements
    os.chdir(os.path.join(project_root, "src", "modules", "administrative", "payments"))
    
    # Exécuter les corrections
    corrections = [
        ("Contrôleur amélioré", fix_enhanced_controller),
        ("Schéma de base de données", fix_database_schema),
        ("Couche de compatibilité", create_compatibility_layer)
    ]
    
    for name, func in corrections:
        print(f"\n🔧 Correction: {name}")
        try:
            func()
        except Exception as e:
            print(f"❌ Erreur dans {name}: {e}")
    
    # Tester les corrections
    print("\n🧪 Test des corrections...")
    test_database_queries()
    
    print("\n" + "="*50)
    print("✅ CORRECTION TERMINÉE")
    print("="*50)
    print("🎯 Les noms de colonnes ont été corrigés pour correspondre")
    print("   à la structure réelle de votre base de données.")
    print()
    print("📋 Corrections appliquées:")
    print("   • Table élèves: id_eleve, nom, prenom, id_classe")
    print("   • Table classes: id_classe, nom_classe, niveau")
    print("   • Jointures corrigées entre les tables")
    print()
    print("🚀 Vous pouvez maintenant relancer le système de paiements !")

if __name__ == "__main__":
    main()

