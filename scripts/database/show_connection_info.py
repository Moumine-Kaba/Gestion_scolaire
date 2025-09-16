#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour afficher toutes les informations de connexion organisées par rôles
Affiche les utilisateurs, leurs permissions et les détails de sécurité
"""

import sqlite3
import os
from datetime import datetime
from src.modules.role import RoleManager
from src.modules.permissions import PermissionManager
from src.modules.auth_enhanced import EnhancedAuthManager

def get_database_path():
    """Retourne le chemin de la base de données"""
    return "database/edumanager.db"

def check_database_exists():
    """Vérifie si la base de données existe"""
    db_path = get_database_path()
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    return True

def get_connection_info():
    """Récupère toutes les informations de connexion depuis la base de données"""
    db_path = get_database_path()
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les utilisateurs avec leurs rôles
        cursor.execute("""
            SELECT 
                u.id_utilisateur,
                u.username,
                u.email,
                u.nom_complet,
                u.date_creation,
                u.derniere_connexion,
                u.nombre_tentatives,
                u.compte_bloque,
                u.date_blocage,
                GROUP_CONCAT(r.nom_role) as roles
            FROM utilisateurs u
            LEFT JOIN user_roles ur ON u.id_utilisateur = ur.id_utilisateur
            LEFT JOIN roles r ON ur.id_role = r.id_role
            GROUP BY u.id_utilisateur
            ORDER BY u.username
        """)
        
        users = cursor.fetchall()
        
        # Récupérer les informations des rôles
        cursor.execute("""
            SELECT 
                r.id_role,
                r.nom_role,
                r.description,
                r.niveau_permission,
                r.date_creation
            FROM roles r
            ORDER BY r.niveau_permission DESC, r.nom_role
        """)
        
        roles = cursor.fetchall()
        
        # Récupérer les permissions des vues par rôle
        cursor.execute("""
            SELECT 
                r.nom_role,
                rvp.nom_vue,
                rvp.niveau_permission,
                rvp.date_creation
            FROM role_view_permissions rvp
            JOIN roles r ON rvp.id_role = r.id_role
            ORDER BY r.nom_role, rvp.nom_vue
        """)
        
        view_permissions = cursor.fetchall()
        
        # Récupérer les permissions des modules par rôle
        cursor.execute("""
            SELECT 
                r.nom_role,
                rmp.nom_module,
                rmp.permissions,
                rmp.date_creation
            FROM role_module_permissions rmp
            JOIN roles r ON rmp.id_role = r.id_role
            ORDER BY r.nom_role, rmp.nom_module
        """)
        
        module_permissions = cursor.fetchall()
        
        # Récupérer les tentatives de connexion récentes
        cursor.execute("""
            SELECT 
                la.username,
                la.ip_address,
                la.user_agent,
                la.success,
                la.failure_reason,
                la.timestamp,
                la.user_agent
            FROM login_attempts la
            ORDER BY la.timestamp DESC
            LIMIT 20
        """)
        
        login_attempts = cursor.fetchall()
        
        # Récupérer les sessions actives
        cursor.execute("""
            SELECT 
                s.token,
                s.id_utilisateur,
                u.username,
                s.ip_address,
                s.user_agent,
                s.date_creation,
                s.date_expiration,
                s.is_active
            FROM sessions s
            JOIN utilisateurs u ON s.id_utilisateur = u.id_utilisateur
            WHERE s.is_active = 1
            ORDER BY s.date_creation DESC
        """)
        
        active_sessions = cursor.fetchall()
        
        conn.close()
        
        return {
            'users': users,
            'roles': roles,
            'view_permissions': view_permissions,
            'module_permissions': module_permissions,
            'login_attempts': login_attempts,
            'active_sessions': active_sessions
        }
        
    except sqlite3.Error as e:
        print(f"❌ Erreur base de données: {e}")
        return None

def display_connection_info():
    """Affiche toutes les informations de connexion organisées par rôles"""
    print("🔐 INFORMATIONS DE CONNEXION PAR RÔLES")
    print("=" * 80)
    
    if not check_database_exists():
        return
    
    # Initialiser les gestionnaires
    try:
        role_manager = RoleManager()
        permission_manager = PermissionManager()
        auth_manager = EnhancedAuthManager()
        print("✅ Gestionnaires initialisés avec succès\n")
    except Exception as e:
        print(f"❌ Erreur initialisation gestionnaires: {e}")
        return
    
    # Récupérer les informations
    info = get_connection_info()
    if not info:
        return
    
    # 1. AFFICHER LES RÔLES DISPONIBLES
    print("📋 RÔLES DISPONIBLES")
    print("-" * 40)
    for role in info['roles']:
        role_id, nom_role, description, niveau, date_creation = role
        date_creation = datetime.fromisoformat(date_creation) if date_creation else "N/A"
        print(f"🔹 {nom_role} (Niveau {niveau})")
        print(f"   Description: {description}")
        print(f"   Créé le: {date_creation}")
        print()
    
    # 2. AFFICHER LES UTILISATEURS PAR RÔLE
    print("👥 UTILISATEURS PAR RÔLE")
    print("-" * 40)
    
    # Organiser les utilisateurs par rôle
    users_by_role = {}
    for user in info['users']:
        user_id, username, email, nom_complet, date_creation, derniere_connexion, tentatives, bloque, date_blocage, roles = user
        
        if not roles:
            roles = "Aucun rôle"
        
        for role in roles.split(','):
            if role not in users_by_role:
                users_by_role[role] = []
            
            users_by_role[role].append({
                'username': username,
                'email': email,
                'nom_complet': nom_complet,
                'date_creation': date_creation,
                'derniere_connexion': derniere_connexion,
                'tentatives': tentatives,
                'bloque': bloque,
                'date_blocage': date_blocage
            })
    
    for role, users in users_by_role.items():
        print(f"🎭 RÔLE: {role}")
        print(f"   Nombre d'utilisateurs: {len(users)}")
        print()
        
        for user in users:
            print(f"   👤 {user['username']}")
            print(f"      Nom complet: {user['nom_complet']}")
            print(f"      Email: {user['email']}")
            print(f"      Créé le: {user['date_creation']}")
            print(f"      Dernière connexion: {user['derniere_connexion']}")
            print(f"      Tentatives échouées: {user['tentatives'] or 0}")
            print(f"      Compte bloqué: {'Oui' if user['bloque'] else 'Non'}")
            if user['date_blocage']:
                print(f"      Date de blocage: {user['date_blocage']}")
            print()
    
    # 3. AFFICHER LES PERMISSIONS DES VUES PAR RÔLE
    print("🔐 PERMISSIONS DES VUES PAR RÔLE")
    print("-" * 40)
    
    permissions_by_role = {}
    for perm in info['view_permissions']:
        role, vue, niveau, date = perm
        if role not in permissions_by_role:
            permissions_by_role[role] = []
        permissions_by_role[role].append((vue, niveau))
    
    for role, permissions in permissions_by_role.items():
        print(f"🎭 {role}:")
        for vue, niveau in permissions:
            print(f"   📱 {vue}: {niveau}")
        print()
    
    # 4. AFFICHER LES PERMISSIONS DES MODULES PAR RÔLE
    print("⚙️ PERMISSIONS DES MODULES PAR RÔLE")
    print("-" * 40)
    
    module_perms_by_role = {}
    for perm in info['module_permissions']:
        role, module, permissions, date = perm
        if role not in module_perms_by_role:
            module_perms_by_role[role] = []
        module_perms_by_role[role].append((module, permissions))
    
    for role, permissions in module_perms_by_role.items():
        print(f"🎭 {role}:")
        for module, perms in permissions:
            print(f"   🗂️ {module}: {perms}")
        print()
    
    # 5. AFFICHER LES TENTATIVES DE CONNEXION RÉCENTES
    print("📊 TENTATIVES DE CONNEXION RÉCENTES")
    print("-" * 40)
    
    if info['login_attempts']:
        for attempt in info['login_attempts'][:10]:  # Limiter à 10
            username, ip, user_agent, success, failure_reason, timestamp, ua = attempt
            status = "✅ Succès" if success else "❌ Échec"
            timestamp = datetime.fromisoformat(timestamp) if timestamp else "N/A"
            print(f"👤 {username} - {status}")
            print(f"   IP: {ip}")
            print(f"   Raison échec: {failure_reason or 'N/A'}")
            print(f"   Date: {timestamp}")
            print()
    else:
        print("Aucune tentative de connexion enregistrée")
    
    # 6. AFFICHER LES SESSIONS ACTIVES
    print("🔄 SESSIONS ACTIVES")
    print("-" * 40)
    
    if info['active_sessions']:
        for session in info['active_sessions']:
            token, user_id, username, ip, user_agent, creation, expiration, active = session
            creation = datetime.fromisoformat(creation) if creation else "N/A"
            expiration = datetime.fromisoformat(expiration) if expiration else "N/A"
            print(f"🔑 Session pour {username}")
            print(f"   IP: {ip}")
            print(f"   Créée le: {creation}")
            print(f"   Expire le: {expiration}")
            print(f"   Active: {'Oui' if active else 'Non'}")
            print()
    else:
        print("Aucune session active")
    
    # 7. AFFICHER LES COMPTES DE DÉMONSTRATION
    print("🧪 COMPTES DE DÉMONSTRATION")
    print("-" * 40)
    print("Ces comptes sont pré-configurés pour tester les différents rôles:")
    print()
    
    demo_accounts = [
        ("admin", "admin123", "Super Admin", "Accès complet"),
        ("directeur", "directeur123", "Directeur", "Gestion étendue"),
        ("professeur", "prof123", "Professeur", "Modules pédagogiques"),
        ("secretaire", "sec123", "Secrétaire", "Modules administratifs"),
        ("eleve", "eleve123", "Élève", "Consultation uniquement")
    ]
    
    for username, password, role, description in demo_accounts:
        print(f"👤 {username} / {password}")
        print(f"   Rôle: {role}")
        print(f"   Description: {description}")
        print()
    
    print("=" * 80)
    print("✅ Affichage terminé ! Utilisez ces informations pour tester les différents rôles.")

def main():
    """Fonction principale"""
    try:
        display_connection_info()
    except KeyboardInterrupt:
        print("\n\n⏹️ Affichage interrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    main()

