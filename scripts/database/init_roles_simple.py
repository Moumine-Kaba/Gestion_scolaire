#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation Simplifiée des Rôles et Permissions
EduManager+ - Gestion Scolaire
"""

import sqlite3
import os

def init_roles_simple():
    """Initialise les rôles et permissions de manière simplifiée"""
    print("🚀 Initialisation simplifiée des rôles et permissions")
    print("=" * 50)
    
    db_path = "database/edumanager.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("1️⃣ Vérification des tables existantes...")
        
        # Vérifier si la table roles existe et sa structure
        cursor.execute('PRAGMA table_info(roles)')
        columns = [col[1] for col in cursor.fetchall()]
        print(f"  Colonnes de la table roles: {columns}")
        
        # Ajouter la colonne niveau si elle n'existe pas
        if 'niveau' not in columns:
            print("  Ajout de la colonne 'niveau'...")
            cursor.execute('ALTER TABLE roles ADD COLUMN niveau INTEGER DEFAULT 1')
            print("  ✅ Colonne 'niveau' ajoutée")
        
        print("\n2️⃣ Insertion des rôles par défaut...")
        
        # Rôles par défaut
        default_roles = [
            (1, "Super Administrateur", "Accès complet à tous les modules", 10, "read,write,delete,admin"),
            (2, "Administrateur", "Gestion complète de l'établissement", 9, "read,write,delete"),
            (3, "Directeur", "Gestion des classes, élèves et professeurs", 8, "read,write"),
            (4, "Professeur", "Gestion des notes, présences et bulletins", 7, "read,write"),
            (5, "Secrétaire", "Gestion administrative et inscriptions", 6, "read,write"),
            (6, "Élève", "Consultation des notes et bulletins", 5, "read"),
            (7, "Parent", "Consultation des informations de l'élève", 4, "read")
        ]
        
        for role_id, nom, description, niveau, permissions in default_roles:
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO roles (id_role, nom, description, niveau, permissions)
                    VALUES (?, ?, ?, ?, ?)
                ''', (role_id, nom, description, niveau, permissions))
                print(f"  ✅ Rôle '{nom}' créé/actualisé")
            except Exception as e:
                print(f"  ❌ Erreur création rôle '{nom}': {e}")
        
        print("\n3️⃣ Vérification de l'utilisateur admin...")
        
        # Vérifier si l'utilisateur admin existe
        cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE username = ?', ('admin',))
        admin_user = cursor.fetchone()
        
        if admin_user:
            admin_id = admin_user[0]
            print(f"  ✅ Utilisateur admin trouvé (ID: {admin_id})")
            
            # Vérifier si le rôle est déjà assigné
            cursor.execute('SELECT id FROM user_roles WHERE user_id = ? AND role_id = 1', (admin_id,))
            if not cursor.fetchone():
                cursor.execute('INSERT INTO user_roles (user_id, role_id, assigned_by) VALUES (?, 1, ?)', (admin_id, admin_id))
                print(f"  ✅ Rôle Super Administrateur assigné à admin")
            else:
                print(f"  ℹ️ Rôle Super Administrateur déjà assigné à admin")
        else:
            print("  ⚠️ Utilisateur admin non trouvé")
        
        print("\n4️⃣ Création des tables de permissions...")
        
        # Table de contrôle d'accès aux vues
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
        print("  ✅ Table user_view_access créée")
        
        # Table des vues disponibles
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
        print("  ✅ Table available_views créée")
        
        print("\n5️⃣ Insertion des vues disponibles...")
        
        # Vues par défaut
        default_views = [
            ("dashboard", "Tableau de bord", "Vue principale", "SCOLARITÉ"),
            ("eleves", "Élèves", "Gestion des élèves", "SCOLARITÉ"),
            ("profs", "Professeurs", "Gestion des professeurs", "SCOLARITÉ"),
            ("classes", "Classes", "Gestion des classes", "SCOLARITÉ"),
            ("salles", "Salles", "Gestion des salles", "SCOLARITÉ"),
            ("notes", "Notes", "Gestion des notes", "PÉDAGOGIE"),
            ("presences", "Présences", "Gestion des présences", "PÉDAGOGIE"),
            ("bulletins", "Bulletins", "Gestion des bulletins", "PÉDAGOGIE"),
            ("paiements", "Paiements", "Gestion des paiements", "FINANCES"),
            ("utilisateurs", "Utilisateurs", "Gestion des utilisateurs", "ADMINISTRATION")
        ]
        
        for view_name, view_title, view_description, module in default_views:
            cursor.execute('''
                INSERT OR IGNORE INTO available_views (view_name, view_title, view_description, module)
                VALUES (?, ?, ?, ?)
            ''', (view_name, view_title, view_description, module))
        
        print(f"  ✅ {len(default_views)} vues insérées")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 Initialisation terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = init_roles_simple()
    if success:
        print("\n✅ Le système de permissions est maintenant initialisé!")
    else:
        print("\n❌ L'initialisation a échoué.")

