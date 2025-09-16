#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration des Tests EduManager+
==================================

Configuration pytest et fixtures communes pour tous les tests.
"""

import os
import sys
import pytest
import tempfile
import sqlite3
from pathlib import Path
from unittest.mock import Mock, patch

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent
src_path = project_root / "src"

if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


@pytest.fixture(scope="session")
def project_root_path():
    """Retourne le chemin racine du projet"""
    return project_root


@pytest.fixture(scope="session")
def src_path():
    """Retourne le chemin du dossier src"""
    return src_path


@pytest.fixture(scope="session")
def test_data_dir():
    """Retourne le dossier des données de test"""
    return project_root / "tests" / "fixtures"


@pytest.fixture(scope="function")
def temp_db():
    """Crée une base de données temporaire pour les tests"""
    # Créer un fichier temporaire
    temp_file = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    temp_file.close()
    
    # Créer la base de données
    conn = sqlite3.connect(temp_file.name)
    
    # Créer les tables de base
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id_utilateur INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            statut TEXT DEFAULT 'actif',
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS roles (
            id_role INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_role TEXT UNIQUE NOT NULL,
            description TEXT,
            niveau_acces INTEGER DEFAULT 1
        );
        
        CREATE TABLE IF NOT EXISTS user_roles (
            user_id INTEGER,
            role_id INTEGER,
            date_attribution TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES utilisateurs (id_utilateur),
            FOREIGN KEY (role_id) REFERENCES roles (id_role),
            PRIMARY KEY (user_id, role_id)
        );
        
        CREATE TABLE IF NOT EXISTS permissions (
            id_permission INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_permission TEXT UNIQUE NOT NULL,
            description TEXT,
            module TEXT NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS role_permissions (
            role_id INTEGER,
            permission_id INTEGER,
            FOREIGN KEY (role_id) REFERENCES roles (id_role),
            FOREIGN KEY (permission_id) REFERENCES permissions (id_permission),
            PRIMARY KEY (role_id, permission_id)
        );
    """)
    
    # Insérer des données de test
    conn.executescript("""
        INSERT INTO roles (nom_role, description, niveau_acces) VALUES
        ('super_admin', 'Super Administrateur', 10),
        ('admin', 'Administrateur', 8),
        ('directeur', 'Directeur', 7),
        ('professeur', 'Professeur', 5),
        ('secretaire', 'Secrétaire', 4),
        ('eleve', 'Élève', 2),
        ('parent', 'Parent', 1);
        
        INSERT INTO permissions (nom_permission, description, module) VALUES
        ('user_create', 'Créer des utilisateurs', 'auth'),
        ('user_read', 'Lire les utilisateurs', 'auth'),
        ('user_update', 'Modifier les utilisateurs', 'auth'),
        ('user_delete', 'Supprimer les utilisateurs', 'auth'),
        ('role_manage', 'Gérer les rôles', 'auth'),
        ('permission_manage', 'Gérer les permissions', 'auth');
        
        INSERT INTO role_permissions (role_id, permission_id) VALUES
        (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),  -- super_admin
        (2, 1), (2, 2), (2, 3), (2, 5), (2, 6),           -- admin
        (3, 2), (3, 3), (3, 5),                            -- directeur
        (4, 2), (4, 3),                                    -- professeur
        (5, 2), (5, 3),                                    -- secretaire
        (6, 2),                                             -- eleve
        (7, 2);                                             -- parent
    """)
    
    conn.commit()
    conn.close()
    
    yield temp_file.name
    
    # Nettoyer
    try:
        os.unlink(temp_file.name)
    except:
        pass


@pytest.fixture(scope="function")
def mock_config():
    """Mock de la configuration pour les tests"""
    with patch('src.core.config.get_config') as mock:
        config = Mock()
        config.database.path = "test.db"
        config.debug = True
        config.logging.level = "DEBUG"
        config.security.secret_key = "test-secret-key"
        config.ui.theme = "dark"
        mock.return_value = config
        yield config


@pytest.fixture(scope="function")
def mock_logger():
    """Mock du logger pour les tests"""
    with patch('logging.getLogger') as mock:
        logger = Mock()
        mock.return_value = logger
        yield logger


@pytest.fixture(scope="function")
def sample_user_data():
    """Données d'utilisateur de test"""
    return {
        "username": "testuser",
        "password": "testpass123",
        "nom": "Test",
        "prenom": "User",
        "email": "test@example.com",
        "statut": "actif"
    }


@pytest.fixture(scope="function")
def sample_role_data():
    """Données de rôle de test"""
    return {
        "nom_role": "test_role",
        "description": "Rôle de test",
        "niveau_acces": 5
    }


@pytest.fixture(scope="function")
def sample_permission_data():
    """Données de permission de test"""
    return {
        "nom_permission": "test_permission",
        "description": "Permission de test",
        "module": "test"
    }


@pytest.fixture(scope="function")
def mock_database_connection():
    """Mock de la connexion à la base de données"""
    with patch('src.core.database.connection.DatabaseManager') as mock:
        db_manager = Mock()
        db_manager.connect.return_value = True
        db_manager.test_connection.return_value = True
        db_manager.get_connection_string.return_value = "sqlite:///test.db"
        mock.return_value = db_manager
        yield db_manager


@pytest.fixture(scope="function")
def mock_customtkinter():
    """Mock de CustomTkinter pour les tests"""
    with patch('customtkinter.set_appearance_mode'), \
         patch('customtkinter.set_default_color_theme'), \
         patch('customtkinter.set_window_scaling'), \
         patch('customtkinter.set_widget_scaling'):
        yield


@pytest.fixture(scope="function")
def mock_tkinter():
    """Mock de tkinter pour les tests"""
    with patch('tkinter.messagebox.showerror'), \
         patch('tkinter.messagebox.showwarning'), \
         patch('tkinter.messagebox.showinfo'):
        yield


# Configuration pytest
def pytest_configure(config):
    """Configuration pytest personnalisée"""
    # Ajouter des marqueurs personnalisés
    config.addinivalue_line(
        "markers", "slow: marque les tests lents"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "unit: marque les tests unitaires"
    )


def pytest_collection_modifyitems(config, items):
    """Modifie la collection des tests"""
    for item in items:
        # Marquer automatiquement les tests selon leur emplacement
        if "test_models" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_services" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_controllers" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        else:
            item.add_marker(pytest.mark.unit)


# Utilitaires de test
class TestUtils:
    """Utilitaires pour les tests"""
    
    @staticmethod
    def assert_dict_contains(dict1, dict2):
        """Vérifie que dict1 contient toutes les clés de dict2"""
        for key, value in dict2.items():
            assert key in dict1, f"Clé '{key}' manquante dans dict1"
            assert dict1[key] == value, f"Valeur différente pour la clé '{key}': {dict1[key]} != {value}"
    
    @staticmethod
    def assert_list_contains(list1, list2):
        """Vérifie que list1 contient tous les éléments de list2"""
        for item in list2:
            assert item in list1, f"Élément '{item}' manquant dans list1"
    
    @staticmethod
    def create_mock_user(**kwargs):
        """Crée un utilisateur mock avec des valeurs par défaut"""
        default_user = {
            "id_utilateur": 1,
            "username": "testuser",
            "password_hash": "hashed_password",
            "nom": "Test",
            "prenom": "User",
            "email": "test@example.com",
            "statut": "actif",
            "date_creation": "2024-01-01 00:00:00"
        }
        default_user.update(kwargs)
        return default_user


# Fixture pour les utilitaires de test
@pytest.fixture
def test_utils():
    """Retourne les utilitaires de test"""
    return TestUtils

