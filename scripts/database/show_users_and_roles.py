#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Affichage des utilisateurs et leurs rôles
EduManager+ - Gestion Scolaire
"""

import os
import sys
import sqlite3
from datetime import datetime

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def show_all_users():
    """Affiche tous les utilisateurs avec leurs rôles"""
    print("👥 Liste complète des utilisateurs et leurs rôles")
    print("=" * 80)
    
    try:
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les utilisateurs avec leurs rôles
        cursor.execute("""
            SELECT 
                u.id_utilisateur,
                u.username,
                u.email,
                u.nom,
                u.prenom,
                u.date_creation,
                r.nom_role,
                r.niveau_acces,
                r.description
            FROM utilisateurs u
            LEFT JOIN user_roles ur ON u.id_utilisateur = ur.user_id
            LEFT JOIN roles r ON ur.role_id = r.id_role
            ORDER BY r.niveau_acces DESC, u.nom, u.prenom
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("❌ Aucun utilisateur trouvé dans la base de données")
            return
        
        # Afficher le tableau des utilisateurs
        print(f"{'ID':<4} {'Username':<20} {'Nom':<15} {'Prénom':<15} {'Rôle':<25} {'Niveau':<8}")
        print("-" * 80)
        
        for user in users:
            user_id, username, email, nom, prenom, date_creation, role, niveau, description = user
            
            # Formater le rôle (peut être None si pas de rôle assigné)
            role_display = role if role else "Aucun rôle"
            niveau_display = str(niveau) if niveau else "-"
            
            print(f"{user_id:<4} {username:<20} {nom:<15} {prenom:<15} {role_display:<25} {niveau_display:<8}")
        
        print("-" * 80)
        print(f"Total: {len(users)} utilisateur(s)")
        
        # Statistiques par rôle
        print(f"\n📊 Statistiques par rôle:")
        print("-" * 50)
        
        cursor.execute("""
            SELECT 
                r.nom_role,
                COUNT(u.id_utilisateur) as nb_users,
                r.niveau_acces,
                r.description
            FROM roles r
            LEFT JOIN user_roles ur ON r.id_role = ur.role_id
            LEFT JOIN utilisateurs u ON ur.user_id = u.id_utilisateur
            GROUP BY r.id_role, r.nom_role, r.niveau_acces, r.description
            ORDER BY r.niveau_acces DESC
        """)
        
        role_stats = cursor.fetchall()
        
        for role_stat in role_stats:
            role_name, nb_users, niveau, description = role_stat
            print(f"  - {role_name:<25} : {nb_users:>2} utilisateur(s) (Niveau {niveau})")
            if description:
                print(f"    {description}")
        
        # Utilisateurs sans rôle
        cursor.execute("""
            SELECT COUNT(*) 
            FROM utilisateurs u 
            LEFT JOIN user_roles ur ON u.id_utilisateur = ur.user_id 
            WHERE ur.user_id IS NULL
        """)
        
        users_without_role = cursor.fetchone()[0]
        if users_without_role > 0:
            print(f"\n⚠️  {users_without_role} utilisateur(s) sans rôle assigné")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des utilisateurs: {e}")

