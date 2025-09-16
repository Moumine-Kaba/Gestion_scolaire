#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire d'Authentification Amélioré avec Rôles et Permissions
EduManager+ - Gestion Scolaire
"""

import sqlite3
import hashlib
import secrets
import time
import os
from typing import Optional, Dict, Tuple, List
from datetime import datetime, timedelta
import json

class EnhancedAuthManager:
    """Gestionnaire d'authentification avancé avec gestion des rôles et permissions"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser les gestionnaires
        self._init_managers()
        self._init_auth_tables()
        self._create_default_users()
    
    def _init_managers(self):
        """Initialise les gestionnaires de rôles et permissions"""
        try:
            from src.modules.role import RoleManager
            from src.modules.permissions import PermissionManager
            
            self.role_manager = RoleManager(self.db_path)
            self.permission_manager = PermissionManager(self.db_path)
            print("✅ Gestionnaires de rôles et permissions initialisés")
            
        except ImportError as e:
            print(f"⚠️ Erreur import gestionnaires: {e}")
            self.role_manager = None
            self.permission_manager = None
    
    def _init_auth_tables(self):
        """Initialise les tables d'authentification avancées"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si la table utilisateurs existe déjà
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='utilisateurs'")
            table_exists = cursor.fetchone() is not None
            
            if not table_exists:
                # Table des utilisateurs améliorée
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS utilisateurs (
                        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE,
                        password_hash TEXT NOT NULL,
                        salt TEXT NOT NULL,
                        nom TEXT NOT NULL,
                        prenom TEXT NOT NULL,
                        telephone TEXT,
                        date_naissance DATE,
                        adresse TEXT,
                        statut TEXT DEFAULT 'actif',
                        derniere_connexion TIMESTAMP,
                        nombre_tentatives INTEGER DEFAULT 0,
                        compte_bloque BOOLEAN DEFAULT FALSE,
                        date_blocage TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            else:
                # Ajouter les nouvelles colonnes si elles n'existent pas
                try:
                    cursor.execute('ALTER TABLE utilisateurs ADD COLUMN nombre_tentatives INTEGER DEFAULT 0')
                except sqlite3.OperationalError:
                    pass  # La colonne existe déjà
                
                try:
                    cursor.execute('ALTER TABLE utilisateurs ADD COLUMN compte_bloque BOOLEAN DEFAULT FALSE')
                except sqlite3.OperationalError:
                    pass  # La colonne existe déjà
                
                try:
                    cursor.execute('ALTER TABLE utilisateurs ADD COLUMN date_blocage TIMESTAMP')
                except sqlite3.OperationalError:
                    pass  # La colonne existe déjà
                
                try:
                    cursor.execute('ALTER TABLE utilisateurs ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                except sqlite3.OperationalError:
                    pass  # La colonne existe déjà
                
                try:
                    cursor.execute('ALTER TABLE utilisateurs ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
                except sqlite3.OperationalError:
                    pass  # La colonne existe déjà
            
            # Table des sessions sécurisées
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
                )
            ''')
            
            # Table des tentatives de connexion avec sécurité
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    ip_address TEXT,
                    success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_agent TEXT,
                    failure_reason TEXT
                )
            ''')
            
            # Table des logs de sécurité
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS security_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tables d'authentification avancées initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation tables: {e}")
    
    def _create_default_users(self):
        """Crée les utilisateurs par défaut avec rôles appropriés"""
        try:
            # Créer l'administrateur principal
            if not self.user_exists("admin"):
                self.create_user_with_role(
                    username="admin",
                    password="admin123",
                    email="admin@edumanager.com",
                    nom="Administrateur",
                    prenom="Système",
                    role_name="Super Administrateur"
                )
                print("✅ Administrateur principal créé")
            
            # Créer des utilisateurs de démonstration
            demo_users = [
                {
                    "username": "directeur",
                    "password": "directeur123",
                    "email": "directeur@edumanager.com",
                    "nom": "Martin",
                    "prenom": "Jean",
                    "role_name": "Directeur"
                },
                {
                    "username": "professeur",
                    "password": "prof123",
                    "email": "professeur@edumanager.com",
                    "nom": "Dubois",
                    "prenom": "Marie",
                    "role_name": "Professeur"
                },
                {
                    "username": "secretaire",
                    "password": "sec123",
                    "email": "secretaire@edumanager.com",
                    "nom": "Leroy",
                    "prenom": "Sophie",
                    "role_name": "Secrétaire"
                },
                {
                    "username": "eleve",
                    "password": "eleve123",
                    "email": "eleve@edumanager.com",
                    "nom": "Petit",
                    "prenom": "Lucas",
                    "role_name": "Élève"
                }
            ]
            
            for user_data in demo_users:
                if not self.user_exists(user_data["username"]):
                    self.create_user_with_role(**user_data)
                    print(f"✅ Utilisateur de démo créé: {user_data['username']}")
            
        except Exception as e:
            print(f"❌ Erreur création utilisateurs par défaut: {e}")
    
    def create_user_with_role(self, username: str, password: str, email: str = None,
                             nom: str = None, prenom: str = None, telephone: str = None,
                             date_naissance: str = None, adresse: str = None,
                             role_name: str = "Élève") -> bool:
        """Crée un utilisateur avec attribution automatique de rôle"""
        try:
            if self.user_exists(username):
                print(f"❌ L'utilisateur {username} existe déjà")
                return False
            
            # Hacher le mot de passe
            password_hash, salt = self._hash_password(password)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insérer l'utilisateur
            cursor.execute('''
                INSERT INTO utilisateurs (
                    username, email, password_hash, salt, nom, prenom,
                    telephone, date_naissance, adresse
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, nom, prenom,
                  telephone, date_naissance, adresse))
            
            user_id = cursor.lastrowid
            
            # Assigner le rôle
            if self.role_manager:
                role = self.role_manager.get_role_by_name(role_name)
                if role:
                    self.role_manager.assign_role_to_user(user_id, role.id_role)
                    print(f"✅ Rôle '{role_name}' assigné à {username}")
                else:
                    print(f"⚠️ Rôle '{role_name}' non trouvé, attribution du rôle par défaut")
                    # Créer un rôle par défaut si nécessaire
                    default_role = self.role_manager.get_role_by_name("Élève")
                    if default_role:
                        self.role_manager.assign_role_to_user(user_id, default_role.id_role)
            
            conn.commit()
            conn.close()
            
            # Logger la création
            self._log_security_action(user_id, "user_created", f"Utilisateur {username} créé avec le rôle {role_name}")
            
            print(f"✅ Utilisateur {username} créé avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création utilisateur: {e}")
            return False
    
    def _hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hache un mot de passe avec un sel sécurisé"""
        if salt is None:
            salt = secrets.token_hex(32)  # Sel de 64 caractères
        
        # Utiliser PBKDF2 pour le hachage
        combined = password + salt
        hash_obj = hashlib.sha256(combined.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return password_hash, salt
    
    def _verify_password(self, password: str, stored_hash: str, stored_salt: str) -> bool:
        """Vérifie un mot de passe"""
        password_hash, _ = self._hash_password(password, stored_salt)
        return password_hash == stored_hash
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None, 
                         user_agent: str = None) -> Optional[Dict]:
        """Authentifie un utilisateur avec vérifications de sécurité"""
        try:
            # Vérifier si le compte est bloqué
            if self._is_account_locked(username):
                self._log_login_attempt(username, ip_address, False, user_agent, "Compte bloqué")
                return None
            
            # Vérifier le nombre de tentatives
            if self._too_many_attempts(username, ip_address):
                self._log_login_attempt(username, ip_address, False, user_agent, "Trop de tentatives")
                return None
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer l'utilisateur
            cursor.execute('''
                SELECT id_utilisateur, username, email, password_hash, salt, 
                       nom, prenom, statut, derniere_connexion
                FROM utilisateurs WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            if not user_data:
                self._log_login_attempt(username, ip_address, False, user_agent, "Utilisateur inexistant")
                return None
            
            user_id, username, email, stored_hash, stored_salt, nom, prenom, statut, derniere_connexion = user_data
            
            # Vérifier le statut
            if statut != 'actif':
                self._log_login_attempt(username, ip_address, False, user_agent, "Compte désactivé")
                return None
            
            # Vérifier le mot de passe
            if not self._verify_password(password, stored_hash, stored_salt):
                # Incrémenter le nombre de tentatives
                self._increment_failed_attempts(username)
                
                # Vérifier si le compte doit être bloqué
                tentatives = self._get_failed_attempts(username)
                if tentatives >= 5:
                    self._lock_account(username)
                
                self._log_login_attempt(username, ip_address, False, user_agent, "Mot de passe incorrect")
                return None
            
            # Réinitialiser le nombre de tentatives en cas de succès
            self._reset_failed_attempts(username)
            
            # Mettre à jour la dernière connexion
            cursor.execute('''
                UPDATE utilisateurs 
                SET derniere_connexion = CURRENT_TIMESTAMP
                WHERE username = ?
            ''', (username,))
            
            # Récupérer les informations complètes de l'utilisateur
            user_info = self._get_complete_user_info(user_id, username, email, nom, prenom, statut, derniere_connexion)
            
            # Créer la session
            session_token = self._create_secure_session(user_id, ip_address, user_agent)
            user_info['session_token'] = session_token
            
            conn.commit()
            conn.close()
            
            # Logger la connexion réussie
            self._log_login_attempt(username, ip_address, True, user_agent, "Connexion réussie")
            self._log_security_action(user_id, "login_success", f"Connexion réussie depuis {ip_address}")
            
            print(f"✅ Connexion réussie pour {username}")
            return user_info
            
        except Exception as e:
            print(f"❌ Erreur authentification: {e}")
            return None
    
    def _get_complete_user_info(self, user_id: int, username: str, email: str, nom: str, 
                                prenom: str, statut: str, derniere_connexion: str) -> Dict:
        """Récupère les informations complètes de l'utilisateur avec rôles et permissions"""
        try:
            # Informations de base
            user_info = {
                'id': user_id,
                'username': username,
                'email': email,
                'nom': nom,
                'prenom': prenom,
                'statut': statut,
                'derniere_connexion': derniere_connexion,
                'full_name': f"{prenom} {nom}",
                'display_name': f"{prenom} {nom[0]}" if nom else prenom
            }
            
            # Rôles et permissions
            if self.role_manager and self.permission_manager:
                # Rôles
                roles = self.role_manager.get_user_roles(user_id)
                user_info['roles'] = [role.nom for role in roles] if roles else ["Utilisateur"]
                user_info['primary_role'] = roles[0].nom if roles else "Utilisateur"
                
                # Permissions détaillées
                permissions = self.permission_manager.get_user_view_permissions(user_id)
                user_info['permissions'] = permissions
                
                # Résumé des permissions
                permissions_summary = self.permission_manager.get_user_permissions_summary(user_id)
                user_info['permissions_summary'] = permissions_summary
                
                # Vues accessibles
                accessible_views = self.permission_manager.get_accessible_views_for_user(user_id)
                user_info['accessible_views'] = accessible_views
                
                # Niveau d'accès global
                user_info['access_level'] = self._determine_access_level(permissions)
                
            else:
                # Fallback si les gestionnaires ne sont pas disponibles
                user_info['roles'] = ["Utilisateur"]
                user_info['primary_role'] = "Utilisateur"
                user_info['permissions'] = {}
                user_info['access_level'] = "basic"
            
            return user_info
            
        except Exception as e:
            print(f"❌ Erreur récupération infos utilisateur: {e}")
            return user_info
    
    def _determine_access_level(self, permissions: Dict[str, str]) -> str:
        """Détermine le niveau d'accès global de l'utilisateur"""
        try:
            if not permissions:
                return "basic"
            
            # Compter les différents niveaux
            admin_count = sum(1 for level in permissions.values() if level == "admin")
            write_count = sum(1 for level in permissions.values() if level in ["write", "delete", "admin"])
            
            if admin_count > 5:
                return "super_admin"
            elif admin_count > 0:
                return "admin"
            elif write_count > 5:
                return "manager"
            elif write_count > 0:
                return "editor"
            else:
                return "viewer"
                
        except Exception as e:
            print(f"❌ Erreur détermination niveau accès: {e}")
            return "basic"
    
    def _get_failed_attempts(self, username: str) -> int:
        """Récupère le nombre de tentatives échouées"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si la colonne existe
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'nombre_tentatives' in columns:
                cursor.execute('SELECT nombre_tentatives FROM utilisateurs WHERE username = ?', (username,))
                result = cursor.fetchone()
                conn.close()
                return result[0] if result else 0
            else:
                conn.close()
                return 0
                
        except Exception as e:
            print(f"⚠️ Erreur récupération tentatives: {e}")
            return 0
    
    def _is_account_locked(self, username: str) -> bool:
        """Vérifie si un compte est bloqué"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si les colonnes existent
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'compte_bloque' in columns and 'date_blocage' in columns:
                cursor.execute('''
                    SELECT compte_bloque, date_blocage 
                    FROM utilisateurs 
                    WHERE username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                conn.close()
                
                if result and result[0]:
                    # Vérifier si le blocage a expiré (30 minutes)
                    if result[1]:
                        try:
                            lock_time = datetime.fromisoformat(result[1])
                            if datetime.now() - lock_time > timedelta(minutes=30):
                                # Débloquer automatiquement
                                self._unlock_account(username)
                                return False
                        except:
                            pass
                    return True
            
            conn.close()
            return False
            
        except Exception as e:
            print(f"⚠️ Erreur vérification blocage: {e}")
            return False
    
    def _too_many_attempts(self, username: str, ip_address: str) -> bool:
        """Vérifie s'il y a trop de tentatives de connexion"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier les tentatives par IP (dernières 15 minutes)
            cursor.execute('''
                SELECT COUNT(*) FROM login_attempts 
                WHERE ip_address = ? AND success = FALSE 
                AND timestamp > datetime('now', '-15 minutes')
            ''', (ip_address,))
            
            ip_attempts = cursor.fetchone()[0]
            
            # Vérifier les tentatives par utilisateur (dernières 15 minutes)
            cursor.execute('''
                SELECT COUNT(*) FROM login_attempts 
                WHERE username = ? AND success = FALSE 
                AND timestamp > datetime('now', '-15 minutes')
            ''', (username,))
            
            user_attempts = cursor.fetchone()[0]
            
            conn.close()
            
            # Limite: 10 tentatives par IP ou 5 par utilisateur
            return ip_attempts >= 10 or user_attempts >= 5
            
        except Exception as e:
            print(f"⚠️ Erreur vérification tentatives: {e}")
            return False
    
    def _increment_failed_attempts(self, username: str):
        """Incrémente le nombre de tentatives échouées"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si la colonne existe
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'nombre_tentatives' in columns:
                cursor.execute('''
                    UPDATE utilisateurs 
                    SET nombre_tentatives = COALESCE(nombre_tentatives, 0) + 1
                    WHERE username = ?
                ''', (username,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Erreur incrémentation tentatives: {e}")
    
    def _reset_failed_attempts(self, username: str):
        """Réinitialise le nombre de tentatives échouées"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si les colonnes existent
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'nombre_tentatives' in columns and 'compte_bloque' in columns and 'date_blocage' in columns:
                cursor.execute('''
                    UPDATE utilisateurs 
                    SET nombre_tentatives = 0, compte_bloque = FALSE, date_blocage = NULL
                    WHERE username = ?
                ''', (username,))
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"⚠️ Erreur réinitialisation tentatives: {e}")
    
    def _lock_account(self, username: str):
        """Bloque un compte"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si les colonnes existent
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'compte_bloque' in columns and 'date_blocage' in columns:
                cursor.execute('''
                    UPDATE utilisateurs 
                    SET compte_bloque = TRUE, date_blocage = CURRENT_TIMESTAMP
                    WHERE username = ?
                ''', (username,))
            
            conn.commit()
            conn.close()
            print(f"🔒 Compte {username} bloqué temporairement")
        except Exception as e:
            print(f"⚠️ Erreur blocage compte: {e}")
    
    def _unlock_account(self, username: str):
        """Débloque un compte"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si les colonnes existent
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if 'nombre_tentatives' in columns and 'compte_bloque' in columns and 'date_blocage' in columns:
                cursor.execute('''
                    UPDATE utilisateurs 
                    SET compte_bloque = FALSE, date_blocage = NULL, nombre_tentatives = 0
                    WHERE username = ?
                ''', (username,))
            
            conn.commit()
            conn.close()
            print(f"🔓 Compte {username} débloqué automatiquement")
        except Exception as e:
            print(f"⚠️ Erreur déblocage compte: {e}")
    
    def _create_secure_session(self, user_id: int, ip_address: str = None, user_agent: str = None) -> str:
        """Crée une session sécurisée"""
        try:
            session_token = secrets.token_urlsafe(64)  # Token très long
            expires_at = datetime.now() + timedelta(hours=8)  # Session de 8h
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Désactiver les anciennes sessions
            cursor.execute('''
                UPDATE sessions 
                SET is_active = FALSE 
                WHERE user_id = ?
            ''', (user_id,))
            
            # Créer la nouvelle session
            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, session_token, expires_at, ip_address, user_agent))
            
            conn.commit()
            conn.close()
            
            return session_token
            
        except Exception as e:
            print(f"⚠️ Erreur création session: {e}")
            return secrets.token_urlsafe(32)  # Fallback
    
    def _log_login_attempt(self, username: str, ip_address: str, success: bool, 
                          user_agent: str = None, reason: str = None):
        """Enregistre une tentative de connexion"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO login_attempts (username, ip_address, success, user_agent, failure_reason)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, ip_address, success, user_agent, reason))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Erreur log tentative connexion: {e}")
    
    def _log_security_action(self, user_id: int, action: str, details: str, ip_address: str = None):
        """Enregistre une action de sécurité"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO security_logs (user_id, action, details, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, action, details, ip_address))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"⚠️ Erreur log sécurité: {e}")
    
    def user_exists(self, username: str) -> bool:
        """Vérifie si un utilisateur existe"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE username = ?', (username,))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except Exception as e:
            print(f"❌ Erreur vérification utilisateur: {e}")
            return False
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Valide une session et retourne les informations de l'utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.user_id, s.expires_at, s.ip_address, u.username, u.email, 
                       u.nom, u.prenom, u.statut
                FROM sessions s
                JOIN utilisateurs u ON s.user_id = u.id_utilisateur
                WHERE s.session_token = ? AND s.is_active = TRUE
            ''', (session_token,))
            
            session_data = cursor.fetchone()
            if not session_data:
                return None
            
            user_id, expires_at, ip_address, username, email, nom, prenom, statut = session_data
            
            # Vérifier l'expiration
            if datetime.fromisoformat(expires_at) < datetime.now():
                # Désactiver la session expirée
                cursor.execute('UPDATE sessions SET is_active = FALSE WHERE session_token = ?', (session_token,))
                conn.commit()
                conn.close()
                return None
            
            # Récupérer les informations complètes
            user_info = self._get_complete_user_info(user_id, username, email, nom, prenom, statut, None)
            user_info['session_token'] = session_token
            user_info['ip_address'] = ip_address
            
            conn.close()
            return user_info
            
        except Exception as e:
            print(f"❌ Erreur validation session: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Déconnecte un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer l'ID utilisateur avant de supprimer
            cursor.execute('SELECT user_id FROM sessions WHERE session_token = ?', (session_token,))
            result = cursor.fetchone()
            
            if result:
                user_id = result[0]
                # Logger la déconnexion
                self._log_security_action(user_id, "logout", "Déconnexion utilisateur")
            
            # Désactiver la session
            cursor.execute('UPDATE sessions SET is_active = FALSE WHERE session_token = ?', (session_token,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur déconnexion: {e}")
            return False
    
    def get_user_security_status(self, username: str) -> Dict:
        """Récupère le statut de sécurité d'un utilisateur"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier si les colonnes existent
            cursor.execute("PRAGMA table_info(utilisateurs)")
            columns = [col[1] for col in cursor.fetchall()]
            
            if all(col in columns for col in ['nombre_tentatives', 'compte_bloque', 'date_blocage', 'derniere_connexion']):
                cursor.execute('''
                    SELECT nombre_tentatives, compte_bloque, date_blocage, derniere_connexion
                    FROM utilisateurs WHERE username = ?
                ''', (username,))
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    tentatives, bloque, date_blocage, derniere_connexion = result
                    return {
                        'tentatives_failed': tentatives,
                        'account_locked': bloque,
                        'lock_date': date_blocage,
                        'last_login': derniere_connexion,
                        'is_locked': bloque and date_blocage and (datetime.now() - datetime.fromisoformat(date_blocage)) < timedelta(minutes=30)
                    }
            
            conn.close()
            return {}
            
        except Exception as e:
            print(f"⚠️ Erreur statut sécurité: {e}")
            return {}
    
    def get_security_logs(self, user_id: int = None, limit: int = 100) -> List[Dict]:
        """Récupère les logs de sécurité"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if user_id:
                cursor.execute('''
                    SELECT user_id, action, details, ip_address, timestamp
                    FROM security_logs 
                    WHERE user_id = ?
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, limit))
            else:
                cursor.execute('''
                    SELECT user_id, action, details, ip_address, timestamp
                    FROM security_logs 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (limit,))
            
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    'user_id': row[0],
                    'action': row[1],
                    'details': row[2],
                    'ip_address': row[3],
                    'timestamp': row[4]
                })
            
            conn.close()
            return logs
            
        except Exception as e:
            print(f"⚠️ Erreur récupération logs: {e}")
            return []
