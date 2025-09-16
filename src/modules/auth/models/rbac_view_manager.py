#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Vues RBAC pour EduManager+
==========================================

Gère l'accès aux vues selon les rôles et permissions des utilisateurs.
"""

import sqlite3
import os
from typing import Dict, List, Optional, Set
from datetime import datetime

class RBACViewManager:
    """Gestionnaire de contrôle d'accès aux vues"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.current_user_id = None
        self.current_user_role = None
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les tables de vues
        self._init_view_tables()
        
        # Créer les permissions de vues par défaut
        self._create_default_view_permissions()
    
    def _init_view_tables(self):
        """Initialise les tables de gestion des vues"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Table des vues disponibles
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS views (
                    id_view INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_view TEXT UNIQUE NOT NULL,
                    titre_view TEXT NOT NULL,
                    description TEXT,
                    module TEXT,
                    icon TEXT,
                    order_index INTEGER DEFAULT 0,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Table des permissions de vues par rôle
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS role_view_permissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role_id INTEGER NOT NULL,
                    view_id INTEGER NOT NULL,
                    can_read BOOLEAN DEFAULT 0,
                    can_write BOOLEAN DEFAULT 0,
                    can_delete BOOLEAN DEFAULT 0,
                    granted BOOLEAN DEFAULT 1,
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    FOREIGN KEY (view_id) REFERENCES views (id_view),
                    UNIQUE(role_id, view_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tables de vues RBAC initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation tables vues: {e}")
    
    def _create_default_view_permissions(self):
        """Crée les permissions de vues par défaut"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vues par défaut avec leurs permissions par rôle
            default_views = [
                ("dashboard", "Dashboard", "Tableau de bord principal", "auth", "home.png", 0),
                ("eleves", "Élèves", "Gestion des élèves", "academic", "eleve.png", 1),
                ("professeurs", "Professeurs", "Gestion des professeurs", "academic", "person.png", 2),
                ("classes", "Classes", "Gestion des classes", "academic", "class.png", 3),
                ("salles", "Salles", "Gestion des salles", "administrative", "classroom.png", 4),
                ("utilisateurs", "Utilisateurs", "Gestion des utilisateurs", "auth", "group.png", 5),
                ("enseignements", "Enseignements", "Gestion des enseignements", "academic", "book.png", 6),
                ("notes", "Notes", "Gestion des notes", "academic", "grade.png", 7),
                ("presences", "Présences", "Gestion des présences", "academic", "check.png", 8),
                ("bulletins", "Bulletins", "Gestion des bulletins", "academic", "stats.png", 9),
                ("emplois", "Emplois du temps", "Gestion des emplois du temps", "academic", "clock.png", 10),
                ("paiements", "Paiements", "Gestion des paiements", "administrative", "transfer.png", 11),
                ("matieres", "Matières", "Gestion des matières", "academic", "assignment.png", 12),
                ("parametres", "Paramètres", "Paramètres système", "auth", "settings.png", 13)
            ]
            
            # Insérer les vues
            for nom_view, titre, description, module, icon, order_idx in default_views:
                cursor.execute('''
                    INSERT OR IGNORE INTO views (nom_view, titre_view, description, module, icon, order_index)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (nom_view, titre, description, module, icon, order_idx))
            
            # Permissions par rôle (1=lecture, 2=écriture, 3=suppression)
            role_permissions = {
                "administrateur": {
                    "dashboard": 3, "eleves": 3, "professeurs": 3, "classes": 3, "salles": 3,
                    "utilisateurs": 3, "enseignements": 3, "notes": 3, "presences": 3,
                    "bulletins": 3, "emplois": 3, "paiements": 3, "matieres": 3, "parametres": 3
                },
                "directeur": {
                    "dashboard": 3, "eleves": 3, "professeurs": 3, "classes": 3, "salles": 2,
                    "utilisateurs": 2, "enseignements": 3, "notes": 3, "presences": 3,
                    "bulletins": 3, "emplois": 3, "paiements": 2, "matieres": 3, "parametres": 1
                },
                "secretaire": {
                    "dashboard": 2, "eleves": 3, "professeurs": 2, "classes": 2, "salles": 2,
                    "utilisateurs": 1, "enseignements": 2, "notes": 2, "presences": 3,
                    "bulletins": 2, "emplois": 2, "paiements": 3, "matieres": 1, "parametres": 1
                },
                "professeur": {
                    "dashboard": 2, "eleves": 2, "professeurs": 1, "classes": 2, "salles": 1,
                    "utilisateurs": 1, "enseignements": 2, "notes": 3, "presences": 3,
                    "bulletins": 2, "emplois": 1, "paiements": 1, "matieres": 2, "parametres": 1
                },
                "eleve": {
                    "dashboard": 1, "eleves": 1, "professeurs": 1, "classes": 1, "salles": 1,
                    "utilisateurs": 1, "enseignements": 1, "notes": 1, "presences": 1,
                    "bulletins": 1, "emplois": 1, "paiements": 1, "matieres": 1, "parametres": 1
                },
                "parent": {
                    "dashboard": 1, "eleves": 1, "professeurs": 1, "classes": 1, "salles": 1,
                    "utilisateurs": 1, "enseignements": 1, "notes": 1, "presences": 1,
                    "bulletins": 1, "emplois": 1, "paiements": 1, "matieres": 1, "parametres": 1
                }
            }
            
            # Assigner les permissions
            for role_name, view_perms in role_permissions.items():
                # Récupérer l'ID du rôle
                cursor.execute('SELECT id_role FROM roles WHERE nom_role = ?', (role_name,))
                role_result = cursor.fetchone()
                if not role_result:
                    continue
                
                role_id = role_result[0]
                
                for view_name, perm_level in view_perms.items():
                    # Récupérer l'ID de la vue
                    cursor.execute('SELECT id_view FROM views WHERE nom_view = ?', (view_name,))
                    view_result = cursor.fetchone()
                    if not view_result:
                        continue
                    
                    view_id = view_result[0]
                    
                    # Déterminer les permissions selon le niveau
                    can_read = perm_level >= 1
                    can_write = perm_level >= 2
                    can_delete = perm_level >= 3
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO role_view_permissions 
                        (role_id, view_id, can_read, can_write, can_delete, granted)
                        VALUES (?, ?, ?, ?, ?, 1)
                    ''', (role_id, view_id, can_read, can_write, can_delete))
            
            conn.commit()
            conn.close()
            print("✅ Permissions de vues par défaut créées")
            
        except Exception as e:
            print(f"❌ Erreur création permissions vues: {e}")
    
    def get_user_authorized_views(self, user_id: int) -> List[Dict]:
        """Récupère les vues autorisées pour un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT v.nom_view, v.titre_view, v.description, v.module, v.icon, v.order_index,
                       rvp.can_read, rvp.can_write, rvp.can_delete
                FROM user_roles ur
                JOIN role_view_permissions rvp ON ur.role_id = rvp.role_id
                JOIN views v ON rvp.view_id = v.id_view
                WHERE ur.user_id = ? AND rvp.granted = 1 AND v.is_active = 1
                ORDER BY v.order_index
            ''', (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            views = []
            for row in results:
                views.append({
                    'nom_view': row[0],
                    'titre_view': row[1],
                    'description': row[2],
                    'module': row[3],
                    'icon': row[4],
                    'order_index': row[5],
                    'can_read': bool(row[6]),
                    'can_write': bool(row[7]),
                    'can_delete': bool(row[8])
                })
            
            return views
            
        except Exception as e:
            print(f"❌ Erreur récupération vues autorisées: {e}")
            return []
    
    def can_access_view(self, user_id: int, view_name: str) -> bool:
        """Vérifie si un utilisateur peut accéder à une vue"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT COUNT(*) 
                FROM user_roles ur
                JOIN role_view_permissions rvp ON ur.role_id = rvp.role_id
                JOIN views v ON rvp.view_id = v.id_view
                WHERE ur.user_id = ? AND v.nom_view = ? AND rvp.granted = 1 AND v.is_active = 1
            ''', (user_id, view_name))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] > 0 if result else False
            
        except Exception as e:
            print(f"❌ Erreur vérification accès vue: {e}")
            return False
    
    def get_view_permissions(self, user_id: int, view_name: str) -> Dict[str, bool]:
        """Récupère les permissions spécifiques d'un utilisateur pour une vue"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT MAX(rvp.can_read), MAX(rvp.can_write), MAX(rvp.can_delete)
                FROM user_roles ur
                JOIN role_view_permissions rvp ON ur.role_id = rvp.role_id
                JOIN views v ON rvp.view_id = v.id_view
                WHERE ur.user_id = ? AND v.nom_view = ? AND rvp.granted = 1 AND v.is_active = 1
            ''', (user_id, view_name))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'can_read': bool(result[0]),
                    'can_write': bool(result[1]),
                    'can_delete': bool(result[2])
                }
            else:
                return {'can_read': False, 'can_write': False, 'can_delete': False}
                
        except Exception as e:
            print(f"❌ Erreur récupération permissions vue: {e}")
            return {'can_read': False, 'can_write': False, 'can_delete': False}
    
    def get_all_views(self) -> List[Dict]:
        """Récupère toutes les vues disponibles"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT nom_view, titre_view, description, module, icon, order_index
                FROM views
                WHERE is_active = 1
                ORDER BY order_index
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            views = []
            for row in results:
                views.append({
                    'nom_view': row[0],
                    'titre_view': row[1],
                    'description': row[2],
                    'module': row[3],
                    'icon': row[4],
                    'order_index': row[5]
                })
            
            return views
            
        except Exception as e:
            print(f"❌ Erreur récupération toutes vues: {e}")
            return []
    
    def set_current_user(self, user_id: int):
        """Définit l'utilisateur actuel"""
        self.current_user_id = user_id
        # Récupérer le rôle de l'utilisateur
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT r.nom_role, r.description, r.niveau_acces
                FROM user_roles ur
                JOIN roles r ON ur.role_id = r.id_role
                WHERE ur.user_id = ?
                ORDER BY r.niveau_acces DESC
                LIMIT 1
            ''', (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                # Créer un objet rôle simple
                self.current_user_role = type('Role', (), {
                    'name': result[0],
                    'description': result[1],
                    'niveau_acces': result[2]
                })()
            else:
                self.current_user_role = None
                
        except Exception as e:
            print(f"❌ Erreur récupération rôle utilisateur: {e}")
            self.current_user_role = None
    
    def get_filtered_navigation(self) -> Dict[str, List[tuple]]:
        """Récupère la navigation filtrée pour l'utilisateur actuel"""
        if not self.current_user_id:
            return {}
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT DISTINCT v.nom_view, v.titre_view, v.description, v.module, v.icon, v.order_index,
                       rvp.can_read, rvp.can_write, rvp.can_delete
                FROM user_roles ur
                JOIN role_view_permissions rvp ON ur.role_id = rvp.role_id
                JOIN views v ON rvp.view_id = v.id_view
                WHERE ur.user_id = ? AND rvp.granted = 1 AND v.is_active = 1
                ORDER BY v.order_index
            ''', (self.current_user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            # Organiser par sections/modules
            navigation = {}
            for row in results:
                module = row[3] or "general"
                if module not in navigation:
                    navigation[module] = []
                
                navigation[module].append((row[1], row[0]))  # (titre, nom_view)
            
            return navigation
            
        except Exception as e:
            print(f"❌ Erreur récupération navigation filtrée: {e}")
            return {}
