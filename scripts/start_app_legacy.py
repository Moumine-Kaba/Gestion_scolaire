#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Démarrage Rapide - EduManager+
Vérifie l'état du système et lance l'application
"""
import os
import sys
import subprocess
import sqlite3
from datetime import datetime

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = ['customtkinter', 'PIL', 'matplotlib']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'customtkinter':
                import customtkinter
            elif package == 'matplotlib':
                import matplotlib
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Manquant")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Packages manquants: {', '.join(missing_packages)}")
        print("💡 Installez-les avec: pip install customtkinter Pillow matplotlib")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def check_database():
    """Vérifie l'état de la base de données"""
    print("\n🔍 Vérification de la base de données...")
    
    db_path = "database/edumanager.db"
    
    if not os.path.exists(db_path):
        print("❌ Base de données introuvable")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables essentielles
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        essential_tables = ['utilisateurs', 'roles', 'user_roles']
        missing_tables = [table for table in essential_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Tables manquantes: {', '.join(missing_tables)}")
            conn.close()
            return False
        
        # Vérifier qu'il y a des utilisateurs
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            print("❌ Aucun utilisateur dans la base")
            conn.close()
            return False
        
        print(f"✅ Base de données OK ({user_count} utilisateurs)")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        return False

def quick_repair():
    """Effectue une réparation rapide si nécessaire"""
    print("\n🔧 Réparation rapide du système...")
    
    try:
        # Vérifier si les scripts de réparation existent
        if not all(os.path.exists(script) for script in ['init_tables.py', 'init_test_data.py', 'assign_roles.py']):
            print("❌ Scripts de réparation manquants")
            return False
        
        # Créer les tables si nécessaire
        print("📋 Création des tables...")
        result = subprocess.run([sys.executable, 'init_tables.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ Erreur création tables: {result.stderr}")
            return False
        
        # Ajouter des données de test
        print("📊 Ajout des données de test...")
        result = subprocess.run([sys.executable, 'init_test_data.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ Erreur données de test: {result.stderr}")
            return False
        
        # Assigner les rôles
        print("👥 Attribution des rôles...")
        result = subprocess.run([sys.executable, 'assign_roles.py'], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"❌ Erreur attribution rôles: {result.stderr}")
            return False
        
        print("✅ Réparation rapide terminée")
        return True
        
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la réparation")
        return False
    except Exception as e:
        print(f"❌ Erreur réparation: {e}")
        return False

def launch_application():
    """Lance l'application principale"""
    print("\n🚀 Lancement de l'application...")
    
    try:
        # Vérifier que main.py existe
        if not os.path.exists('main.py'):
            print("❌ Fichier main.py introuvable")
            return False
        
        # Lancer l'application
        print("✅ Application lancée avec succès !")
        print("💡 Fermez cette fenêtre pour arrêter l'application")
        
        # Lancer en arrière-plan
        subprocess.Popen([sys.executable, 'main.py'])
        return True
        
    except Exception as e:
        print(f"❌ Erreur lancement: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎓 EduManager+ - Gestion Scolaire")
    print("=" * 40)
    print(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Étape 1: Vérifier les dépendances
    if not check_dependencies():
        print("\n❌ Dépendances manquantes. Installation requise.")
        return False
    
    # Étape 2: Vérifier la base de données
    if not check_database():
        print("\n⚠️  Problème détecté avec la base de données.")
        print("🔄 Tentative de réparation automatique...")
        
        if not quick_repair():
            print("\n❌ La réparation automatique a échoué.")
            print("💡 Utilisez le script de réparation complet: python repair_system.py")
            return False
        
        # Vérifier à nouveau après réparation
        if not check_database():
            print("\n❌ La base de données n'est toujours pas fonctionnelle.")
            return False
    
    # Étape 3: Lancer l'application
    if not launch_application():
        print("\n❌ Impossible de lancer l'application.")
        return False
    
    print("\n🎉 Prêt ! L'application EduManager+ est en cours d'exécution.")
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n💡 Solutions recommandées:")
            print("1. Exécuter: python repair_system.py")
            print("2. Vérifier les logs d'erreur")
            print("3. Contacter le support technique")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Arrêt demandé par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)
