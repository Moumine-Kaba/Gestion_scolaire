#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test du système de permissions avancé
EduManager+ - Gestion Scolaire
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta

# Ajouter le chemin du projet
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def test_permission_system():
    """Test du système de permissions avancé"""
    print("🧪 Test du système de permissions avancé")
    print("=" * 50)
    
    try:
        # Importer le gestionnaire de permissions
        from models.permission_manager import PermissionManager
        
        # Initialiser le gestionnaire
        db_path = "database/edumanager.db"
        perm_manager = PermissionManager(db_path)
        
        print("✅ Gestionnaire de permissions initialisé")
        
        # Test 1: Vérifier les rôles créés
        print("\n📋 Test 1: Vérification des rôles")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT nom_role, description, niveau_acces FROM roles ORDER BY niveau_acces DESC")
        roles = cursor.fetchall()
        
        print(f"Nombre de rôles créés: {len(roles)}")
        for role in roles:
            print(f"  - {role[0]} (Niveau: {role[1]}) - {role[2]}")
        
        # Test 2: Vérifier les permissions
        print("\n🔐 Test 2: Vérification des permissions")
        cursor.execute("""
            SELECT r.nom_role, COUNT(rp.vue_nom) as nb_permissions
            FROM roles r
            LEFT JOIN role_permissions rp ON r.id_role = rp.role_id
            GROUP BY r.id_role, r.nom_role
            ORDER BY r.niveau_acces DESC
        """)
        
        permissions = cursor.fetchall()
        for perm in permissions:
            print(f"  - {perm[0]}: {perm[1]} permissions")
        
        # Test 3: Simuler un utilisateur avec différents rôles
        print("\n👤 Test 3: Simulation d'utilisateurs")
        
        # Créer un utilisateur de test
        cursor.execute("""
            INSERT OR IGNORE INTO utilisateurs (username, email, mot_de_passe, nom, prenom)
            VALUES (?, ?, ?, ?, ?)
        """, ("test_prof", "prof@test.com", "hash123", "Dupont", "Jean"))
        
        cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE username = ?", ("test_prof",))
        user_id = cursor.fetchone()[0]
        
        # Assigner le rôle Professeur
        perm_manager.assign_role_to_user(user_id, "Professeur")
        
        # Tester les permissions
        print(f"\nUtilisateur test créé (ID: {user_id}) avec le rôle Professeur")
        
        # Vérifier les permissions sur différentes vues
        test_views = ["dashboard", "eleves", "notes", "paiements", "utilisateurs", "settings"]
        
        for view in test_views:
            can_access = perm_manager.can_access_view(user_id, view)
            permission_level = perm_manager.get_user_permission_level(user_id, view)
            print(f"  - {view}: Accès: {can_access}, Niveau: {permission_level}")
        
        # Test 4: Vérifier les restrictions
        print("\n🚫 Test 4: Vérification des restrictions")
        restrictions = perm_manager.get_restricted_views(user_id)
        print(f"Restrictions pour le Professeur:")
        for view, actions in restrictions.items():
            print(f"  - {view}: {', '.join(actions)}")
        
        # Test 5: Vérifier les actions autorisées
        print("\n✅ Test 5: Vérification des actions autorisées")
        test_actions = ["view", "create", "update", "delete", "export"]
        
        for view in ["notes", "eleves", "paiements"]:
            print(f"\nActions autorisées sur {view}:")
            for action in test_actions:
                can_do = perm_manager.can_perform_action(user_id, view, action)
                print(f"  - {action}: {'✅' if can_do else '❌'}")
        
        # Test 6: Créer un élève et tester ses restrictions
        print("\n🎓 Test 6: Test des restrictions pour un élève")
        
        cursor.execute("""
            INSERT OR IGNORE INTO utilisateurs (username, email, mot_de_passe, nom, prenom)
            VALUES (?, ?, ?, ?, ?)
        """, ("test_eleve", "eleve@test.com", "hash123", "Martin", "Pierre"))
        
        cursor.execute("SELECT id_utilisateur FROM utilisateurs WHERE username = ?", ("test_eleve",))
        eleve_id = cursor.fetchone()[0]
        
        # Assigner le rôle Élève
        perm_manager.assign_role_to_user(eleve_id, "Élève")
        
        print(f"Élève créé (ID: {eleve_id})")
        
        # Tester les restrictions
        eleve_restrictions = perm_manager.get_restricted_views(eleve_id)
        print(f"Restrictions pour l'Élève:")
        for view, actions in eleve_restrictions.items():
            print(f"  - {view}: {', '.join(actions)}")
        
        # Test 7: Vérifier l'accès aux données
        print("\n🔍 Test 7: Vérification de l'accès aux données")
        
        for view in ["eleves", "notes", "paiements", "utilisateurs"]:
            can_access_data = perm_manager.check_data_access(eleve_id, view)
            print(f"  - Accès aux données {view}: {'✅' if can_access_data else '❌'}")
        
        # Test 8: Logs d'audit
        print("\n📝 Test 8: Test des logs d'audit")
        
        # Simuler quelques tentatives d'accès
        perm_manager.log_access_attempt(user_id, "notes", "view", True)
        perm_manager.log_access_attempt(user_id, "paiements", "view", False)
        perm_manager.log_access_attempt(eleve_id, "notes", "view", True)
        
        print("Logs d'audit créés")
        
        # Récupérer les logs
        user_logs = perm_manager.get_user_audit_logs(user_id, 10)
        print(f"Logs pour l'utilisateur {user_id}: {len(user_logs)} entrées")
        
        # Nettoyer les données de test
        print("\n🧹 Nettoyage des données de test")
        cursor.execute("DELETE FROM user_roles WHERE user_id IN (?, ?)", (user_id, eleve_id))
        cursor.execute("DELETE FROM access_logs WHERE user_id IN (?, ?)", (user_id, eleve_id))
        cursor.execute("DELETE FROM utilisateurs WHERE id_utilisateur IN (?, ?)", (user_id, eleve_id))
        
        conn.commit()
        conn.close()
        
        print("✅ Tests terminés avec succès!")
        
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

def test_security_features():
    """Test des fonctionnalités de sécurité"""
    print("\n🔒 Test des fonctionnalités de sécurité")
    print("=" * 50)
    
    try:
        from models.permission_manager import PermissionManager
        
        db_path = "database/edumanager.db"
        perm_manager = PermissionManager(db_path)
        
        # Test de la hiérarchie des rôles
        print("\n📊 Test de la hiérarchie des rôles")
        
        roles_hierarchy = [
            "Super Administrateur",
            "Administrateur", 
            "Directeur Général",
            "Directeur Pédagogique",
            "Proviseur",
            "Censeur",
            "Surveillant Général",
            "Professeur Principal",
            "Professeur",
            "Comptable Principal",
            "Comptable",
            "Secrétaire Principal",
            "Secrétaire",
            "Élève",
            "Parent",
            "Visiteur"
        ]
        
        for role in roles_hierarchy:
            level = perm_manager._get_role_level(role)
            print(f"  - {role}: Niveau {level}")
        
        print("\n✅ Tests de sécurité terminés!")
        
    except Exception as e:
        print(f"❌ Erreur lors des tests de sécurité: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage des tests du système de permissions")
    print("=" * 60)
    
    # Test principal
    test_permission_system()
    
    # Test des fonctionnalités de sécurité
    test_security_features()
    
    print("\n🎉 Tous les tests sont terminés!")

