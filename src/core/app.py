#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Principale EduManager+
==================================

Point d'entrée principal de l'application avec gestion des erreurs et logging.
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os
import sys
import logging
import traceback
from pathlib import Path
from typing import Optional

import customtkinter as ctk
from tkinter import messagebox

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.core.config import get_config, Config
from src.core.exceptions import EduManagerException, ConfigurationError, DatabaseError
from src.core.database.connection 
from database.connection import get_db_connection

class EduManagerApp:
    """Application principale EduManager+"""
    
    def __init__(self):
        """Initialise l'application"""
        self.config = get_config()
        self.logger = self._setup_logging()
        self.database_manager = None
        self.main_window = None
        
        # Configuration de CustomTkinter
        self._setup_ui()
        
        self.logger.info("Application EduManager+ initialisée")
    
    def _setup_logging(self) -> logging.Logger:
        """Configure le système de logging"""
        logger = logging.getLogger("EduManager")
        logger.setLevel(getattr(logging, self.config.logging.level.upper()))
        
        # Créer le dossier de logs s'il n'existe pas
        log_file = Path(self.config.logs_dir) / "edumanager.log"
        log_file.parent.mkdir(exist_ok=True)
        
        # Handler pour fichier
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Handler pour console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(self.config.logging.format)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Ajouter les handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    def _setup_ui(self):
        """Configure l'interface utilisateurs"""
        try:
            # Configuration de CustomTkinter
            ctk.set_appearance_mode(self.config.ui.theme)
            ctk.set_default_color_theme("blue")
            
            # Configuration de la fenêtre principale
            ctk.set_window_scaling(1.0)
            ctk.set_widget_scaling(1.0)
            
            self.logger.info("Interface utilisateurs configurée")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la configuration de l'UI: {e}")
            raise ConfigurationError("Configuration de l'interface utilisateurs", details={"error": str(e)})
    
    def _check_dependencies(self) -> bool:
        """Vérifie que toutes les dépendances sont installées"""
        required_packages = [
            'customtkinter',
            'PIL',
            'matplotlib',
            'sqlite3'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                if package == 'PIL':
                    import PIL
                elif package == 'sqlite3':
                    # Remplacé par SQL Server  # Remplacé par SQL Server
                else:
                    __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            error_msg = f"Packages manquants: {', '.join(missing_packages)}\n\n"
            error_msg += "Veuillez les installer avec:\n"
            error_msg += "pip install " + " ".join(missing_packages)
            
            self.logger.error(f"Dépendances manquantes: {missing_packages}")
            messagebox.showerror("Dépendances manquantes", error_msg)
            return False
        
        self.logger.info("Toutes les dépendances sont installées")
        return True
    
    def _check_database(self) -> bool:
        """Vérifie que la base de données existe et est accessible"""
        try:
            db_path = Path(self.config.database.path)
            
            if not db_path.exists():
                # Créer le dossier database s'il n'existe pas
                db_path.parent.mkdir(exist_ok=True)
                
                # Créer un fichier de base de données vide
                # Remplacé par SQL Server  # Remplacé par SQL Server
                conn = get_db_connection()
                conn.close()
                
                self.logger.info("Base de données créée")
            
            # Tester la connexion
            self.database_manager = get_db_connection())
            self.database_manager.test_connection()
            
            self.logger.info("Base de données accessible")
            return True
            
        except Exception as e:
            self.logger.error(f"Erreur base de données: {e}")
            messagebox.showerror("Erreur Base de Données", f"Impossible d'accéder à la base de données:\n{str(e)}")
            return False
    
    def _show_error_dialog(self, title: str, message: str, error: Optional[Exception] = None):
        """Affiche une boîte de dialogue d'erreur"""
        if error:
            message += f"\n\nDétails techniques:\n{str(error)}"
            if self.config.debug:
                message += f"\n\nTraceback:\n{traceback.format_exc()}"
        
        messagebox.showerror(title, message)
        self.logger.error(f"{title}: {message}")
        if error:
            self.logger.error(f"Exception: {error}")
    
    def _show_warning_dialog(self, title: str, message: str):
        """Affiche une boîte de dialogue d'avertissement"""
        messagebox.showwarning(title, message)
        self.logger.warning(f"{title}: {message}")
    
    def _show_info_dialog(self, title: str, message: str):
        """Affiche une boîte de dialogue d'information"""
        messagebox.showinfo(title, message)
        self.logger.info(f"{title}: {message}")
    
    def start(self):
        """Démarre l'application"""
        try:
            self.logger.info("🚀 Démarrage d'EduManager+...")
            
            # Vérifier les dépendances
            if not self._check_dependencies():
                self.logger.error("❌ Dépendances manquantes")
                return False
            
            # Vérifier la base de données
            if not self._check_database():
                self.logger.error("❌ Erreur base de données")
                return False
            
            self.logger.info("✅ Vérifications terminées")
            
            # Lancer le splash view en premier
            self._launch_splash_view()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du démarrage: {e}")
            self._show_error_dialog("Erreur de Démarrage", "Impossible de démarrer l'application", e)
            return False
    
    def _launch_splash_view(self):
        """Lance la vue de démarrage"""
        try:
            from src.modules.auth.views.splash_view import SplashView
            
            self.logger.info("🚀 Lancement du splash view...")
            self.main_window = SplashView()
            self.main_window.mainloop()
            
        except ImportError as e:
            self.logger.error(f"❌ Erreur d'import: {e}")
            self._show_error_dialog("Erreur d'Import", f"Impossible d'importer le module de démarrage:\n{str(e)}")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du lancement: {e}")
            self._show_error_dialog("Erreur de Lancement", "Impossible de lancer l'interface", e)
    
    def stop(self):
        """Arrête l'application"""
        try:
            self.logger.info("🛑 Arrêt d'EduManager+...")
            
            # Fermer la base de données
            if self.database_manager:
                self.database_manager.close()
            
            # Fermer la fenêtre principale
            if self.main_window:
                self.main_window.quit()
            
            self.logger.info("✅ Application arrêtée proprement")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'arrêt: {e}")
    
    def restart(self):
        """Redémarre l'application"""
        try:
            self.logger.info("🔄 Redémarrage d'EduManager+...")
            
            self.stop()
            self.start()
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du redémarrage: {e}")
            self._show_error_dialog("Erreur de Redémarrage", "Impossible de redémarrer l'application", e)

def main():
    """Point d'entrée principal de l'application"""
    app = None
    
    try:
        # Créer et démarrer l'application
        app = EduManagerApp()
        success = app.start()
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateurs")
        if app:
            app.stop()
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        if app:
            app._show_error_dialog("Erreur Fatale", "Une erreur fatale s'est produite", e)
        sys.exit(1)
        
    finally:
        # Nettoyage final
        if app:
            app.stop()

if __name__ == "__main__":
    main()

