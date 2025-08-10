import sqlite3
import os

def get_connection():
    db_path = "database/edumanager.db"
    if not os.path.exists("database"):
        os.makedirs("database")
    return sqlite3.connect(db_path)
