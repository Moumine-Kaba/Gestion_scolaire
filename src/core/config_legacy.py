#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Centralisée - EduManager+
Gestion Scolaire
"""
import os
from pathlib import Path

# ============================================================================
# CONFIGURATION DE BASE
# ============================================================================

# Informations de l'application
APP_NAME = "EduManager+"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Système de Gestion Scolaire Avancé"
APP_AUTHOR = "Équipe EduManager+"
APP_YEAR = "2024"

# ============================================================================
# CHEMINS ET RÉPERTOIRES
# ============================================================================

# Répertoire racine du projet
ROOT_DIR = Path(__file__).parent.absolute()

# Répertoire de la base de données
DATABASE_DIR = ROOT_DIR / "database"
DATABASE_FILE = DATABASE_DIR / "edumanager.db"
DATABASE_PATH = str(DATABASE_FILE)

# Répertoires des modules
MODELS_DIR = ROOT_DIR / "models"
VIEWS_DIR = ROOT_DIR / "views"
ASSETS_DIR = ROOT_DIR / "assets"
LOGS_DIR = ROOT_DIR / "logs"
REPORTS_DIR = ROOT_DIR / "reports"
BACKUPS_DIR = ROOT_DIR / "backups"

# Répertoire des images et icônes
IMAGES_DIR = ASSETS_DIR / "images"
ICONS_DIR = ASSETS_DIR / "icons"

# ============================================================================
# BASE DE DONNÉES
# ============================================================================

# Configuration SQLite
SQLITE_TIMEOUT = 30.0
SQLITE_CHECK_SAME_THREAD = False
SQLITE_ISOLATION_LEVEL = None

# Tables essentielles du système
ESSENTIAL_TABLES = [
    # Tables d'authentification
    'utilisateurs',
    'roles', 
    'user_roles',
    'role_view_permissions',
    'sessions',
    'login_attempts',
    
    # Tables pédagogiques
    'eleves',
    'professeurs',
    'classes',
    'matieres',
    'notes',
    'presences',
    'bulletins',
    
    # Tables administratives
    'parents',
    'salles',
    'enseignements',
    'emplois_temps',
    'paiements'
]

# ============================================================================
# AUTHENTIFICATION ET SÉCURITÉ
# ============================================================================

# Configuration des mots de passe
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL = False

# Configuration des sessions
SESSION_TIMEOUT_HOURS = 24
MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15

# Rôles par défaut
DEFAULT_ROLES = [
    "Super Administrateur",
    "Directeur",
    "Professeur", 
    "Élève",
    "Parent",
    "Secrétaire",
    "Surveillant"
]

# ============================================================================
# INTERFACE UTILISATEUR
# ============================================================================

# Configuration CustomTkinter
CTK_THEME = "dark"  # "light" ou "dark"
CTK_COLOR_SCHEME = "blue"  # "blue", "green", "dark-blue"
CTK_SCALING = 1.0

# Dimensions de l'interface
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
SIDEBAR_WIDTH = 280
MAIN_CONTENT_WIDTH = WINDOW_WIDTH - SIDEBAR_WIDTH

# Couleurs de l'interface
COLORS = {
    'primary': '#1f538d',
    'secondary': '#14375e',
    'accent': '#4CAF50',
    'success': '#4CAF50',
    'warning': '#FF9800',
    'error': '#F44336',
    'info': '#2196F3',
    'light': '#f5f5f5',
    'dark': '#2d2d2d',
    'white': '#ffffff',
    'black': '#000000'
}

# ============================================================================
# PERMISSIONS ET VUES
# ============================================================================

# Types de vues disponibles
VIEW_TYPES = [
    'dashboard',
    'notes',
    'presences', 
    'bulletins',
    'eleves',
    'professeurs',
    'classes',
    'matieres',
    'utilisateurs',
    'roles',
    'parametres',
    'rapports',
    'finance',
    'bibliotheque',
    'calendrier'
]

# Niveaux de permissions
PERMISSION_LEVELS = [
    'none',
    'read',
    'write', 
    'delete',
    'admin'
]

# ============================================================================
# LOGGING ET DÉBOGAGE
# ============================================================================

# Configuration des logs
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = LOGS_DIR / "edumanager.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Mode debug
DEBUG_MODE = False
VERBOSE_LOGGING = False

# ============================================================================
# PERFORMANCE ET LIMITES
# ============================================================================

# Limites de données
MAX_RECORDS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 100
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Timeouts
REQUEST_TIMEOUT = 30
DATABASE_TIMEOUT = 60
UI_UPDATE_INTERVAL = 1000  # ms

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def ensure_directories():
    """Crée tous les répertoires nécessaires"""
    directories = [
        DATABASE_DIR,
        MODELS_DIR,
        VIEWS_DIR,
        ASSETS_DIR,
        IMAGES_DIR,
        ICONS_DIR,
        LOGS_DIR,
        REPORTS_DIR,
        BACKUPS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✅ Répertoire créé/vérifié: {directory}")

def get_asset_path(asset_name: str, asset_type: str = "images") -> Path:
    """Retourne le chemin complet d'un asset"""
    if asset_type == "images":
        return IMAGES_DIR / asset_name
    elif asset_type == "icons":
        return ICONS_DIR / asset_name
    else:
        return ASSETS_DIR / asset_name

def get_database_path() -> str:
    """Retourne le chemin de la base de données"""
    return str(DATABASE_FILE)

def is_development_mode() -> bool:
    """Vérifie si on est en mode développement"""
    return DEBUG_MODE or os.getenv('EDUMANAGER_DEV') == '1'

def get_version_info() -> dict:
    """Retourne les informations de version"""
    return {
        'name': APP_NAME,
        'version': APP_VERSION,
        'description': APP_DESCRIPTION,
        'author': APP_AUTHOR,
        'year': APP_YEAR
    }

# ============================================================================
# INITIALISATION
# ============================================================================

if __name__ == "__main__":
    print(f"🔧 Configuration {APP_NAME} v{APP_VERSION}")
    print("=" * 50)
    
    # Créer les répertoires
    ensure_directories()
    
    # Afficher la configuration
    print(f"\n📁 Répertoire racine: {ROOT_DIR}")
    print(f"🗄️  Base de données: {DATABASE_PATH}")
    print(f"🎨 Thème: {CTK_THEME}")
    print(f"🔐 Rôles: {len(DEFAULT_ROLES)}")
    print(f"👁️  Vues: {len(VIEW_TYPES)}")
    print(f"📊 Tables: {len(ESSENTIAL_TABLES)}")
    
    print("\n✅ Configuration initialisée avec succès !")
else:
    # Créer automatiquement les répertoires au chargement du module
    ensure_directories()
