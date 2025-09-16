#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Démarrage EduManager+
===============================

Script principal pour démarrer l'application avec gestion des erreurs.
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def setup_environment():
    """Configure l'environnement de l'application"""
    # Variables d'environnement
    os.environ.setdefault("EDUMANAGER_ENV", "development")
    os.environ.setdefault("EDUMANAGER_DEBUG", "true")
    
    # Chemin de travail
    os.chdir(project_root)
    
    print(f"🏗️  Environnement configuré:")
    print(f"   - Dossier projet: {project_root}")
    print(f"   - Environnement: {os.environ['EDUMANAGER_ENV']}")
    print(f"   - Debug: {os.environ['EDUMANAGER_DEBUG']}")

def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    
    print(f"✅ Version Python: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Vérifie les dépendances principales"""
    required_packages = [
        'customtkinter',
        'PIL',
        'matplotlib'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Packages manquants: {', '.join(missing_packages)}")
        print("   Installez-les avec: pip install -r deployment/requirements/requirements.txt")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def setup_logging():
    """Configure le système de logging"""
    # Créer le dossier de logs
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "startup.log", encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Système de logging configuré")
    return logger

def main():
    """Fonction principale"""
    print("🚀 Démarrage d'EduManager+")
    print("=" * 50)
    
    try:
        # Vérifications préliminaires
        if not check_python_version():
            sys.exit(1)
        
        if not check_dependencies():
            sys.exit(1)
        
        # Configuration de l'environnement
        setup_environment()
        
        # Configuration du logging
        logger = setup_logging()
        
        # Import et démarrage de l'application
        logger.info("Import de l'application principale...")
        
        try:
            from src.core.app import main as app_main
            logger.info("Application importée avec succès")
            
            # Démarrer l'application
            logger.info("Démarrage de l'application...")
            app_main()
            
        except ImportError as e:
            logger.error(f"Erreur d'import: {e}")
            print(f"❌ Erreur d'import: {e}")
            print("   Vérifiez que la nouvelle architecture est en place")
            print("   Exécutez: python migrate_to_new_architecture.py")
            sys.exit(1)
            
        except Exception as e:
            logger.error(f"Erreur lors du démarrage: {e}")
            print(f"❌ Erreur lors du démarrage: {e}")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

