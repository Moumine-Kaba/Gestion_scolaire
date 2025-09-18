#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de réinitialisation des utilisateurs avec RBAC pour EduManager+
Supprime la table users existante et crée de nouveaux utilisateurs avec leurs rôles
"""

import os
import sys
import sqlite3
from pathlib import Path

# Ajouter le répertoire src au path
project_root = Path(__file__).resolve().parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

from src.modules.auth.models.rbac_system import RBACSystem

def reset_users_and_roles():
    """Supprime la table users et crée de nouveaux utilisateurs avec rôles"""
    
    print("🔄 Réinitialisation des utilisateurs avec RBAC")
    print("=" * 50)
    
    # Chemin de la base de données
    db_path = project_root / "database" / "edumanager.db"
    
    print(f"📁 Base de données: {db_path}")
    
    try:
        # 1. Supprimer la table users existante
        print("\n🗑️ Suppression de la table users existante...")
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS utilisateurs")
        conn.commit()
        conn.close()
        print("✅ Table utilisateurs supprimée")
        
        # 2. Recréer la table utilisateurs
        print("\n📋 Création de la nouvelle table utilisateurs...")
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE utilisateurs (
                id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_utilisateur TEXT UNIQUE NOT NULL,
                mot_de_passe TEXT NOT NULL,
                email TEXT,
                nom TEXT,
                prenom TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                derniere_connexion TIMESTAMP,
                est_actif BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
        print("✅ Table utilisateurs recréée")
        
        # 3. Initialiser le système RBAC
        print("\n🔧 Initialisation du système RBAC...")
        rbac = RBACSystem(str(db_path), dev_mode=False)
        
        # 4. Créer les utilisateurs avec leurs rôles
        print("\n👥 Création des utilisateurs avec rôles...")
        
        users_data = [
            {
                "username": "directeur",
                "password": "directeur123",
                "email": "directeur@ecole.com",
                "nom": "Dupont",
                "prenom": "Jean",
                "roles": "Directeur"
            },
            {
                "username": "comptable",
                "password": "comptable123",
                "email": "comptable@ecole.com",
                "nom": "Martin",
                "prenom": "Marie",
                "roles": "Comptable"
            },
            {
                "username": "secretaire",
                "password": "secretaire123",
                "email": "secretaire@ecole.com",
                "nom": "Bernard",
                "prenom": "Sophie",
                "roles": "Secrétaire"
            },
            {
                "username": "surveillant",
                "password": "surveillant123",
                "email": "surveillant@ecole.com",
                "nom": "Petit",
                "prenom": "Pierre",
                "roles": "Surveillant"
            },
            {
                "username": "admin",
                "password": "admin123",
                "email": "admin@ecole.com",
                "nom": "Administrateur",
                "prenom": "Système",
                "roles": "Directeur"
            }
        ]
        
        created_count = 0
        for user_data in users_data:
            try:
                # Créer l'utilisateurs
                conn = sqlite3.connect(str(db_path), timeout=30)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, email, nom, prenom)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_data["username"],
                    user_data["password"],
                    user_data["email"],
                    user_data["nom"],
                    user_data["prenom"]
                ))
                
                user_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                # Attribuer le rôle
                if rbac.assign_role_to_user(user_id, user_data["roles"]):
                    print(f"✅ {user_data['username']} ({user_data['nom']} {user_data['prenom']}) → {user_data['roles']}")
                    created_count += 1
                else:
                    print(f"❌ Échec attribution rôle pour {user_data['username']}")
                    
            except Exception as e:
                print(f"❌ Erreur création utilisateurs {user_data['username']}: {e}")
        
        print(f"\n✅ {created_count} utilisateurs créés avec leurs rôles")
        
        # 5. Afficher le résumé
        print("\n📊 Résumé des utilisateurs créés:")
        print("=" * 40)
        
        for user_data in users_data:
            print(f"👤 {user_data['username']}")
            print(f"   Nom: {user_data['nom']} {user_data['prenom']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Rôle: {user_data['roles']}")
            print(f"   Mot de passe: {user_data['password']}")
            print()
        
        print("🔐 Informations de connexion:")
        print("=" * 30)
        print("Directeur: directeur / directeur123")
        print("Comptable: comptable / comptable123")
        print("Secrétaire: secretaire / secretaire123")
        print("Surveillant: surveillant / surveillant123")
        print("Admin: admin / admin123")
        
        return rbac
        
    except Exception as e:
        print(f"❌ Erreur lors de la réinitialisation: {e}")
        import traceback
        traceback.print_exc()
        return None

def verify_setup(rbac):
    """Vérifie que la configuration est correcte"""
    
    print("\n🔍 Vérification de la configuration...")
    
    try:
        conn = sqlite3.connect(rbac.db_path, timeout=30)
        cursor = conn.cursor()
        
        # Vérifier les utilisateurs
        cursor.execute('SELECT COUNT(*) FROM utilisateurs')
        user_count = cursor.fetchone()[0]
        print(f"✅ {user_count} utilisateurs dans la base")
        
        # Vérifier les rôles
        roles = rbac.get_all_roles()
        print(f"✅ {len(roles)} rôles configurés")
        
        # Vérifier les attributions de rôles
        cursor.execute('SELECT COUNT(*) FROM rbac_user_roles')
        role_assignments = cursor.fetchone()[0]
        print(f"✅ {role_assignments} attributions de rôles")
        
        # Lister les utilisateurs avec leurs rôles
        print("\n📋 Utilisateurs et leurs rôles:")
        cursor.execute('''
            SELECT u.nom_utilisateur, u.nom, u.prenom, r.name
            FROM utilisateurs u
            LEFT JOIN rbac_user_roles ur ON u.id_utilisateur = ur.user_id
            LEFT JOIN rbac_roles r ON ur.role_id = r.id
            ORDER BY u.nom_utilisateur
        ''')
        
        users_with_roles = cursor.fetchall()
        for username, nom, prenom, roles in users_with_roles:
            role_display = roles if roles else "Aucun rôle"
            print(f"  • {username} ({nom} {prenom}): {role_display}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

def main():
    """Fonction principale"""
    
    print("🚀 Réinitialisation des utilisateurs avec RBAC - EduManager+")
    print("⚠️ ATTENTION: Cette opération va supprimer tous les utilisateurs existants!")
    
    # Demander confirmation
    confirm = input("\n❓ Continuer ? (o/n): ").lower().strip()
    if confirm not in ['o', 'oui', 'y', 'yes']:
        print("❌ Opération annulée")
        return
    
    # Effectuer la réinitialisation
    rbac = reset_users_and_roles()
    
    if rbac:
        # Vérifier la configuration
        verify_setup(rbac)
        
        print("\n✅ Réinitialisation terminée avec succès!")
        print("\n📝 Prochaines étapes:")
        print("  1. Redémarrer l'application EduManager+")
        print("  2. Se connecter avec un des nouveaux utilisateurs")
        print("  3. Vérifier que les permissions RBAC fonctionnent correctement")
        print("  4. Tester l'accès aux différentes vues selon le rôle")
        
    else:
        print("\n❌ Échec de la réinitialisation")

if __name__ == "__main__":
    main()
