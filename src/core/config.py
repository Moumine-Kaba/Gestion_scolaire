#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration de l'Application EduManager+
=========================================

Gestion centralisée de la configuration de l'application.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """Configuration de la base de données"""
    type: str = "sqlite"
    host: str = "localhost"
    port: int = 5432
    name: str = "edumanager"
    username: str = ""
    password: str = ""
    path: str = "database/edumanager.db"
    
    def get_connection_string(self) -> str:
        """Retourne la chaîne de connexion"""
        if self.type == "sqlite":
            return f"sqlite:///{self.path}"
        elif self.type == "postgresql":
            return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"
        else:
            raise ValueError(f"Type de base de données non supporté: {self.type}")


@dataclass
class LoggingConfig:
    """Configuration des logs"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file: str = "logs/edumanager.log"
    max_size: int = 10 * 1024 * 1024  # 10 MB
    backup_count: int = 5


@dataclass
class SecurityConfig:
    """Configuration de sécurité"""
    secret_key: str = "your-secret-key-change-in-production"
    session_timeout: int = 3600  # 1 heure
    max_login_attempts: int = 5
    lockout_duration: int = 900  # 15 minutes
    password_min_length: int = 8
    require_special_chars: bool = True


@dataclass
class UIConfig:
    """Configuration de l'interface utilisateur"""
    theme: str = "dark"
    language: str = "fr"
    window_width: int = 1200
    window_height: int = 800
    enable_animations: bool = True
    show_tooltips: bool = True


@dataclass
class Config:
    """Configuration principale de l'application"""
    
    # Informations de base
    app_name: str = "EduManager+"
    version: str = "2.0.0"
    debug: bool = False
    
    # Chemins
    base_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    data_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    logs_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "logs")
    resources_dir: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "resources")
    
    # Sous-configurations
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    ui: UIConfig = field(default_factory=UIConfig)
    
    def __post_init__(self):
        """Initialisation post-création"""
        # Créer les dossiers nécessaires
        self.data_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        self.resources_dir.mkdir(exist_ok=True)
        
        # Charger la configuration depuis l'environnement
        self._load_from_environment()
    
    def _load_from_environment(self):
        """Charge la configuration depuis les variables d'environnement"""
        # Configuration de la base de données
        if os.getenv("DB_TYPE"):
            self.database.type = os.getenv("DB_TYPE")
        if os.getenv("DB_HOST"):
            self.database.host = os.getenv("DB_HOST")
        if os.getenv("DB_PORT"):
            self.database.port = int(os.getenv("DB_PORT"))
        if os.getenv("DB_NAME"):
            self.database.name = os.getenv("DB_NAME")
        if os.getenv("DB_USERNAME"):
            self.database.username = os.getenv("DB_USERNAME")
        if os.getenv("DB_PASSWORD"):
            self.database.password = os.getenv("DB_PASSWORD")
        
        # Configuration de sécurité
        if os.getenv("SECRET_KEY"):
            self.security.secret_key = os.getenv("SECRET_KEY")
        if os.getenv("DEBUG"):
            self.debug = os.getenv("DEBUG").lower() == "true"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertit la configuration en dictionnaire"""
        return {
            "app_name": self.app_name,
            "version": self.version,
            "debug": self.debug,
            "database": {
                "type": self.database.type,
                "host": self.database.host,
                "port": self.database.port,
                "name": self.database.name,
                "path": self.database.path
            },
            "logging": {
                "level": self.logging.level,
                "file": str(self.logging.file)
            },
            "security": {
                "session_timeout": self.security.session_timeout,
                "max_login_attempts": self.security.max_login_attempts
            },
            "ui": {
                "theme": self.ui.theme,
                "language": self.ui.language
            }
        }
    
    def save_to_file(self, file_path: str):
        """Sauvegarde la configuration dans un fichier JSON"""
        config_data = self.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'Config':
        """Charge la configuration depuis un fichier JSON"""
        if not os.path.exists(file_path):
            return cls()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        config = cls()
        
        # Mettre à jour les valeurs
        if "database" in config_data:
            for key, value in config_data["database"].items():
                if hasattr(config.database, key):
                    setattr(config.database, key, value)
        
        if "logging" in config_data:
            for key, value in config_data["logging"].items():
                if hasattr(config.logging, key):
                    setattr(config.logging, key, value)
        
        if "security" in config_data:
            for key, value in config_data["security"].items():
                if hasattr(config.security, key):
                    setattr(config.security, key, value)
        
        if "ui" in config_data:
            for key, value in config_data["ui"].items():
                if hasattr(config.ui, key):
                    setattr(config.ui, key, value)
        
        return config


# Instance globale de configuration
config = Config()

# Fonction utilitaire pour obtenir la configuration
def get_config() -> Config:
    """Retourne l'instance de configuration globale"""
    return config

