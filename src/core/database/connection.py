#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Connexion à la Base de Données
==============================================

Gère les connexions à la base de données avec pool de connexions et gestion d'erreurs.
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from contextlib import contextmanager

from src.core.exceptions import DatabaseError, ConfigurationError


class DatabaseManager:
    """Gestionnaire de connexion à la base de données"""
    
    def __init__(self, db_path: str):
        """Initialise le gestionnaire de base de données"""
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(__name__)
        self._connection = None
        self._is_connected = False
        
        # Vérifier que le chemin est valide
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Dossier de base de données créé: {self.db_path.parent}")
    
    def connect(self) -> bool:
        """Établit une connexion à la base de données"""
        try:
            if self._is_connected and self._connection:
                return True
            
            # Créer la connexion
            self._connection = sqlite3.connect(
                str(self.db_path),
                check_same_thread=False,
                timeout=30.0
            )
            
            # Configurer la connexion
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute("PRAGMA journal_mode = WAL")
            self._connection.execute("PRAGMA synchronous = NORMAL")
            self._connection.execute("PRAGMA cache_size = 10000")
            self._connection.execute("PRAGMA temp_store = memory")
            
            self._is_connected = True
            self.logger.info(f"Connexion à la base de données établie: {self.db_path}")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Erreur de connexion à la base de données: {e}")
            raise DatabaseError("Impossible de se connecter à la base de données", operation="connect", details={"error": str(e)})
        
        except Exception as e:
            self.logger.error(f"Erreur inattendue lors de la connexion: {e}")
            raise DatabaseError("Erreur inattendue lors de la connexion", operation="connect", details={"error": str(e)})
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        try:
            if self._connection:
                self._connection.close()
                self._connection = None
                self._is_connected = False
                self.logger.info("Connexion à la base de données fermée")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la fermeture de la connexion: {e}")
    
    def close(self):
        """Alias pour disconnect()"""
        self.disconnect()
    
    def test_connection(self) -> bool:
        """Teste la connexion à la base de données"""
        try:
            if not self.connect():
                return False
            
            # Exécuter une requête simple
            cursor = self._connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            cursor.close()
            
            if result and result[0] == 1:
                self.logger.info("Test de connexion réussi")
                return True
            else:
                self.logger.error("Test de connexion échoué")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors du test de connexion: {e}")
            return False
    
    @contextmanager
    def get_cursor(self):
        """Contexte manager pour obtenir un curseur de base de données"""
        cursor = None
        try:
            if not self._is_connected:
                self.connect()
            
            cursor = self._connection.cursor()
            yield cursor
            
            # Commit automatique si pas d'erreur
            self._connection.commit()
            
        except Exception as e:
            # Rollback en cas d'erreur
            if self._connection:
                self._connection.rollback()
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête", operation="execute", details={"error": str(e)})
            
        finally:
            if cursor:
                cursor.close()
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> int:
        """Exécute une requête SQL et retourne le nombre de lignes affectées"""
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                return cursor.rowcount
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête", operation="execute", details={"error": str(e), "query": query})
    
    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """Exécute une requête SQL avec plusieurs paramètres"""
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, params_list)
                return cursor.rowcount
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête multiple: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête multiple", operation="execute_many", details={"error": str(e), "query": query})
    
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Récupère une seule ligne de résultat"""
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                row = cursor.fetchone()
                if row:
                    return dict(row)
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération d'une ligne: {e}")
            raise DatabaseError("Erreur lors de la récupération d'une ligne", operation="fetch_one", details={"error": str(e), "query": query})
    
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Récupère toutes les lignes de résultat"""
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de toutes les lignes: {e}")
            raise DatabaseError("Erreur lors de la récupération de toutes les lignes", operation="fetch_all", details={"error": str(e), "query": query})
    
    def table_exists(self, table_name: str) -> bool:
        """Vérifie si une table existe"""
        try:
            query = """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name=?
            """
            result = self.fetch_one(query, (table_name,))
            return result is not None
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de l'existence de la table: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Récupère les informations sur une table"""
        try:
            query = "PRAGMA table_info(?)"
            return self.fetch_all(query, (table_name,))
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations de la table: {e}")
            return []
    
    def get_table_names(self) -> List[str]:
        """Récupère la liste de toutes les tables"""
        try:
            query = """
                SELECT name FROM sqlite_master 
                WHERE type='table' 
                ORDER BY name
            """
            results = self.fetch_all(query)
            return [row['name'] for row in results]
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des noms de tables: {e}")
            return []
    
    def backup_database(self, backup_path: str) -> bool:
        """Crée une sauvegarde de la base de données"""
        try:
            if not self._is_connected:
                self.connect()
            
            backup_path = Path(backup_path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Créer la sauvegarde
            backup_conn = sqlite3.connect(str(backup_path))
            self._connection.backup(backup_conn)
            backup_conn.close()
            
            self.logger.info(f"Sauvegarde créée: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """Restaure la base de données depuis une sauvegarde"""
        try:
            backup_path = Path(backup_path)
            if not backup_path.exists():
                self.logger.error(f"Fichier de sauvegarde introuvable: {backup_path}")
                return False
            
            # Fermer la connexion actuelle
            self.disconnect()
            
            # Restaurer depuis la sauvegarde
            import shutil
            shutil.copy2(backup_path, self.db_path)
            
            # Reconnecter
            self.connect()
            
            self.logger.info(f"Base de données restaurée depuis: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration: {e}")
            return False
    
    def get_database_size(self) -> int:
        """Retourne la taille de la base de données en octets"""
        try:
            if self.db_path.exists():
                return self.db_path.stat().st_size
            return 0
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de la taille: {e}")
            return 0
    
    def get_database_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la base de données"""
        try:
            info = {
                "path": str(self.db_path),
                "exists": self.db_path.exists(),
                "size_bytes": self.get_database_size(),
                "connected": self._is_connected,
                "tables": self.get_table_names()
            }
            
            if self._is_connected:
                info["sqlite_version"] = sqlite3.sqlite_version
                info["connection_timeout"] = 30.0
            
            return info
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations: {e}")
            return {"error": str(e)}
    
    def __enter__(self):
        """Support du contexte manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Support du contexte manager"""
        self.disconnect()
    
    def __del__(self):
        """Destructeur pour fermer la connexion"""
        try:
            self.disconnect()
        except:
            pass

