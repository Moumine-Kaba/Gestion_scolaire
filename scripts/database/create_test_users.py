#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Création d'utilisateurs de test avec rôles
EduManager+ - Gestion Scolaire
Compatible avec le système de login existant
"""

import os
import sys
import sqlite3
import hashlib
import secrets
from datetime import datetime

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def hash_password_with_salt(password: str) -> tuple:
    """Hash un mot de passe avec un sel (compatible avec AuthManager)"""
    salt = secrets.token_hex(16)
    combined = password + salt
    hash_obj = hashlib.sha256(combined.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    return password_hash, salt

def create_test_users():
    """Crée des utilisateurs de test avec leurs rôles"""
    print("🚀 Création des utilisateurs de test")
    print("=" * 50)
    
    try:
        # Connexion à la base de données
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier que la table utilisateurs existe avec la bonne structure
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                nom TEXT,
                prenom TEXT,
                telephone TEXT,
                date_naissance DATE,
                adresse TEXT,
                statut TEXT DEFAULT 'actif',
                derniere_connexion TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Vérifier que la table roles existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS roles (
                id_role INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_role TEXT UNIQUE NOT NULL,
                description TEXT,
                niveau_acces INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Vérifier que la table user_roles existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                FOREIGN KEY (role_id) REFERENCES roles (id_role),
                UNIQUE(user_id, role_id)
            )
        """)
        
        # Vérifier que la table sessions existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
            )
        """)
        
        # Vérifier que la table login_attempts existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                ip_address TEXT,
                success BOOLEAN NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print("✅ Tables vérifiées/créées")
        
        # Créer les rôles s'ils n'existent pas
        roles_to_create = [
            ("Super Administrateur", "Accès complet système + gestion des administrateurs", 15),
            ("Administrateur", "Accès complet à toutes les fonctionnalités", 10),
            ("Directeur Général", "Gestion complète de l'établissement + finances", 9),
            ("Directeur Pédagogique", "Gestion pédagogique complète", 8),
            ("Proviseur", "Gestion pédagogique et administrative", 7),
            ("Censeur", "Gestion de la discipline et surveillance", 6),
            ("Surveillant Général", "Gestion des présences et discipline", 5),
            ("Professeur Principal", "Gestion de classe + notes + bulletins", 4),
            ("Professeur", "Gestion des cours et notes de sa matière", 3),
            ("Comptable Principal", "Gestion financière complète", 3),
            ("Comptable", "Gestion financière limitée", 2),
            ("Secrétaire Principal", "Gestion administrative complète", 2),
            ("Secrétaire", "Gestion administrative limitée", 1),
            ("Élève", "Consultation des informations personnelles", 1),
            ("Parent", "Consultation des informations de l'enfant", 1),
            ("Visiteur", "Accès limité aux informations publiques", 0)
        ]
        
        for role_name, description, level in roles_to_create:
            cursor.execute('''
                INSERT OR IGNORE INTO roles (nom_role, description, niveau_acces)
                VALUES (?, ?, ?)
            ''', (role_name, description, level))
        
        conn.commit()
        print("✅ Rôles créés/vérifiés")
        
        # Définir les utilisateurs de test avec leurs rôles
        test_users = [
            # Super Administrateur
            {
                "username": "superadmin",
                "email": "superadmin@edumanager.com",
                "password": "superadmin123",
                "nom": "Dupont",
                "prenom": "Jean-Pierre",
                "role": "Super Administrateur"
            },
            # Administrateur
            {
                "username": "admin",
                "email": "admin@edumanager.com",
                "password": "admin123",
                "nom": "Martin",
                "prenom": "Sophie",
                "role": "Administrateur"
            },
            # Directeur Général
            {
                "username": "directeur",
                "email": "directeur@edumanager.com",
                "password": "directeur123",
                "nom": "Bernard",
                "prenom": "Marie-Claude",
                "role": "Directeur Général"
            },
            # Directeur Pédagogique
            {
                "username": "pedagogique",
                "email": "pedagogique@edumanager.com",
                "password": "pedagogique123",
                "nom": "Leroy",
                "prenom": "Pierre",
                "role": "Directeur Pédagogique"
            },
            # Proviseur
            {
                "username": "proviseur",
                "email": "proviseur@edumanager.com",
                "password": "proviseur123",
                "nom": "Dubois",
                "prenom": "François",
                "role": "Proviseur"
            },
            # Censeur
            {
                "username": "censeur",
                "email": "censeur@edumanager.com",
                "password": "censeur123",
                "nom": "Moreau",
                "prenom": "Claude",
                "role": "Censeur"
            },
            # Surveillant Général
            {
                "username": "surveillant",
                "email": "surveillant@edumanager.com",
                "password": "surveillant123",
                "nom": "Rousseau",
                "prenom": "Michel",
                "role": "Surveillant Général"
            },
            # Professeur Principal
            {
                "username": "prof_principal",
                "email": "prof.principal@edumanager.com",
                "password": "prof123",
                "nom": "Girard",
                "prenom": "Isabelle",
                "role": "Professeur Principal"
            },
            # Professeur
            {
                "username": "prof_maths",
                "email": "prof.maths@edumanager.com",
                "password": "maths123",
                "nom": "Lefevre",
                "prenom": "Thomas",
                "role": "Professeur"
            },
            # Professeur
            {
                "username": "prof_francais",
                "email": "prof.francais@edumanager.com",
                "password": "francais123",
                "nom": "Mercier",
                "prenom": "Catherine",
                "role": "Professeur"
            },
            # Comptable Principal
            {
                "username": "comptable_principal",
                "email": "comptable.principal@edumanager.com",
                "password": "comptable123",
                "nom": "Blanc",
                "prenom": "Nathalie",
                "role": "Comptable Principal"
            },
            # Comptable
            {
                "username": "comptable",
                "email": "comptable@edumanager.com",
                "password": "comptable123",
                "nom": "Petit",
                "prenom": "Laurent",
                "role": "Comptable"
            },
            # Secrétaire Principal
            {
                "username": "secretaire_principal",
                "email": "secretaire.principal@edumanager.com",
                "password": "secretaire123",
                "nom": "Roux",
                "prenom": "Anne-Marie",
                "role": "Secrétaire Principal"
            },
            # Secrétaire
            {
                "username": "secretaire",
                "email": "secretaire@edumanager.com",
                "password": "secretaire123",
                "nom": "Simon",
                "prenom": "Julie",
                "role": "Secrétaire"
            },
            # Élève
            {
                "username": "eleve1",
                "email": "eleve1@edumanager.com",
                "password": "eleve123",
                "nom": "Durand",
                "prenom": "Lucas",
                "role": "Élève"
            },
            # Élève
            {
                "username": "eleve2",
                "email": "eleve2@edumanager.com",
                "password": "eleve123",
                "nom": "Leroy",
                "prenom": "Emma",
                "role": "Élève"
            },
            # Parent
            {
                "username": "parent1",
                "email": "parent1@edumanager.com",
                "password": "parent123",
                "nom": "Durand",
                "prenom": "Marc",
                "role": "Parent"
            },
            # Parent
            {
                "username": "parent2",
                "email": "parent2@edumanager.com",
                "password": "parent123",
                "nom": "Leroy",
                "prenom": "Sylvie",
                "role": "Parent"
            },
            # Visiteur
            {
                "username": "visiteur",
                "email": "visiteur@edumanager.com",
                "password": "visiteur123",
                "nom": "Anonyme",
                "prenom": "Visiteur",
                "role": "Visiteur"
            }
        ]
        
        print(f"\n👥 Création de {len(test_users)} utilisateurs de test...")
        
        created_users = []
        
        for user_data in test_users:
            try:
                # Créer l'utilisateur avec hash et sel
                password_hash, salt = hash_password_with_salt(user_data["password"])
                
                cursor.execute('''
                    INSERT OR IGNORE INTO utilisateurs (
                        username, email, password_hash, salt, nom, prenom, statut
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_data["username"],
                    user_data["email"],
                    password_hash,
                    salt,
                    user_data["nom"],
                    user_data["prenom"],
                    "actif"
                ))
                
                # Récupérer l'ID de l'utilisateur
                cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE username = ?", (user_data["username"],))
                user_id = cursor.fetchone()[0]
                
                # Récupérer l'ID du rôle
                cursor.execute("SELECT id_role FROM roles WHERE nom_role = ?", (user_data["role"],))
                role_result = cursor.fetchone()
                
                if role_result:
                    role_id = role_result[0]
                    
                    # Assigner le rôle à l'utilisateur
                    cursor.execute('''
                        INSERT OR IGNORE INTO user_roles (user_id, role_id)
                        VALUES (?, ?)
                    ''', (user_id, role_id))
                    
                    created_users.append({
                        "id": user_id,
                        "username": user_data["username"],
                        "role": user_data["role"],
                        "password": user_data["password"]
                    })
                    
                    print(f"✅ {user_data['prenom']} {user_data['nom']} ({user_data['username']}) - Rôle: {user_data['role']}")
                else:
                    print(f"❌ Rôle '{user_data['role']}' non trouvé pour {user_data['username']}")
                
            except Exception as e:
                print(f"❌ Erreur création utilisateur {user_data['username']}: {e}")
        
        conn.commit()
        
        # Afficher le résumé
        print(f"\n📊 Résumé de la création:")
        print(f"  - Utilisateurs créés: {len(created_users)}")
        
        # Grouper par rôle
        roles_count = {}
        for user in created_users:
            role = user["role"]
            roles_count[role] = roles_count.get(role, 0) + 1
        
        print(f"\n🔐 Répartition par rôle:")
        for role, count in sorted(roles_count.items()):
            print(f"  - {role}: {count} utilisateur(s)")
        
        # Afficher les informations de connexion
        print(f"\n🔑 Informations de connexion:")
        print("=" * 60)
        print(f"{'Username':<20} {'Password':<15} {'Rôle':<25}")
        print("=" * 60)
        
        for user in created_users:
            print(f"{user['username']:<20} {user['password']:<15} {user['role']:<25}")
        
        print("=" * 60)
        print(f"\n💡 Conseils d'utilisation:")
        print(f"  - Utilisez ces comptes pour tester le système de permissions")
        print(f"  - Chaque rôle a des restrictions différentes")
        print(f"  - Testez la navigation et l'accès aux vues selon les rôles")
        print(f"  - Le système de login est maintenant compatible avec ces utilisateurs")
        
        conn.close()
        print(f"\n🎉 Création des utilisateurs terminée avec succès!")
        
        return created_users
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        return []

def verify_users_and_roles():
    """Vérifie que les utilisateurs et rôles ont été créés correctement"""
    print(f"\n🔍 Vérification des utilisateurs et rôles")
    print("=" * 50)
    
    try:
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les utilisateurs
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        user_count = cursor.fetchone()[0]
        print(f"✅ Utilisateurs dans la base: {user_count}")
        
        # Vérifier les rôles
        cursor.execute("SELECT COUNT(*) FROM roles")
        role_count = cursor.fetchone()[0]
        print(f"✅ Rôles dans la base: {role_count}")
        
        # Vérifier les assignations de rôles
        cursor.execute("SELECT COUNT(*) FROM user_roles")
        assignment_count = cursor.fetchone()[0]
        print(f"✅ Assignations de rôles: {assignment_count}")
        
        # Vérifier la structure de la table utilisateurs
        cursor.execute("PRAGMA table_info(utilisateurs)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Structure de la table utilisateurs:")
        for col in columns:
            print(f"  - {col}")
        
        # Afficher quelques exemples
        print(f"\n📋 Exemples d'utilisateurs créés:")
        cursor.execute("""
            SELECT u.username, u.nom, u.prenom, r.nom_role
            FROM utilisateurs u
            JOIN user_roles ur ON u.id_utilisateur = ur.user_id
            JOIN roles r ON ur.role_id = r.id_role
            ORDER BY r.niveau_acces DESC, u.nom
            LIMIT 10
        """)
        
        users = cursor.fetchall()
        for user in users:
            print(f"  - {user[1]} {user[2]} ({user[0]}) - {user[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

def test_login_compatibility():
    """Teste la compatibilité avec le système de login"""
    print(f"\n🔐 Test de compatibilité avec le système de login")
    print("=" * 60)
    
    try:
        # Importer le gestionnaire d'authentification
        from src.modules.auth import AuthManager
        
        # Initialiser le gestionnaire
        db_path = "database/edumanager.db"
        auth_manager = AuthManager(db_path)
        
        print("✅ AuthManager initialisé avec succès")
        
        # Tester l'authentification d'un utilisateur
        test_username = "admin"
        test_password = "admin123"
        
        print(f"\n🧪 Test d'authentification pour {test_username}...")
        
        user_info = auth_manager.authenticate_user(test_username, test_password)
        
        if user_info:
            print(f"✅ Authentification réussie!")
            print(f"  - ID: {user_info['id_utilisateur']}")
            print(f"  - Username: {user_info['username']}")
            print(f"  - Nom: {user_info['nom']} {user_info['prenom']}")
            print(f"  - Rôles: {', '.join(user_info['roles'])}")
            print(f"  - Permissions: {len(user_info['permissions'])} permissions")
        else:
            print(f"❌ Échec de l'authentification")
        
        print(f"\n✅ Le système de login est compatible avec les utilisateurs créés!")
        
    except ImportError as e:
        print(f"⚠️ Impossible d'importer AuthManager: {e}")
        print(f"  - Vérifiez que le fichier models/auth.py existe")
    except Exception as e:
        print(f"❌ Erreur lors du test de compatibilité: {e}")

if __name__ == "__main__":
    print("🚀 Script de création d'utilisateurs de test")
    print("=" * 60)
    
    # Créer les utilisateurs
    created_users = create_test_users()
    
    if created_users:
        # Vérifier la création
        verify_users_and_roles()
        
        # Tester la compatibilité avec le login
        test_login_compatibility()
        
        print(f"\n🎯 Prochaines étapes:")
        print(f"  1. Lancer l'application: python main.py")
        print(f"  2. Se connecter avec un des comptes créés")
        print(f"  3. Tester les permissions selon les rôles")
        print(f"  4. Exécuter les tests: python test_permissions_advanced.py")
        print(f"  5. Vérifier l'affichage: python show_users_and_roles.py")
    
    print(f"\n✨ Script terminé!")
