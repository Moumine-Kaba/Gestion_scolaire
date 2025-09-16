#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration de l'Environnement de Développement
================================================

Configuration spécifique pour le développement local.
"""

import os
from pathlib import Path

# Configuration de base
DEBUG = True
TESTING = False

# Base de données
DATABASE = {
    "type": "sqlite",
    "path": "database/edumanager_dev.db",
    "echo": True,  # Log des requêtes SQL
}

# Logging
LOGGING = {
    "level": "DEBUG",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "logs/edumanager_dev.log",
}

# Sécurité
SECURITY = {
    "secret_key": "dev-secret-key-change-in-production",
    "session_timeout": 7200,  # 2 heures en dev
    "debug_toolbar": True,
}

# Interface utilisateur
UI = {
    "theme": "dark",
    "language": "fr",
    "enable_animations": True,
    "show_debug_info": True,
}

# Développement
DEVELOPMENT = {
    "auto_reload": True,
    "show_sql_queries": True,
    "enable_profiling": False,
    "mock_external_services": True,
}

