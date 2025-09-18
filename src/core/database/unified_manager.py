#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Base de Données Unifié
======================================

Gère les connexions à différentes bases de données (SQLite, SQL Server, PostgreSQL).
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import logging
from typing import Optional, Dict, Any, List, Tuple
from contextlib import contextmanager
from enum import Enum

from src.core.config import DatabaseConfig
from src.core.database.sqlserver_connection import SQLServerManager
from src.core.exceptions import DatabaseError, ConfigurationError

class DatabaseType(Enum):
    """Types de bases de données supportées"""
    SQLITE = "sqlite"
    SQLSERVER = "sqlserver"
    POSTGRESQL = "postgresql"

class UnifiedDatabaseManager:
    """Gestionnaire unifié pour différentes bases de données"""
    
    def __init__(self, config: DatabaseConfig):
        """Initialise le gestionnaire unifié"""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self._manager = None
        self._db_type = DatabaseType(config.type.lower())
        
        # Initialiser le gestionnaire approprié
        self._initialize_manager()
    
    def _initialize_manager(self):
        """Initialise le gestionnaire de base de données approprié"""
        try:
            if self._db_type == DatabaseType.SQLITE:
                self._manager = SQLiteManager(self.config.path)
            elif self._db_type == DatabaseType.SQLSERVER:
                self._manager = SQLServerManager(
                    server=self.config.host,
                    database=self.config.name,
                    username=self.config.username,
                    password=self.config.password,
                    driver=self.config.driver,
                    trusted_connection=self.config.trusted_connection
                )
            elif self._db_type == DatabaseType.POSTGRESQL:
                # TODO: Implémenter PostgreSQL si nécessaire
                raise NotImplementedError("PostgreSQL n'est pas encore implémenté")
            else:
                raise ValueError(f"Type de base de données non supporté: {self.config.type}")
            
            self.logger.info(f"Gestionnaire de base de données initialisé: {self._db_type.value}")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'initialisation du gestionnaire: {e}")
            raise ConfigurationError(f"Impossible d'initialiser le gestionnaire de base de données", 
                                   details={"error": str(e), "type": self.config.type})
    
    def connect(self) -> bool:
        """Établit une connexion à la base de données"""
        try:
            return self._manager.connect()
        except Exception as e:
            self.logger.error(f"Erreur de connexion: {e}")
            raise DatabaseError("Impossible de se connecter à la base de données", 
                              operation="connect", 
                              details={"error": str(e), "type": self.config.type})
    
    def disconnect(self):
        """Ferme la connexion à la base de données"""
        try:
            self._manager.disconnect()
        except Exception as e:
            self.logger.error(f"Erreur lors de la fermeture: {e}")
    
    def close(self):
        """Alias pour disconnect()"""
        self.disconnect()
    
    def test_connection(self) -> bool:
        """Teste la connexion à la base de données"""
        try:
            return self._manager.test_connection()
        except Exception as e:
            self.logger.error(f"Erreur lors du test de connexion: {e}")
            return False
    
    @contextmanager
    def get_cursor(self):
        """Contexte manager pour obtenir un curseur de base de données"""
        try:
            with self._manager.get_cursor() as cursor:
                yield cursor
        except Exception as e:
            self.logger.error(f"Erreur lors de l'obtention du curseur: {e}")
            raise DatabaseError("Erreur lors de l'obtention du curseur", 
                              operation="get_cursor", 
                              details={"error": str(e)})
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> int:
        """Exécute une requête SQL et retourne le nombre de lignes affectées"""
        try:
            # Adapter la requête selon le type de base de données
            adapted_query = self._adapt_query(query)
            return self._manager.execute(adapted_query, params)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête", 
                              operation="execute", 
                              details={"error": str(e), "query": query})
    
    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """Exécute une requête SQL avec plusieurs paramètres"""
        try:
            adapted_query = self._adapt_query(query)
            return self._manager.execute_many(adapted_query, params_list)
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête multiple: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête multiple", 
                              operation="execute_many", 
                              details={"error": str(e), "query": query})
    
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Récupère une seule ligne de résultat"""
        try:
            adapted_query = self._adapt_query(query)
            return self._manager.fetch_one(adapted_query, params)
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération d'une ligne: {e}")
            raise DatabaseError("Erreur lors de la récupération d'une ligne", 
                              operation="fetch_one", 
                              details={"error": str(e), "query": query})
    
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Récupère toutes les lignes de résultat"""
        try:
            adapted_query = self._adapt_query(query)
            return self._manager.fetch_all(adapted_query, params)
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de toutes les lignes: {e}")
            raise DatabaseError("Erreur lors de la récupération de toutes les lignes", 
                              operation="fetch_all", 
                              details={"error": str(e), "query": query})
    
    def table_exists(self, table_name: str) -> bool:
        """Vérifie si une table existe"""
        try:
            return self._manager.table_exists(table_name)
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de l'existence de la table: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Récupère les informations sur une table"""
        try:
            return self._manager.get_table_info(table_name)
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations de la table: {e}")
            return []
    
    def get_table_names(self) -> List[str]:
        """Récupère la liste de toutes les tables"""
        try:
            return self._manager.get_table_names()
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des noms de tables: {e}")
            return []
    
    def backup_database(self, backup_path: str) -> bool:
        """Crée une sauvegarde de la base de données"""
        try:
            return self._manager.backup_database(backup_path)
        except Exception as e:
            self.logger.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def restore_database(self, backup_path: str) -> bool:
        """Restaure la base de données depuis une sauvegarde"""
        try:
            return self._manager.restore_database(backup_path)
        except Exception as e:
            self.logger.error(f"Erreur lors de la restauration: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la base de données"""
        try:
            info = self._manager.get_database_info()
            info["type"] = self._db_type.value
            info["config"] = {
                "host": self.config.host,
                "port": self.config.port,
                "name": self.config.name,
                "username": self.config.username,
                "driver": self.config.driver,
                "trusted_connection": self.config.trusted_connection
            }
            return info
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations: {e}")
            return {"error": str(e), "type": self._db_type.value}
    
    def _adapt_query(self, query: str) -> str:
        """Adapte une requête SQL selon le type de base de données"""
        if self._db_type == DatabaseType.SQLITE:
            return query
        elif self._db_type == DatabaseType.SQLSERVER:
            return self._adapt_query_for_sqlserver(query)
        else:
            return query
    
    def _adapt_query_for_sqlserver(self, query: str) -> str:
        """Adapte une requête SQL pour SQL Server"""
        # Remplacements spécifiques pour SQL Server
        adapted_query = query
        
        # Remplacer LIMIT par TOP (pour les requêtes simples)
        if "LIMIT" in adapted_query.upper() and "ORDER BY" in adapted_query.upper():
            # Pour les requêtes avec ORDER BY, utiliser OFFSET/FETCH
            pass  # SQL Server 2012+ supporte OFFSET/FETCH
        elif "LIMIT" in adapted_query.upper():
            # Pour les requêtes simples sans ORDER BY
            import re
            limit_match = re.search(r'LIMIT\s+(\d+)', adapted_query, re.IGNORECASE)
            if limit_match:
                limit_value = limit_match.group(1)
                # Remplacer LIMIT par TOP au début de la requête SELECT
                adapted_query = re.sub(r'SELECT\s+', f'SELECT TOP {limit_value} ', adapted_query, flags=re.IGNORECASE)
                adapted_query = re.sub(r'LIMIT\s+\d+', '', adapted_query, flags=re.IGNORECASE)
        
        # Remplacer les fonctions de date SQLite par SQL Server
        adapted_query = adapted_query.replace("date('now')", "GETDATE()")
        adapted_query = adapted_query.replace("datetime('now')", "GETDATE()")
        
        # Remplacer les paramètres ? par @param pour SQL Server (si nécessaire)
        # Note: pyodbc peut gérer les ? directement
        
        return adapted_query
    
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

# Fonction utilitaire pour créer un gestionnaire de base de données
def create_database_manager(config: Optional[DatabaseConfig] = None) -> UnifiedDatabaseManager:
    """Crée un gestionnaire de base de données unifié"""
    if config is None:
        from src.core.config import get_config
        config = get_config().database
    
    return Unifiedget_db_connection()
