# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
from enum import Enum
from typing import List, Dict, Optional

class PermissionLevel(Enum):
    """Niveaux de permissions"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

class Role:
    """Modèle de rôle avec permissions"""
    
    def __init__(self, id_role: int, nom: str, description: str, permissions: List[str]):
        self.id_role = id_role
        self.nom = nom
        self.description = description
        self.permissions = permissions if permissions else []
    
    def has_permission(self, permissions: str) -> bool:
        """Vérifie si le rôle a une permissions spécifique"""
        return permissions in self.permissions
    
    def can_read(self) -> bool:
        return self.has_permission(PermissionLevel.READ.value)
    
    def can_write(self) -> bool:
        return self.has_permission(PermissionLevel.WRITE.value)
    
    def can_delete(self) -> bool:
        return self.has_permission(PermissionLevel.DELETE.value)
    
    def is_admin(self) -> bool:
        return self.has_permission(PermissionLevel.ADMIN.value)

class RoleManager:
    """Gestionnaire des rôles"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Créer le dossier database s'il n'existe pas
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        try:
            self._init_roles_table()
            print("✅ Gestionnaire de rôles initialisé")
        except Exception as e:
            print(f"❌ Erreur initialisation rôles: {e}")
    
    def _init_roles_table(self):
        """Initialise la table des rôles"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Table des rôles
            cursor.execute('''
                CREATE TABLE roles (
                    id_role INT IDENTITY(1,1) PRIMARY KEY,
                    nom NVARCHAR(255) UNIQUE NOT NULL,
                    description NVARCHAR(255),
                    permissions NVARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT GETDATE()
                )
            ''')
            
            # Table des permissions par module
            cursor.execute('''
                CREATE TABLE role_permissions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    role_id INTEGER,
                    module NVARCHAR(255) NOT NULL,
                    permissions NVARCHAR(255) NOT NULL,
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    UNIQUE(role_id, module, permissions)
                )
            ''')
            
            # Table des utilisateurs et leurs rôles
            cursor.execute('''
                CREATE TABLE user_roles (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                    assigned_at DATETIME DEFAULT GETDATE(),
                    FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilisateur),
                    FOREIGN KEY (role_id) REFERENCES roles (id_role),
                    UNIQUE(user_id, role_id)
                )
            ''')
            
            conn.commit()
            conn.close()
            
            # Créer les rôles par défaut
            self._create_default_roles()
            
        except Exception as e:
            print(f"❌ Erreur création tables rôles: {e}")
            raise
    
    def _create_default_roles(self):
        """Crée les rôles par défaut du système"""
        try:
            default_roles = [
                {
                    "nom": "Super Administrateur",
                    "description": "Accès complet à tous les modules et fonctionnalités",
                    "permissions": ["read", "write", "delete", "admin"]
                },
                {
                    "nom": "Administrateur",
                    "description": "Gestion complète de l'établissement",
                    "permissions": ["read", "write", "delete"]
                },
                {
                    "nom": "Directeur",
                    "description": "Gestion des classes, élèves et professeurs",
                    "permissions": ["read", "write"]
                },
                {
                    "nom": "Professeur",
                    "description": "Gestion des notes, présences et bulletins",
                    "permissions": ["read", "write"]
                },
                {
                    "nom": "Secrétaire",
                    "description": "Gestion administrative et inscriptions",
                    "permissions": ["read", "write"]
                },
                {
                    "nom": "Élève",
                    "description": "Consultation des notes et bulletins",
                    "permissions": ["read"]
                },
                {
                    "nom": "Parent",
                    "description": "Consultation des informations de l'élève",
                    "permissions": ["read"]
                }
            ]
            
            for role_data in default_roles:
                if not self.role_exists(role_data["nom"]):
                    success = self.create_role(role_data["nom"], role_data["description"], role_data["permissions"])
                    if success:
                        print(f"✅ Rôle '{role_data['nom']}' créé")
                    else:
                        print(f"⚠️ Échec création rôle '{role_data['nom']}'")
                        
        except Exception as e:
            print(f"❌ Erreur création rôles par défaut: {e}")
    
    def create_role(self, nom: str, description: str, permissions: List[str]) -> bool:
        """Crée un nouveau rôle"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Insérer le rôle
            cursor.execute('''
                INSERT INTO roles (nom, description, permissions)
                VALUES (?, ?, ?)
            ''', (nom, description, ",".join(permissions) if permissions else "read"))
            
            role_id = cursor.lastrowid
            
            # Insérer les permissions détaillées
            if permissions:
                for permissions in permissions:
                    cursor.execute('''
                        INSERT INTO role_permissions (role_id, module, permissions)
                        VALUES (?, ?, ?)
                    ''', (role_id, "global", permissions))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur création rôle {nom}: {e}")
            return False
    
    def role_exists(self, nom: str) -> bool:
        """Vérifie si un rôle existe"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id_role FROM roles WHERE nom = ?', (nom,))
            exists = cursor.fetchone() is not None
            conn.close()
            return exists
        except Exception as e:
            print(f"❌ Erreur vérification rôle: {e}")
            return False
    
    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Récupère un rôle par son ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM roles WHERE id_role = ?', (role_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                permissions = row[3].split(",") if row[3] else ["read"]
                return Role(row[0], row[1], row[2], permissions)
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle par ID: {e}")
            return None
    
    def get_role_by_name(self, nom: str) -> Optional[Role]:
        """Récupère un rôle par son nom"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM roles WHERE nom = ?', (nom,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                permissions = row[3].split(",") if row[3] else ["read"]
                return Role(row[0], row[1], row[2], permissions)
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération rôle par nom: {e}")
            return None
    
    def get_all_roles(self) -> List[Role]:
        """Récupère tous les rôles"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM roles ORDER BY nom')
            rows = cursor.fetchall()
            conn.close()
            
            roles = []
            for row in rows:
                permissions = row[3].split(",") if row[3] else ["read"]
                roles.append(Role(row[0], row[1], row[2], permissions))
            
            return roles
            
        except Exception as e:
            print(f"❌ Erreur récupération tous les rôles: {e}")
            return []
    
    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """Assigne un rôle à un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO user_roles (user_id, role_id)
                VALUES (?, ?)
            ''', (user_id, role_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur attribution rôle: {e}")
            return False
    
    def get_user_roles(self, user_id: int) -> List[Role]:
        """Récupère tous les rôles d'un utilisateurs"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT r.* FROM roles r
                JOIN user_roles ur ON r.id_role = ur.role_id
                WHERE ur.user_id = ?
            ''', (user_id,))
            rows = cursor.fetchall()
            conn.close()
            
            roles = []
            for row in rows:
                permissions = row[3].split(",") if row[3] else ["read"]
                roles.append(Role(row[0], row[1], row[2], permissions))
            
            return roles
            
        except Exception as e:
            print(f"❌ Erreur récupération rôles utilisateurs: {e}")
            return []
    
    def update_role(self, role_id: int, nom: str, description: str, permissions: List[str]) -> bool:
        """Met à jour un rôle existant"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Mettre à jour le rôle
            cursor.execute('''
                UPDATE roles 
                SET nom = ?, description = ?, permissions = ?
                WHERE id_role = ?
            ''', (nom, description, ",".join(permissions) if permissions else "read", role_id))
            
            # Supprimer les anciennes permissions
            cursor.execute('DELETE FROM role_permissions WHERE role_id = ?', (role_id,))
            
            # Insérer les nouvelles permissions
            if permissions:
                for permissions in permissions:
                    cursor.execute('''
                        INSERT INTO role_permissions (role_id, module, permissions)
                        VALUES (?, ?, ?)
                    ''', (role_id, "global", permissions))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur mise à jour rôle: {e}")
            return False
    
    def delete_role(self, role_id: int) -> bool:
        """Supprime un rôle"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Vérifier si le rôle est utilisé
            cursor.execute('SELECT COUNT(*) FROM user_roles WHERE role_id = ?', (role_id,))
            if cursor.fetchone()[0] > 0:
                print("⚠️ Impossible de supprimer un rôle en cours d'utilisation")
                return False
            
            # Supprimer les permissions
            cursor.execute('DELETE FROM role_permissions WHERE role_id = ?', (role_id,))
            
            # Supprimer le rôle
            cursor.execute('DELETE FROM roles WHERE id_role = ?', (role_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Erreur suppression rôle: {e}")
            return False
