# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import hashlib
import secrets
import time
import os
from typing import Optional, Dict, Tuple
from datetime import datetime, timedelta

# Import local du gestionnaire de rôles
try:
    from src.modules.roles import RoleManager, Role
except ImportError:
    # Fallback si l'import échoue
    RoleManager = None
    Role = None

class AuthManager:
    """Gestionnaire d'authentification et de sécurité"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Créer le dossier database s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialiser le gestionnaire de rôles
        if RoleManager:
            self.role_manager = RoleManager(db_path)
        else:
            self.role_manager = None
            print("⚠️ Gestionnaire de rôles non disponible")
        
        self._init_auth_tables()
        self._create_default_admin()
    
    def _init_auth_tables(self):
        """Initialise les tables d'authentification"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Table des utilisateurs (si elle n'existe pas)
            cursor.execute('''
                CREATE TABLE utilisateurs (
                    id_utilisateur INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(255) UNIQUE NOT NULL,
                    email NVARCHAR(255) UNIQUE,
                    password_hash NVARCHAR(255) NOT NULL,
                    salt NVARCHAR(255) NOT NULL,
                    nom NVARCHAR(255),
                    prenom NVARCHAR(255),
                    telephone NVARCHAR(255),
                    date_naissance DATE,
                    adresse NVARCHAR(255),
                    statut NVARCHAR(255) DEFAULT 'actif',
                    derniere_connexion TIMESTAMP,
                    created_at DATETIME DEFAULT GETDATE(),
                    updated_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Table des sessions
            cursor.execute('''
                CREATE TABLE sessions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    session_token NVARCHAR(255) UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address NVARCHAR(255),
                    user_agent NVARCHAR(255),
                    created_at DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur)
                )
            ''')
            
            # Table des tentatives de connexion
            cursor.execute('''
                CREATE TABLE login_attempts (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    username NVARCHAR(255) NOT NULL,
                    ip_address NVARCHAR(255),
                    success BOOLEAN NOT NULL,
                    timestamp DATETIME DEFAULT GETDATE()
                )
            ''')
            
            conn.commit()
            conn.close()
            print("✅ Tables d'authentification initialisées")
            
        except Exception as e:
            print(f"❌ Erreur initialisation tables: {e}")
    
    def _create_default_admin(self):
        """Crée l'utilisateurs administrateur par défaut"""
        try:
            if not self.user_exists("admin"):
                # Créer l'admin sans rôle si le gestionnaire de rôles n'est pas disponible
                if self.role_manager:
                    success = self.create_user(
                        username="admin",
                        password="admin123",
                        email="admin@edumanager.com",
                        nom="Administrateur",
                        prenom="Système",
                        role_name="Super Administrateur"
                    )
                else:
                    success = self.create_user_simple(
                        username="admin",
                        password="admin123",
                        email="admin@edumanager.com",
                        nom="Administrateur",
                        prenom="Système"
                    )
                
                if success:
                    print("✅ Utilisateur administrateur créé avec succès!")
                    print("   Username: admin")
                    print("   Password: admin123")
                else:
                    print("❌ Échec création utilisateurs admin")
        except Exception as e:
            print(f"❌ Erreur création admin: {e}")
    
    def create_user_simple(self, username: str, password: str, email: str = None, 
                          nom: str = None, prenom: str = None) -> bool:
        """Crée un utilisateurs simple sans gestion des rôles"""
        try:
            if self.user_exists(username):
                print(f"❌ L'utilisateurs {username} existe déjà")
                return False
            
            password_hash, salt = self._hash_password(password)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO utilisateurs (
                    username, email, password_hash, salt, nom, prenom
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, nom, prenom))
            
            conn.commit()
            conn.close()
            
            print(f"✅ Utilisateur {username} créé avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création utilisateurs: {e}")
            return False
    
    def _hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        """Hache un mot de passe avec un sel"""
        if salt is None:
            salt = secrets.token_hex(16)
        
        # Combiner le mot de passe et le sel
        combined = password + salt
        
        # Créer le hash SHA-256
        hash_obj = hashlib.sha256(combined.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        
        return password_hash, salt
    
    def _verify_password(self, password: str, stored_hash: str, stored_salt: str) -> bool:
        """Vérifie un mot de passe"""
        password_hash, _ = self._hash_password(password, stored_salt)
        return password_hash == stored_hash
    
    def create_user(self, username: str, password: str, email: str = None, 
                   nom: str = None, prenom: str = None, telephone: str = None,
                   date_naissance: str = None, adresse: str = None, 
                   role_name: str = "Élève") -> bool:
        """Crée un nouvel utilisateurs avec gestion des rôles"""
        try:
            # Vérifier si l'utilisateurs existe déjà
            if self.user_exists(username):
                print(f"❌ L'utilisateurs {username} existe déjà")
                return False
            
            # Hacher le mot de passe
            password_hash, salt = self._hash_password(password)
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insérer l'utilisateurs
            cursor.execute('''
                INSERT INTO utilisateurs (
                    username, email, password_hash, salt, nom, prenom,
                    telephone, date_naissance, adresse
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (username, email, password_hash, salt, nom, prenom,
                  telephone, date_naissance, adresse))
            
            user_id = cursor.lastrowid
            
            # Assigner le rôle si le gestionnaire est disponible
            if self.role_manager:
                roles = self.role_manager.get_role_by_name(role_name)
                if roles:
                    self.role_manager.assign_role_to_user(user_id, roles.id_role)
                    print(f"✅ Rôle '{role_name}' assigné à {username}")
                else:
                    print(f"⚠️ Rôle '{role_name}' non trouvé pour {username}")
            
            conn.commit()
            conn.close()
            
            print(f"✅ Utilisateur {username} créé avec succès!")
            return True
            
        except Exception as e:
            print(f"❌ Erreur création utilisateurs: {e}")
            return False
    
    def user_exists(self, username: str) -> bool:
        """Vérifie si un utilisateurs existe"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id_utilisateur FROM utilisateurs WHERE username = ?', (username,))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except Exception as e:
            print(f"❌ Erreur vérification utilisateurs: {e}")
            return False
    
    def authenticate_user(self, username: str, password: str, ip_address: str = None) -> Optional[Dict]:
        """Authentifie un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer l'utilisateurs
            cursor.execute('''
                SELECT id_utilisateur, username, email, password_hash, salt, 
                       nom, prenom, statut, derniere_connexion
                FROM utilisateurs WHERE username = ?
            ''', (username,))
            
            user_data = cursor.fetchone()
            if not user_data:
                self._log_login_attempt(username, ip_address, False)
                return None
            
            user_id, username, email, stored_hash, stored_salt, nom, prenom, statut, derniere_connexion = user_data
            
            # Vérifier le statut
            if statut != 'actif':
                print(f"❌ Compte {username} désactivé")
                return None
            
            # Vérifier le mot de passe
            if not self._verify_password(password, stored_hash, stored_salt):
                self._log_login_attempt(username, ip_address, False)
                print(f"❌ Mot de passe incorrect pour {username}")
                return None
            
            # Mettre à jour la dernière connexion
            cursor.execute('''
                UPDATE utilisateurs 
                SET derniere_connexion = CURRENT_TIMESTAMP
                WHERE id_utilisateur = ?
            ''', (user_id,))
            
            # Récupérer les rôles de l'utilisateurs
            roles = []
            permissions = []
            if self.role_manager:
                roles = self.role_manager.get_user_roles(user_id)
                permissions = self._get_user_permissions(roles)
            
            # Créer la session
            session_token = self._create_session(user_id, ip_address)
            
            conn.commit()
            conn.close()
            
            # Logger la tentative réussie
            self._log_login_attempt(username, ip_address, True)
            
            # Retourner les informations de l'utilisateurs
            user_info = {
                'id_utilisateur': user_id,
                'username': username,
                'email': email,
                'nom': nom,
                'prenom': prenom,
                'statut': statut,
                'roles': [roles.nom for roles in roles] if roles else ["Utilisateur"],
                'permissions': permissions,
                'session_token': session_token,
                'derniere_connexion': derniere_connexion
            }
            
            print(f"✅ Connexion réussie pour {username}")
            return user_info
            
        except Exception as e:
            print(f"❌ Erreur authentification: {e}")
            return None
    
    def _create_session(self, user_id: int, ip_address: str = None) -> str:
        """Crée une nouvelle session pour l'utilisateurs"""
        try:
            session_token = secrets.token_urlsafe(32)
            expires_at = datetime.now() + timedelta(hours=24)  # Session de 24h
            
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Supprimer les anciennes sessions de l'utilisateurs
            cursor.execute('DELETE FROM sessions WHERE user_id = ?', (user_id,))
            
            # Créer la nouvelle session
            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at, ip_address)
                VALUES (?, ?, ?, ?)
            ''', (user_id, session_token, expires_at, ip_address))
            
            conn.commit()
            conn.close()
            
            return session_token
            
        except Exception as e:
            print(f"❌ Erreur création session: {e}")
            return secrets.token_urlsafe(32)  # Fallback
    
    def _get_user_permissions(self, roles: list) -> list:
        """Récupère toutes les permissions d'un utilisateurs"""
        try:
            permissions = set()
            for roles in roles:
                if hasattr(roles, 'permissions'):
                    permissions.update(roles.permissions)
            return list(permissions)
        except Exception as e:
            print(f"❌ Erreur récupération permissions: {e}")
            return ["read"]  # Permission par défaut
    
    def _log_login_attempt(self, username: str, ip_address: str, success: bool):
        """Enregistre une tentative de connexion"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO login_attempts (username, ip_address, success)
                VALUES (?, ?, ?)
            ''', (username, ip_address, success))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"❌ Erreur log tentative connexion: {e}")
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        """Valide une session et retourne les informations de l'utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Vérifier la session
            cursor.execute('''
                SELECT s.user_id, s.expires_at, u.username, u.email, u.nom, u.prenom, u.statut
                FROM sessions s
                JOIN utilisateurs u ON s.user_id = u.id_utilisateur
                WHERE s.session_token = ?
            ''', (session_token,))
            
            session_data = cursor.fetchone()
            if not session_data:
                return None
            
            user_id, expires_at, username, email, nom, prenom, statut = session_data
            
            # Vérifier l'expiration
            if datetime.fromisoformat(expires_at) < datetime.now():
                # Supprimer la session expirée
                cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
                conn.commit()
                conn.close()
                return None
            
            # Récupérer les rôles
            roles = []
            permissions = []
            if self.role_manager:
                roles = self.role_manager.get_user_roles(user_id)
                permissions = self._get_user_permissions(roles)
            
            conn.close()
            
            return {
                'id_utilisateur': user_id,
                'username': username,
                'email': email,
                'nom': nom,
                'prenom': prenom,
                'statut': statut,
                'roles': [roles.nom for roles in roles] if roles else ["Utilisateur"],
                'permissions': permissions
            }
            
        except Exception as e:
            print(f"❌ Erreur validation session: {e}")
            return None
    
    def logout_user(self, session_token: str) -> bool:
        """Déconnecte un utilisateurs en supprimant sa session"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur déconnexion: {e}")
            return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Récupère un utilisateurs par son ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_utilisateur, username, email, nom, prenom, telephone,
                       date_naissance, adresse, statut, derniere_connexion, created_at
                FROM utilisateurs WHERE id_utilisateur = ?
            ''', (user_id,))
            
            user_data = cursor.fetchone()
            if not user_data:
                return None
            
            # Récupérer les rôles
            roles = []
            if self.role_manager:
                roles = self.role_manager.get_user_roles(user_id)
            
            conn.close()
            
            return {
                'id_utilisateur': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'nom': user_data[3],
                'prenom': user_data[4],
                'telephone': user_data[5],
                'date_naissance': user_data[6],
                'adresse': user_data[7],
                'statut': user_data[8],
                'derniere_connexion': user_data[9],
                'created_at': user_data[10],
                'roles': [roles.nom for roles in roles] if roles else ["Utilisateur"]
            }
            
        except Exception as e:
            print(f"❌ Erreur récupération utilisateurs: {e}")
            return None
    
    def get_all_users(self) -> list:
        """Récupère tous les utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id_utilisateur, username, email, nom, prenom, statut, derniere_connexion
                FROM utilisateurs ORDER BY username
            ''')
            
            users = []
            for row in cursor.fetchall():
                user_id = row[0]
                roles = []
                if self.role_manager:
                    roles = self.role_manager.get_user_roles(user_id)
                
                users.append({
                    'id_utilisateur': user_id,
                    'username': row[1],
                    'email': row[2],
                    'nom': row[3],
                    'prenom': row[4],
                    'statut': row[5],
                    'derniere_connexion': row[6],
                    'roles': [roles.nom for roles in roles] if roles else ["Utilisateur"]
                })
            
            conn.close()
            return users
            
        except Exception as e:
            print(f"❌ Erreur récupération utilisateurs: {e}")
            return []
    
    def update_user_status(self, user_id: int, statut: str) -> bool:
        """Met à jour le statut d'un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE utilisateurs 
                SET statut = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id_utilisateur = ?
            ''', (statut, user_id))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour statut: {e}")
            return False
