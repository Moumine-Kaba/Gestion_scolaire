#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test rapide du login avec les utilisateurs créés
EduManager+ - Gestion Scolaire
"""

import os
import sys
import sqlite3

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_login_with_users():
    """Teste le login avec tous les utilisateurs créés"""
    print("🔐 Test du login avec les utilisateurs créés")
    print("=" * 60)
    
    try:
        # Importer le gestionnaire d'authentification
        from models.auth import AuthManager
        
        # Initialiser le gestionnaire
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        
        print("✅ AuthManager initialisé avec succès")
        
        # Liste des utilisateurs à tester
        test_users = [
            ("superadmin", "superadmin123"),
            ("admin", "admin123"),
            ("directeur", "directeur123"),
            ("pedagogique", "pedagogique123"),
            ("proviseur", "proviseur123"),
            ("censeur", "censeur123"),
            ("surveillant", "surveillant123"),
            ("prof_principal", "prof123"),
            ("prof_maths", "maths123"),
            ("prof_francais", "francais123"),
            ("comptable_principal", "comptable123"),
            ("comptable", "comptable123"),
            ("secretaire_principal", "secretaire123"),
            ("secretaire", "secretaire123"),
            ("eleve1", "eleve123"),
            ("eleve2", "eleve123"),
            ("parent1", "parent123"),
            ("parent2", "parent123"),
            ("visiteur", "visiteur123")
        ]
        
        print(f"\n🧪 Test de login pour {len(test_users)} utilisateurs...")
        print("-" * 60)
        
        successful_logins = 0
        failed_logins = 0
        
        for username, password in test_users:
            try:
                print(f"🔑 Test de {username}...", end=" ")
                
                user_info = auth_manager.authenticate_user(username, password)
                
                if user_info:
                    print("✅ SUCCÈS")
                    print(f"    - Rôles: {', '.join(user_info['roles'])}")
                    print(f"    - Permissions: {len(user_info['permissions'])} permissions")
                    successful_logins += 1
                else:
                    print("❌ ÉCHEC")
                    failed_logins += 1
                    
            except Exception as e:
                print(f"❌ ERREUR: {e}")
                failed_logins += 1
        
        print("-" * 60)
        print(f"📊 Résumé des tests:")
        print(f"  - Logins réussis: {successful_logins}")
        print(f"  - Logins échoués: {failed_logins}")
        print(f"  - Taux de succès: {(successful_logins/len(test_users)*100):.1f}%")
        
        if successful_logins == len(test_users):
            print(f"\n🎉 Tous les utilisateurs peuvent se connecter avec succès!")
        else:
            print(f"\n⚠️ Certains utilisateurs ont des problèmes de connexion")
        
        return successful_logins == len(test_users)
        
    except ImportError as e:
        print(f"❌ Impossible d'importer AuthManager: {e}")
        print(f"  - Vérifiez que le fichier models/auth.py existe")
        return False
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")
        return False

def test_specific_user(username, password):
    """Teste le login d'un utilisateur spécifique"""
    print(f"\n🔍 Test détaillé pour {username}")
    print("=" * 40)
    
    try:
        from models.auth import AuthManager
        
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        
        user_info = auth_manager.authenticate_user(username, password)
        
        if user_info:
            print(f"✅ Authentification réussie!")
            print(f"  - ID: {user_info['id_utilisateur']}")
            print(f"  - Username: {user_info['username']}")
            print(f"  - Nom: {user_info['nom']} {user_info['prenom']}")
            print(f"  - Email: {user_info['email']}")
            print(f"  - Statut: {user_info['statut']}")
            print(f"  - Rôles: {', '.join(user_info['roles'])}")
            print(f"  - Permissions: {len(user_info['permissions'])} permissions")
            
            if user_info['permissions']:
                print(f"  - Détail des permissions:")
                for perm in user_info['permissions'][:10]:  # Afficher les 10 premières
                    print(f"    • {perm}")
                if len(user_info['permissions']) > 10:
                    print(f"    ... et {len(user_info['permissions']) - 10} autres")
            
            return True
        else:
            print(f"❌ Échec de l'authentification")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def show_available_users():
    """Affiche la liste des utilisateurs disponibles"""
    print(f"\n👥 Utilisateurs disponibles pour les tests")
    print("=" * 60)
    
    try:
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT u.username, u.nom, u.prenom, r.nom_role, r.niveau_acces
            FROM utilisateurs u
            JOIN user_roles ur ON u.id_utilateur = ur.user_id
            JOIN roles r ON ur.role_id = r.id_role
            ORDER BY r.niveau_acces DESC, u.nom
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("❌ Aucun utilisateur trouvé")
            return
        
        print(f"{'Username':<20} {'Nom':<15} {'Prénom':<15} {'Rôle':<25} {'Niveau':<8}")
        print("-" * 60)
        
        for user in users:
            username, nom, prenom, role, niveau = user
            print(f"{username:<20} {nom:<15} {prenom:<15} {role:<25} {niveau:<8}")
        
        print("-" * 60)
        print(f"Total: {len(users)} utilisateur(s)")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage: {e}")

def main():
    """Menu principal"""
    while True:
        print(f"\n🎯 Menu de test du login")
        print("=" * 40)
        print(f"1. Test complet de tous les utilisateurs")
        print(f"2. Test d'un utilisateur spécifique")
        print(f"3. Afficher les utilisateurs disponibles")
        print(f"4. Quitter")
        
        choice = input(f"\nChoisissez une option (1-4): ").strip()
        
        if choice == "1":
            test_login_with_users()
        elif choice == "2":
            username = input("Entrez le username: ").strip()
            password = input("Entrez le password: ").strip()
            if username and password:
                test_specific_user(username, password)
            else:
                print("❌ Username et password requis")
        elif choice == "3":
            show_available_users()
        elif choice == "4":
            print(f"👋 Au revoir!")
            break
        else:
            print(f"❌ Option invalide. Veuillez choisir 1, 2, 3 ou 4.")

if __name__ == "__main__":
    print("🚀 Script de test du login")
    print("=" * 60)
    
    # Test automatique de tous les utilisateurs
    success = test_login_with_users()
    
    if success:
        print(f"\n🎉 Tous les tests sont passés avec succès!")
        print(f"   Vous pouvez maintenant lancer l'application et vous connecter")
    else:
        print(f"\n⚠️ Certains tests ont échoué")
        print(f"   Vérifiez la création des utilisateurs")
    
    # Proposer le menu interactif
    print(f"\n" + "="*60)
    main()