def show_user_details(username=None):
    """Affiche les détails d'un utilisateur spécifique"""
    if not username:
        username = input("Entrez le username de l'utilisateur à afficher: ").strip()
    
    print(f"\n🔍 Détails de l'utilisateur: {username}")
    print("=" * 60)
    
    try:
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer les détails de l'utilisateur
        cursor.execute("""
            SELECT 
                u.id_utilisateur,
                u.username,
                u.email,
                u.nom,
                u.prenom,
                u.date_creation,
                r.nom_role,
                r.niveau_acces,
                r.description
            FROM utilisateurs u
            LEFT JOIN user_roles ur ON u.id_utilisateur = ur.user_id
            LEFT JOIN roles r ON ur.role_id = r.id_role
            WHERE u.username = ?
        """, (username,))
        
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Utilisateur '{username}' non trouvé")
            return
        
        user_id, username, email, nom, prenom, date_creation, role, niveau, description = user
        
        print(f"📋 Informations personnelles:")
        print(f"  - ID: {user_id}")
        print(f"  - Username: {username}")
        print(f"  - Email: {email}")
        print(f"  - Nom: {nom}")
        print(f"  - Prénom: {prenom}")
        print(f"  - Date de création: {date_creation}")
        
        print(f"\n🔐 Rôle et permissions:")
        if role:
            print(f"  - Rôle: {role}")
            print(f"  - Niveau d'accès: {niveau}")
            print(f"  - Description: {description}")
        else:
            print(f"  - Aucun rôle assigné")
        
        # Vérifier les permissions si un rôle est assigné
        if role:
            print(f"\n✅ Permissions disponibles:")
            try:
                from src.modules.permission_manager import PermissionManager
                perm_manager = PermissionManager("database/edumanager.db")
                
                # Récupérer les permissions de l'utilisateur
                permissions = perm_manager.get_user_permissions(user_id)
                if permissions:
                    print(f"  - Vues accessibles: {', '.join(sorted(permissions))}")
                else:
                    print(f"  - Aucune vue accessible")
                
                # Récupérer les restrictions
                restrictions = perm_manager.get_restricted_views(user_id)
                if restrictions:
                    print(f"\n🚫 Restrictions appliquées:")
                    for view, actions in restrictions.items():
                        print(f"  - {view}: {', '.join(actions)}")
                else:
                    print(f"\n✅ Aucune restriction appliquée")
                    
            except ImportError:
                print(f"  - Impossible de charger le gestionnaire de permissions")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage des détails: {e}")

def show_role_hierarchy():
    """Affiche la hiérarchie des rôles"""
    print(f"\n🔐 Hiérarchie des rôles par niveau d'accès")
    print("=" * 60)
    
    try:
        db_path = "database/edumanager.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                r.nom_role,
                r.niveau_acces,
                r.description,
                COUNT(u.id_utilisateur) as nb_users
            FROM roles r
            LEFT JOIN user_roles ur ON r.id_role = ur.role_id
            LEFT JOIN utilisateurs u ON ur.user_id = u.id_utilisateur
            GROUP BY r.id_role, r.nom_role, r.niveau_acces, r.description
            ORDER BY r.niveau_acces DESC
        """)
        
        roles = cursor.fetchall()
        
        print(f"{'Niveau':<8} {'Rôle':<30} {'Utilisateurs':<12} {'Description'}")
        print("-" * 60)
        
        for role in roles:
            nom_role, niveau, description, nb_users = role
            description_short = description[:40] + "..." if len(description) > 40 else description
            print(f"{niveau:<8} {nom_role:<30} {nb_users:<12} {description_short}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'affichage de la hiérarchie: {e}")

def main():
    """Menu principal"""
    while True:
        print(f"\n🎯 Menu d'affichage des utilisateurs et rôles")
        print("=" * 50)
        print(f"1. Afficher tous les utilisateurs")
        print(f"2. Détails d'un utilisateur spécifique")
        print(f"3. Hiérarchie des rôles")
        print(f"4. Quitter")
        
        choice = input(f"\nChoisissez une option (1-4): ").strip()
        
        if choice == "1":
            show_all_users()
        elif choice == "2":
            show_user_details()
        elif choice == "3":
            show_role_hierarchy()
        elif choice == "4":
            print(f"👋 Au revoir!")
            break
        else:
            print(f"❌ Option invalide. Veuillez choisir 1, 2, 3 ou 4.")

if __name__ == "__main__":
    print("🚀 Script d'affichage des utilisateurs et rôles")
    print("=" * 60)
    
    # Afficher directement tous les utilisateurs
    show_all_users()
    
    # Puis proposer le menu interactif
    print(f"\n" + "="*60)
    main()

