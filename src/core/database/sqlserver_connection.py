#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de Connexion SQL Server
====================================

Gère les connexions à SQL Server avec pool de connexions et gestion d'erreurs.
"""

import pyodbc
import logging
from typing import Optional, Dict, Any, List, Tuple
from contextlib import contextmanager
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine

from src.core.exceptions import DatabaseError, ConfigurationError

class SQLServerManager:
    """Gestionnaire de connexion à SQL Server"""
    
    def __init__(self, server: str, database: str, username: str = None, password: str = None, 
                 driver: str = "ODBC Driver 17 for SQL Server", trusted_connection: bool = False):
        """Initialise le gestionnaire de base de données SQL Server"""
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.trusted_connection = trusted_connection
        self.logger = logging.getLogger(__name__)
        self._engine = None
        self._connection = None
        self._is_connected = False
        
        # Construire la chaîne de connexion
        self._build_connection_string()
    
    def _build_connection_string(self):
        """Construit la chaîne de connexion SQL Server"""
        if self.trusted_connection:
            # Authentification Windows
            self.connection_string = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"Trusted_Connection=yes;"
            )
        else:
            # Authentification SQL Server
            self.connection_string = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
            )
        
        # Chaîne de connexion SQLAlchemy
        self.sqlalchemy_url = (
            f"mssql+pyodbc://{self.username}:{self.password}@{self.server}/{self.database}"
            f"?driver={self.driver.replace(' ', '+')}"
        )
    
    def connect(self) -> bool:
        """Établit une connexion à SQL Server"""
        try:
            if self._is_connected and self._connection:
                return True
            
            # Créer le moteur SQLAlchemy
            self._engine = create_engine(
                self.sqlalchemy_url,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=False
            )
            
            # Tester la connexion
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self._is_connected = True
            self.logger.info(f"Connexion à SQL Server établie: {self.server}/{self.database}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur de connexion à SQL Server: {e}")
            raise DatabaseError("Impossible de se connecter à SQL Server", 
                              operation="connect", 
                              details={"error": str(e)})
    
    def disconnect(self):
        """Ferme la connexion à SQL Server"""
        try:
            if self._engine:
                self._engine.dispose()
                self._engine = None
                self._is_connected = False
                self.logger.info("Connexion à SQL Server fermée")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la fermeture de la connexion: {e}")
    
    def close(self):
        """Alias pour disconnect()"""
        self.disconnect()
    
    def is_connected(self) -> bool:
        """Vérifie si la connexion est active"""
        return self._is_connected and self._engine is not None
    
    def cursor(self):
        """Retourne un curseur pour compatibilité avec l'ancien code"""
        if not self._engine:
            raise DatabaseError("Connexion non établie", operation="cursor")
        
        # Créer une connexion et retourner un curseur compatible
        conn = self._engine.connect()
        return conn
    
    def test_connection(self) -> bool:
        """Teste la connexion à SQL Server"""
        try:
            if not self.connect():
                return False
            
            with self._engine.connect() as conn:
                result = conn.execute(text("SELECT 1 as test"))
                row = result.fetchone()
                
            if row and row[0] == 1:
                self.logger.info("Test de connexion SQL Server réussi")
                return True
            else:
                self.logger.error("Test de connexion SQL Server échoué")
                return False
                
        except Exception as e:
            self.logger.error(f"Erreur lors du test de connexion: {e}")
            return False
    
    @contextmanager
    def get_cursor(self):
        """Contexte manager pour obtenir un curseur de base de données"""
        conn = None
        cursor = None
        try:
            if not self._is_connected:
                self.connect()
            
            conn = self._engine.connect()
            cursor = conn.execute(text(""))
            yield cursor
            
            # Commit automatique si pas d'erreur
            conn.commit()
            
        except Exception as e:
            # Rollback en cas d'erreur
            if conn:
                conn.rollback()
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête", 
                              operation="execute", 
                              details={"error": str(e)})
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute(self, query: str, params: Optional[Tuple] = None) -> int:
        """Exécute une requête SQL et retourne le nombre de lignes affectées"""
        try:
            with self._engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                conn.commit()
                return result.rowcount
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête", 
                              operation="execute", 
                              details={"error": str(e), "query": query})
    
    def execute_many(self, query: str, params_list: List) -> int:
        """Exécute une requête SQL avec plusieurs paramètres"""
        try:
            with self._engine.connect() as conn:
                total_rows = 0
                for params in params_list:
                    # Convertir les paramètres en liste si nécessaire
                    if isinstance(params, dict):
                        # Pour les dictionnaires, on utilise les valeurs dans l'ordre
                        params = list(params.values())
                    elif isinstance(params, tuple):
                        params = list(params)
                    
                    result = conn.execute(text(query), params)
                    total_rows += result.rowcount
                conn.commit()
                return total_rows
                
        except Exception as e:
            self.logger.error(f"Erreur lors de l'exécution de la requête multiple: {e}")
            raise DatabaseError("Erreur lors de l'exécution de la requête multiple", 
                              operation="execute_many", 
                              details={"error": str(e), "query": query})
    
    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Dict[str, Any]]:
        """Récupère une seule ligne de résultat"""
        try:
            with self._engine.connect() as conn:
                if params:
                    # Convertir les paramètres en liste si nécessaire
                    if isinstance(params, tuple):
                        params = list(params)
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                
                row = result.fetchone()
                if row:
                    return dict(row._mapping)
                return None
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération d'une ligne: {e}")
            raise DatabaseError("Erreur lors de la récupération d'une ligne", 
                              operation="fetch_one", 
                              details={"error": str(e), "query": query})
    
    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """Récupère toutes les lignes de résultat"""
        try:
            with self._engine.connect() as conn:
                if params:
                    result = conn.execute(text(query), params)
                else:
                    result = conn.execute(text(query))
                
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération de toutes les lignes: {e}")
            raise DatabaseError("Erreur lors de la récupération de toutes les lignes", 
                              operation="fetch_all", 
                              details={"error": str(e), "query": query})
    
    def table_exists(self, table_name: str) -> bool:
        """Vérifie si une table existe"""
        try:
            query = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = ?
            """
            result = self.fetch_one(query, (table_name,))
            return result is not None
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la vérification de l'existence de la table: {e}")
            return False
    
    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        """Récupère les informations sur une table"""
        try:
            query = """
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    IS_NULLABLE,
                    COLUMN_DEFAULT,
                    CHARACTER_MAXIMUM_LENGTH
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_NAME = ?
                ORDER BY ORDINAL_POSITION
            """
            return self.fetch_all(query, (table_name,))
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des informations de la table: {e}")
            return []
    
    def get_table_names(self) -> List[str]:
        """Récupère la liste de toutes les tables"""
        try:
            query = """
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
                ORDER BY TABLE_NAME
            """
            results = self.fetch_all(query)
            return [row['TABLE_NAME'] for row in results]
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la récupération des noms de tables: {e}")
            return []
    
    def create_database(self) -> bool:
        """Crée la base de données si elle n'existe pas"""
        try:
            # Connexion au serveur master pour créer la DB
            master_connection_string = self.connection_string.replace(
                f"DATABASE={self.database};", "DATABASE=master;"
            )
            
            conn = pyodbc.connect(master_connection_string)
            cursor = conn.cursor()
            
            # Vérifier si la base existe
            cursor.execute("SELECT name FROM sys.databases WHERE name = ?", (self.database,))
            if not cursor.fetchone():
                # Créer la base de données
                cursor.execute(f"CREATE DATABASE [{self.database}]")
                conn.commit()
                self.logger.info(f"Base de données '{self.database}' créée")
            else:
                self.logger.info(f"Base de données '{self.database}' existe déjà")
            
            conn.close()
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la création de la base de données: {e}")
            return False
    
    def get_database_info(self) -> Dict[str, Any]:
        """Retourne des informations sur la base de données"""
        try:
            info = {
                "server": self.server,
                "database": self.database,
                "connected": self._is_connected,
                "tables": self.get_table_names()
            }
            
            if self._is_connected:
                # Récupérer la version SQL Server
                version_query = "SELECT @@VERSION as version"
                version_result = self.fetch_one(version_query)
                if version_result:
                    info["sql_server_version"] = version_result["version"]
            
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
