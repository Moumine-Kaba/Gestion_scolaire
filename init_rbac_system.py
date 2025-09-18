#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'initialisation du système RBAC pour EduManager+
Configure les rôles par défaut et attribue des utilisateurs
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

def setup_rbac_system():
    """Configure le système RBAC"""
    
    # Chemin de la base de données
    db_path = project_root / "database" / "edumanager.db"
    
    print("🔧 Configuration du système RBAC pour EduManager+")
    print(f"📁 Base de données: {db_path}")
    
    # Initialiser le système RBAC
    try:
        rbac = RBACSystem(str(db_path), dev_mode=False)
        print("✅ Système RBAC initialisé")
        
        # Lister les rôles créés
        roles = rbac.get_all_roles()
        print(f"\n📋 Rôles disponibles ({len(roles)}):")
        for roles in roles:
            print(f"  • {roles.name}: {roles.description}")
        
        return rbac
        
    except Exception as e:
        print(f"❌ Erreur initialisation RBAC: {e}")
        return None

def assign_roles_to_users(rbac: RBACSystem):
    """Attribue des rôles aux utilisateurs existants"""
    
    print("\n👥 Attribution des rôles aux utilisateurs...")
    
    try:
        conn = sqlite3.connect(rbac.db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les utilisateurs
        cursor.execute('SELECT id_utilisateur, nom_utilisateur, email FROM utilisateurs')
        users = cursor.fetchall()
        
        if not users:
            print("⚠️ Aucun utilisateurs trouvé dans la base de données")
            return
        
        print(f"📊 {len(users)} utilisateurs trouvés")
        
        # Attribuer des rôles par défaut
        role_assignments = {
            "admin": "Directeur",
            "directeur": "Directeur", 
            "comptable": "Comptable",
            "secretaire": "Secrétaire",
            "surveillant": "Surveillant"
        }
        
        assigned_count = 0
        for user_id, username, email in users:
            # Déterminer le rôle basé sur le nom d'utilisateurs ou l'email
            role_to_assign = None
            
            username_lower = username.lower()
            email_lower = email.lower() if email else ""
            
            for key, role_name in role_assignments.items():
                if key in username_lower or key in email_lower:
                    role_to_assign = role_name
                    break
            
            # Par défaut, attribuer le rôle Directeur aux premiers utilisateurs
            if not role_to_assign:
                if assigned_count == 0:
                    role_to_assign = "Directeur"
                elif assigned_count == 1:
                    role_to_assign = "Comptable"
                elif assigned_count == 2:
                    role_to_assign = "Secrétaire"
                elif assigned_count == 3:
                    role_to_assign = "Surveillant"
                else:
                    role_to_assign = "Surveillant"  # Rôle par défaut
            
            # Attribuer le rôle
            if rbac.assign_role_to_user(user_id, role_to_assign):
                print(f"✅ {username} → {role_to_assign}")
                assigned_count += 1
            else:
                print(f"❌ Échec attribution {username} → {role_to_assign}")
        
        conn.close()
        print(f"\n✅ {assigned_count} utilisateurs ont reçu un rôle")
        
    except Exception as e:
        print(f"❌ Erreur attribution rôles: {e}")

def create_test_users(rbac: RBACSystem):
    """Crée des utilisateurs de test avec différents rôles"""
    
    print("\n🧪 Création d'utilisateurs de test...")
    
    test_users = [
        {
            "username": "directeur",
            "password": "directeur123",
            "email": "directeur@ecole.com",
            "nom": "Directeur",
            "prenom": "Test",
            "roles": "Directeur"
        },
        {
            "username": "comptable",
            "password": "comptable123", 
            "email": "comptable@ecole.com",
            "nom": "Comptable",
            "prenom": "Test",
            "roles": "Comptable"
        },
        {
            "username": "secretaire",
            "password": "secretaire123",
            "email": "secretaire@ecole.com", 
            "nom": "Secrétaire",
            "prenom": "Test",
            "roles": "Secrétaire"
        },
        {
            "username": "surveillant",
            "password": "surveillant123",
            "email": "surveillant@ecole.com",
            "nom": "Surveillant", 
            "prenom": "Test",
            "roles": "Surveillant"
        }
    ]
    
    try:
        conn = sqlite3.connect(rbac.db_path)
        cursor = conn.cursor()
        
        created_count = 0
        for user_data in test_users:
            # Vérifier si l'utilisateurs existe déjà
            cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE nom_utilisateur = ?', 
                          (user_data["username"],))
            
            if cursor.fetchone():
                print(f"⚠️ Utilisateur {user_data['username']} existe déjà")
                continue
            
            # Créer l'utilisateurs
            cursor.execute('''
                INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, email, nom, prenom)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                user_data["username"],
                user_data["password"],  # En production, il faudrait hasher le mot de passe
                user_data["email"],
                user_data["nom"],
                user_data["prenom"]
            ))
            
            user_id = cursor.lastrowid
            
            # Attribuer le rôle
            if rbac.assign_role_to_user(user_id, user_data["roles"]):
                print(f"✅ Utilisateur {user_data['username']} créé avec rôle {user_data['roles']}")
                created_count += 1
            else:
                print(f"❌ Échec attribution rôle pour {user_data['username']}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ {created_count} utilisateurs de test créés")
        
    except Exception as e:
        print(f"❌ Erreur création utilisateurs de test: {e}")

def show_rbac_status(rbac: RBACSystem):
    """Affiche le statut du système RBAC"""
    
    print("\n📊 Statut du système RBAC:")
    
    # Rôles
    roles = rbac.get_all_roles()
    print(f"  • Rôles configurés: {len(roles)}")
    
    # Utilisateurs avec rôles
    try:
        conn = sqlite3.connect(rbac.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(DISTINCT ur.user_id) 
            FROM rbac_user_roles ur
        ''')
        users_with_roles = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM utilisateurs')
        total_users = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"  • Utilisateurs avec rôle: {users_with_roles}/{total_users}")
        
    except Exception as e:
        print(f"  • Erreur récupération statistiques: {e}")
    
    # Permissions par rôle
    print("\n🔐 Permissions par rôle:")
    for roles in roles:
        print(f"\n  {roles.name}:")
        print(f"    Description: {roles.description}")
        
        # Compter les permissions par niveau
        permission_counts = {}
        for view, level in roles.permissions.items():
            level_name = level.name
            permission_counts[level_name] = permission_counts.get(level_name, 0) + 1
        
        for level, count in permission_counts.items():
            print(f"    {level}: {count} vues")

def main():
    """Fonction principale"""
    
    print("🚀 Initialisation du système RBAC - EduManager+")
    print("=" * 50)
    
    # Configuration du système
    rbac = setup_rbac_system()
    if not rbac:
        print("❌ Impossible de configurer le système RBAC")
        return
    
    # Attribution des rôles aux utilisateurs existants
    assign_roles_to_users(rbac)
    
    # Création d'utilisateurs de test (optionnel)
    create_test = input("\n❓ Créer des utilisateurs de test ? (o/n): ").lower().strip()
    if create_test in ['o', 'oui', 'y', 'yes']:
        create_test_users(rbac)
    
    # Afficher le statut
    show_rbac_status(rbac)
    
    print("\n✅ Configuration RBAC terminée!")
    print("\n📝 Prochaines étapes:")
    print("  1. Redémarrer l'application EduManager+")
    print("  2. Se connecter avec un utilisateurs pour tester les permissions")
    print("  3. Vérifier que seules les vues autorisées apparaissent dans la sidebar")

if __name__ == "__main__":
    main()
