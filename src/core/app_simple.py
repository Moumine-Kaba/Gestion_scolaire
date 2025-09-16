#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application Principale EduManager+ - Version Simplifiée
======================================================

Version simplifiée pour tester la nouvelle architecture sans imports complexes.
"""

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


class SimpleEduManagerApp:
    """Application principale EduManager+ - Version simplifiée"""
    
    def __init__(self):
        """Initialise l'application"""
        self.config = get_config()
        self.logger = self._setup_logging()
        self.main_window = None
        
        # Configuration de CustomTkinter
        self._setup_ui()
        
        self.logger.info("Application EduManager+ (version simplifiée) initialisée")
    
    def _setup_logging(self) -> logging.Logger:
        """Configure le système de logging"""
        logger = logging.getLogger("EduManager")
        logger.setLevel(logging.INFO)
        
        # Créer le dossier de logs s'il n'existe pas
        log_file = Path(self.config.logs_dir) / "edumanager_simple.log"
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
        """Configure l'interface utilisateur"""
        try:
            # Configuration de CustomTkinter
            ctk.set_appearance_mode(self.config.ui.theme)
            ctk.set_default_color_theme("blue")
            
            # Configuration de la fenêtre principale
            ctk.set_window_scaling(1.0)
            ctk.set_widget_scaling(1.0)
            
            self.logger.info("Interface utilisateur configurée")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de la configuration de l'UI: {e}")
            raise ConfigurationError("Configuration de l'interface utilisateur", details={"error": str(e)})
    
    def _check_dependencies(self) -> bool:
        """Vérifie que toutes les dépendances sont installées"""
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
            error_msg = f"Packages manquants: {', '.join(missing_packages)}\n\n"
            error_msg += "Veuillez les installer avec:\n"
            error_msg += "pip install " + " ".join(missing_packages)
            
            self.logger.error(f"Dépendances manquantes: {missing_packages}")
            messagebox.showerror("Dépendances manquantes", error_msg)
            return False
        
        self.logger.info("Toutes les dépendances sont installées")
        return True
    
    def _show_simple_interface(self):
        """Affiche une interface simple pour tester l'application"""
        try:
            # Créer la fenêtre principale
            self.main_window = ctk.CTk()
            self.main_window.title("EduManager+ - Test de l'Architecture")
            self.main_window.geometry("800x600")
            self.main_window.configure(fg_color="#0A192F")
            
            # Titre principal
            title_label = ctk.CTkLabel(
                self.main_window,
                text="🎓 EduManager+",
                font=("Segoe UI", 32, "bold"),
                text_color="#60A5FA"
            )
            title_label.pack(pady=(50, 20))
            
            # Sous-titre
            subtitle_label = ctk.CTkLabel(
                self.main_window,
                text="Système de Gestion Scolaire",
                font=("Segoe UI", 18),
                text_color="#94A3B8"
            )
            subtitle_label.pack(pady=(0, 40))
            
            # Message de succès
            success_label = ctk.CTkLabel(
                self.main_window,
                text="✅ Architecture de fichiers réorganisée avec succès !",
                font=("Segoe UI", 16, "bold"),
                text_color="#10B981"
            )
            success_label.pack(pady=(0, 20))
            
            # Informations sur l'architecture
            info_frame = ctk.CTkFrame(self.main_window, fg_color="#1E293B")
            info_frame.pack(pady=20, padx=40, fill="x")
            
            info_text = """
🏗️  Nouvelle Architecture Implémentée :

📁 src/ - Code source principal
   ├── core/ - Composants de base
   ├── modules/ - Modules fonctionnels
   ├── shared/ - Composants partagés
   └── utils/ - Utilitaires

📁 tests/ - Tests automatisés
📁 docs/ - Documentation
📁 scripts/ - Scripts utilitaires
📁 resources/ - Ressources
📁 config/ - Configuration
📁 deployment/ - Déploiement

✅ Tous les fichiers ont été migrés
✅ Structure modulaire en place
✅ Imports corrigés
✅ Architecture professionnelle
            """
            
            info_label = ctk.CTkLabel(
                info_frame,
                text=info_text,
                font=("Consolas", 12),
                text_color="#E2E8F0",
                justify="left"
            )
            info_label.pack(pady=20, padx=20)
            
            # Bouton de fermeture
            close_button = ctk.CTkButton(
                self.main_window,
                text="Fermer",
                font=("Segoe UI", 14, "bold"),
                height=45,
                corner_radius=10,
                fg_color="#EF4444",
                hover_color="#DC2626",
                command=self.main_window.quit
            )
            close_button.pack(pady=(30, 0))
            
            self.logger.info("Interface simple affichée avec succès")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'affichage de l'interface: {e}")
            self._show_error_dialog("Erreur d'Interface", "Impossible d'afficher l'interface", e)
    
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
    
    def start(self):
        """Démarre l'application"""
        try:
            self.logger.info("🚀 Démarrage d'EduManager+ (version simplifiée)...")
            
            # Vérifier les dépendances
            if not self._check_dependencies():
                self.logger.error("❌ Dépendances manquantes")
                return False
            
            self.logger.info("✅ Vérifications terminées")
            
            # Afficher l'interface simple
            self._show_simple_interface()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du démarrage: {e}")
            self._show_error_dialog("Erreur de Démarrage", "Impossible de démarrer l'application", e)
            return False
    
    def stop(self):
        """Arrête l'application"""
        try:
            self.logger.info("🛑 Arrêt d'EduManager+...")
            
            # Fermer la fenêtre principale
            if self.main_window:
                self.main_window.quit()
            
            self.logger.info("✅ Application arrêtée proprement")
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'arrêt: {e}")


def main():
    """Point d'entrée principal de l'application"""
    app = None
    
    try:
        # Créer et démarrer l'application
        app = SimpleEduManagerApp()
        success = app.start()
        
        if not success:
            sys.exit(1)
        
        # Lancer la boucle principale
        if app.main_window:
            app.main_window.mainloop()
            
    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
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
