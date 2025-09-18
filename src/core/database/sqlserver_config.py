#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration SQL Server pour EduManager+
==========================================

Fichier de configuration spécifique pour la migration vers SQL Server.
"""

import os
from pathlib import Path
from src.core.config import DatabaseConfig, Config

# Configuration SQL Server par défaut
SQLSERVER_CONFIG = {
    'type': 'sqlserver',
    'host': '.',  # Instance par défaut détectée
    'port': 1433,
    'name': 'EduManager',
    'username': '',  # Vide pour l'authentification Windows
    'password': '',  # Vide pour l'authentification Windows
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': True  # Authentification Windows détectée
}

# Configuration pour l'authentification Windows (recommandée)
SQLSERVER_WINDOWS_AUTH_CONFIG = {
    'type': 'sqlserver',
    'host': 'localhost',
    'port': 1433,
    'name': 'EduManager',
    'username': '',  # Vide pour l'authentification Windows
    'password': '',  # Vide pour l'authentification Windows
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': True
}

def get_sqlserver_config() -> DatabaseConfig:
    """Retourne la configuration SQL Server"""
    return DatabaseConfig(**SQLSERVER_CONFIG)

def get_sqlserver_windows_auth_config() -> DatabaseConfig:
    """Retourne la configuration SQL Server avec authentification Windows"""
    return DatabaseConfig(**SQLSERVER_WINDOWS_AUTH_CONFIG)

def create_sqlserver_config(server: str, database: str, username: str = None, 
                          password: str = None, use_windows_auth: bool = False) -> DatabaseConfig:
    """Crée une configuration SQL Server personnalisée"""
    if use_windows_auth:
        return DatabaseConfig(
            type='sqlserver',
            host=server,
            port=1433,
            name=database,
            username='',
            password='',
            driver='ODBC Driver 17 for SQL Server',
            trusted_connection=True
        )
    else:
        return DatabaseConfig(
            type='sqlserver',
            host=server,
            port=1433,
            name=database,
            username=username,
            password=password,
            driver='ODBC Driver 17 for SQL Server',
            trusted_connection=False
        )

def load_config_from_env() -> DatabaseConfig:
    """Charge la configuration SQL Server depuis les variables d'environnement"""
    return DatabaseConfig(
        type=os.getenv('DB_TYPE', 'sqlserver'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', '1433')),
        name=os.getenv('DB_NAME', 'EduManager'),
        username=os.getenv('DB_USERNAME', ''),
        password=os.getenv('DB_PASSWORD', ''),
        driver=os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server'),
        trusted_connection=os.getenv('DB_TRUSTED_CONNECTION', 'false').lower() == 'true'
    )

# Instructions d'installation et de configuration
INSTALLATION_INSTRUCTIONS = """
Instructions d'installation SQL Server pour EduManager+
======================================================

1. INSTALLATION DE SQL SERVER:
   - Téléchargez SQL Server Express (gratuit) ou SQL Server Developer Edition
   - Installez SQL Server avec les fonctionnalités de base de données
   - Installez SQL Server Management Studio (SSMS) pour la gestion

2. INSTALLATION DU DRIVER ODBC:
   - Téléchargez "Microsoft ODBC Driver 17 for SQL Server"
   - Installez le driver sur votre système

3. CONFIGURATION DE LA BASE DE DONNÉES:
   - Ouvrez SSMS et connectez-vous à votre instance SQL Server
   - Créez une nouvelle base de données nommée "EduManager"
   - Configurez l'authentification (Windows ou SQL Server)

4. INSTALLATION DES DÉPENDANCES PYTHON:
   pip install -r requirements_sqlserver.txt

5. CONFIGURATION DE L'APPLICATION:
   - Modifiez les paramètres dans ce fichier
   - Ou utilisez les variables d'environnement:
     export DB_HOST=votre_serveur
     export DB_NAME=EduManager
     export DB_USERNAME=votre_utilisateur
     export DB_PASSWORD=votre_mot_de_passe

6. EXÉCUTION DE LA MIGRATION:
   python migrate_to_sqlserver.py

7. TEST DE LA CONNEXION:
   python test_sqlserver_connection.py
"""

def print_installation_instructions():
    """Affiche les instructions d'installation"""
    print(INSTALLATION_INSTRUCTIONS)

if __name__ == "__main__":
    print_installation_instructions()
