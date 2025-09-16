#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation des Rôles et Permissions
EduManager+ - Gestion Scolaire
"""

import sys
import os
import sqlite3

# Ajouter le répertoire parent au path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
if project_root not in sys.path:
    sys.path.append(project_root)

def init_roles_and_permissions():
    """Initialise les rôles et permissions dans la base de données"""
    print("🚀 Initialisation des rôles et permissions")
    print("=" * 50)
    
    db_path = "database/edumanager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier et adapter la table des rôles si nécessaire
        print("\n1️⃣ Vérification de la table des rôles...")
        
        # Vérifier si la colonne niveau existe
        cursor.execute('PRAGMA table_info(roles)')
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'niveau' not in columns:
            print("  ℹ️ Ajout de la colonne 'niveau' à la table roles...")
            try:
                cursor.execute('ALTER TABLE roles ADD COLUMN niveau INTEGER DEFAULT 1')
                print("  ✅ Colonne 'niveau' ajoutée")
            except Exception as e:
                print(f"  ⚠️ Impossible d'ajouter la colonne niveau: {e}")
                print("  ℹ️ Utilisation de la structure existante")
        
        # Créer la table si elle n'existe pas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS roles (
                id_role INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                description TEXT,
                permissions TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 2. Créer la table des rôles utilisateur si elle n'existe pas
        print("2️⃣ Création de la table des rôles utilisateur...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assigned_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                FOREIGN KEY (role_id) REFERENCES roles (id_role),
                FOREIGN KEY (assigned_by) REFERENCES utilisateurs (id_utilisateur),
                UNIQUE(user_id, role_id)
            )
        ''')
        
        # 3. Insérer les rôles par défaut
        print("3️⃣ Insertion des rôles par défaut...")
        default_roles = [
            (1, "Super Administrateur", "Accès complet à tous les modules et fonctionnalités", 10, "read,write,delete,admin"),
            (2, "Administrateur", "Gestion complète de l'établissement", 9, "read,write,delete"),
            (3, "Directeur", "Gestion des classes, élèves et professeurs", 8, "read,write"),
            (4, "Professeur", "Gestion des notes, présences et bulletins", 7, "read,write"),
            (5, "Secrétaire", "Gestion administrative et inscriptions", 6, "read,write"),
            (6, "Élève", "Consultation des notes et bulletins", 5, "read"),
            (7, "Parent", "Consultation des informations de l'élève", 4, "read")
        ]
        
        for role_id, nom, description, niveau, permissions in default_roles:
            try:
                # Essayer d'insérer avec la colonne niveau
                cursor.execute('''
                    INSERT OR REPLACE INTO roles (id_role, nom, description, niveau, permissions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (role_id, nom, description, niveau, permissions))
                print(f"  ✅ Rôle '{nom}' créé/actualisé avec niveau")
            except Exception:
                # Fallback sans la colonne niveau
                cursor.execute('''
                    INSERT OR REPLACE INTO roles (id_role, nom, description, permissions)
                    VALUES (?, ?, ?, ?)
                ''', (role_id, nom, description, permissions))
                print(f"  ✅ Rôle '{nom}' créé/actualisé (sans niveau)")
        
        # 4. Assigner le rôle Super Administrateur à l'utilisateur admin
        print("4️⃣ Attribution du rôle Super Administrateur à l'utilisateur admin...")
        
        # Vérifier si l'utilisateur admin existe
        cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE username = ?', ('admin',))
        admin_user = cursor.fetchone()
        
        if admin_user:
            admin_id = admin_user[0]
            
            # Vérifier si le rôle est déjà assigné
            cursor.execute('''
                SELECT id FROM user_roles 
                WHERE user_id = ? AND role_id = 1
            ''', (admin_id,))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO user_roles (user_id, role_id, assigned_by)
                    VALUES (?, 1, ?)
                ''', (admin_id, admin_id))
                print(f"  ✅ Rôle Super Administrateur assigné à l'utilisateur admin (ID: {admin_id})")
            else:
                print(f"  ℹ️ Rôle Super Administrateur déjà assigné à l'utilisateur admin")
        else:
            print("  ⚠️ Utilisateur admin non trouvé")
        
        # 5. Créer des utilisateurs de test avec différents rôles
        print("5️⃣ Création d'utilisateurs de test...")
        
        test_users = [
            ("directeur", "directeur123", "Directeur", "Test", "Directeur"),
            ("professeur", "prof123", "Professeur", "Test", "Professeur"),
            ("secretaire", "sec123", "Secrétaire", "Test", "Secrétaire"),
            ("eleve", "eleve123", "Élève", "Test", "Élève")
        ]
        
        for username, password, nom, prenom, role_name in test_users:
            # Vérifier si l'utilisateur existe déjà
            cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE username = ?', (username,))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                # Créer l'utilisateur
                cursor.execute('''
                    INSERT INTO utilisateurs (username, password_hash, salt, nom, prenom, statut)
                    VALUES (?, ?, ?, ?, ?, 'actif')
                ''', (username, password, "salt", nom, prenom))
                
                user_id = cursor.lastrowid
                
                # Assigner le rôle correspondant
                role_id_map = {
                    "Directeur": 3,
                    "Professeur": 4,
                    "Secrétaire": 5,
                    "Élève": 6
                }
                
                role_id = role_id_map.get(role_name)
                if role_id:
                    cursor.execute('''
                        INSERT INTO user_roles (user_id, role_id, assigned_by)
                        VALUES (?, ?, ?)
                    ''', (user_id, role_id, admin_id if admin_user else 1))
                    print(f"  ✅ Utilisateur '{username}' créé avec le rôle '{role_name}'")
                else:
                    print(f"  ⚠️ Rôle '{role_name}' non trouvé pour l'utilisateur '{username}'")
            else:
                print(f"  ℹ️ Utilisateur '{username}' existe déjà")
        
        # 6. Créer la table de contrôle d'accès aux vues
        print("6️⃣ Création de la table de contrôle d'accès aux vues...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_view_access (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                view_name TEXT NOT NULL,
                access_level TEXT DEFAULT 'read',
                granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                granted_by INTEGER,
                FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                FOREIGN KEY (granted_by) REFERENCES utilisateurs (id_utilisateur),
                UNIQUE(user_id, view_name)
            )
        ''')
        
        # 7. Créer la table des vues disponibles
        print("7️⃣ Création de la table des vues disponibles...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS available_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                view_name TEXT UNIQUE NOT NULL,
                view_title TEXT NOT NULL,
                view_description TEXT,
                module TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insérer les vues disponibles
        default_views = [
            ("dashboard", "Tableau de bord", "Vue principale de l'application", "SCOLARITÉ"),
            ("eleves", "Élèves", "Gestion des élèves", "SCOLARITÉ"),
            ("profs", "Professeurs", "Gestion des professeurs", "SCOLARITÉ"),
            ("classes", "Classes", "Gestion des classes", "SCOLARITÉ"),
            ("salles", "Salles", "Gestion des salles", "SCOLARITÉ"),
            ("enseignements", "Enseignements", "Gestion des enseignements", "PÉDAGOGIE"),
            ("matieres", "Matières", "Gestion des matières", "PÉDAGOGIE"),
            ("notes", "Notes", "Gestion des notes", "PÉDAGOGIE"),
            ("presences", "Présences", "Gestion des présences", "PÉDAGOGIE"),
            ("bulletins", "Bulletins", "Gestion des bulletins", "PÉDAGOGIE"),
            ("emplois", "Emplois du temps", "Gestion des emplois du temps", "PÉDAGOGIE"),
            ("paiements", "Paiements", "Gestion des paiements", "FINANCES"),
            ("utilisateurs", "Utilisateurs", "Gestion des utilisateurs", "ADMINISTRATION"),
            ("actualites", "Actualités", "Gestion des actualités", "ADMINISTRATION"),
            ("annonces", "Annonces", "Gestion des annonces", "ADMINISTRATION"),
            ("notifications", "Notifications", "Gestion des notifications", "ADMINISTRATION"),
            ("taches", "Tâches", "Gestion des tâches", "ADMINISTRATION"),
            ("biblio", "Bibliothèque", "Gestion de la bibliothèque", "OUTILS"),
            ("calendriers", "Calendriers", "Gestion des calendriers", "OUTILS"),
            ("carrieres", "Carrières", "Gestion des carrières", "OUTILS"),
            ("competences", "Compétences", "Gestion des compétences", "OUTILS"),
            ("documents", "Documents", "Gestion des documents", "OUTILS"),
            ("maintenances", "Maintenance", "Gestion de la maintenance", "OUTILS"),
            ("messagerie", "Messagerie", "Gestion de la messagerie", "OUTILS"),
            ("objectifs", "Objectifs", "Gestion des objectifs", "OUTILS"),
            ("personnel", "Personnel", "Gestion du personnel", "OUTILS"),
            ("transfert", "Transfert", "Gestion des transferts", "OUTILS"),
            ("settings", "Paramètres", "Paramètres du système", "OUTILS")
        ]
        
        for view_name, view_title, view_description, module in default_views:
            cursor.execute('''
                INSERT OR IGNORE INTO available_views (view_name, view_title, view_description, module)
                VALUES (?, ?, ?, ?)
            ''', (view_name, view_title, view_description, module))
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Initialisation terminée avec succès!")
        print("\n📋 Récapitulatif:")
        print("  • Rôles créés: 7 rôles par défaut")
        print("  • Utilisateur admin: rôle Super Administrateur")
        print("  • Utilisateurs de test créés avec leurs rôles respectifs")
        print("  • Tables de permissions initialisées")
        print("\n🔑 Comptes de test:")
        print("  • directeur / directeur123 (rôle Directeur)")
        print("  • professeur / prof123 (rôle Professeur)")
        print("  • secretaire / sec123 (rôle Secrétaire)")
        print("  • eleve / eleve123 (rôle Élève)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_roles_and_permissions()
    if success:
        print("\n✅ L'application est maintenant prête avec le système de permissions!")
        print("   Vous pouvez vous connecter avec différents comptes pour tester les restrictions d'accès.")
    else:
        print("\n❌ L'initialisation a échoué. Vérifiez les erreurs ci-dessus.")
