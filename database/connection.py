import pyodbc
import os
from src.core.database.sqlserver_connection import SQLServerManager

# Configuration SQL Server
SQLSERVER_CONFIG = {
    'type': 'sqlserver',
    'host': '.',
    'port': 1433,
    'name': 'EduManager',
    'username': '',
    'password': '',
    'driver': 'ODBC Driver 17 for SQL Server',
    'trusted_connection': True
}

# Instance globale du gestionnaire de base de données
db_manager = SQLServerManager(
    server=SQLSERVER_CONFIG['host'],
    database=SQLSERVER_CONFIG['name'],
    username=SQLSERVER_CONFIG['username'],
    password=SQLSERVER_CONFIG['password'],
    driver=SQLSERVER_CONFIG['driver'],
    trusted_connection=SQLSERVER_CONFIG['trusted_connection']
)

def connect_db():
    """Fonction pour obtenir une connexion à la base de données SQL Server."""
    if not db_manager.is_connected():
        db_manager.connect()
    return db_manager

def get_db_connection():
    """Fonction pour obtenir une connexion à la base de données."""
    # Éviter la récursion en créant une nouvelle connexion directement
    try:
        import pyodbc
        
        # Construire la chaîne de connexion pyodbc
        if SQLSERVER_CONFIG['trusted_connection']:
            connection_string = (
                f"DRIVER={{{SQLSERVER_CONFIG['driver']}}};"
                f"SERVER={SQLSERVER_CONFIG['host']};"
                f"DATABASE={SQLSERVER_CONFIG['name']};"
                f"Trusted_Connection=yes;"
            )
        else:
            connection_string = (
                f"DRIVER={{{SQLSERVER_CONFIG['driver']}}};"
                f"SERVER={SQLSERVER_CONFIG['host']};"
                f"DATABASE={SQLSERVER_CONFIG['name']};"
                f"UID={SQLSERVER_CONFIG['username']};"
                f"PWD={SQLSERVER_CONFIG['password']};"
            )
        
        conn = pyodbc.connect(connection_string)
        return conn
        
    except Exception as e:
        print(f"❌ Erreur connexion pyodbc: {e}")
        return None

def create_all_tables():
    """Les tables sont déjà créées dans SQL Server lors de la migration."""
    print("✅ Tables SQL Server déjà créées lors de la migration !")