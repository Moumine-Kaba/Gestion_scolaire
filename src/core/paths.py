# -*- coding: utf-8 -*-
"""
Configuration centralisée des chemins pour EduManager+
- Base de données centralisée
- Thème global
- Icônes centralisées
"""

import os
import sys
from database.connection import get_db_connection

def get_project_root():
    """Retourne le chemin racine du projet"""
    current_file = os.path.abspath(__file__)
    # Remonter depuis src/core/paths.py vers la racine
    return os.path.dirname(os.path.dirname(os.path.dirname(current_file)))

def get_database_path():
    """Retourne le chemin vers la base de données centralisée"""
    return os.path.join(get_project_root(), "database", "edumanager.db")

def get_icons_path():
    """Retourne le chemin vers le dossier des icônes"""
    return os.path.join(get_project_root(), "resources", "icons")

def get_theme_path():
    """Retourne le chemin vers le fichier de thème"""
    return os.path.join(get_project_root(), "resources", "themes", "theme.py")

def get_resources_path():
    """Retourne le chemin vers le dossier resources"""
    return os.path.join(get_project_root(), "resources")

# Chemins centralisés
PROJECT_ROOT = get_project_root()
DATABASE_PATH = get_database_path()
ICONS_PATH = get_icons_path()
THEME_PATH = get_theme_path()
RESOURCES_PATH = get_resources_path()

# Configuration pour l'import du thème
def setup_theme_import():
    """Configure l'import du thème global"""
    try:
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        
        # Import du thème global
        import resources.themes.theme as theme_module
        print("✅ Thème global importé depuis resources/themes/theme.py")
        return True
    except ImportError as e:
        print(f"⚠️ Erreur import thème: {e}")
        return False

# Configuration pour les icônes
def get_icon_path(icon_name):
    """Retourne le chemin complet vers une icône"""
    return os.path.join(ICONS_PATH, f"{icon_name}.png")

def icon_exists(icon_name):
    """Vérifie si une icône existe"""
    return os.path.exists(get_icon_path(icon_name))

# Configuration pour la base de données
# La fonction get_db_connection est maintenant importée directement depuis database.connection

# Affichage des chemins pour debug
def print_paths():
    """Affiche tous les chemins configurés"""
    print("=== CHEMINS CENTRALISÉS EDUMANAGER+ ===")
    print(f"📁 Racine projet: {PROJECT_ROOT}")
    print(f"🗄️ Base de données: {DATABASE_PATH}")
    print(f"🎨 Dossier icônes: {ICONS_PATH}")
    print(f"🎭 Fichier thème: {THEME_PATH}")
    print(f"📦 Dossier resources: {RESOURCES_PATH}")
    print("=" * 40)

if __name__ == "__main__":
    print_paths()
