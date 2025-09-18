# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import os

def get_connection():
    db_path = "database/edumanager.db"
    if not os.path.exists("database"):
        os.makedirs("database")
    return get_db_connection()
