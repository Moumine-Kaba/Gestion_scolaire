#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test simple pour vérifier que l'application fonctionne
"""

import sqlite3
from pathlib import Path

def test_application():
    """Test simple de l'application"""
    print("🧪 Test de l'application EduManager+")
    print("=" * 50)
    
    # Vérifier la base de données
    db_path = Path(__file__).parent / "database" / "edumanager.db"
    print(f"📁 Base de données: {db_path}")
    
    try:
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        
        # Vérifier la table utilisateurs
        cursor.execute("PRAGMA table_info(utilisateurs)")
        columns = cursor.fetchall()
        print("📋 Structure de la table utilisateurs:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Vérifier les utilisateurs existants
        cursor.execute("SELECT id_utilisateur, nom_utilisateur, nom, prenom FROM utilisateurs LIMIT 5")
        users = cursor.fetchall()
        print(f"\n👤 Utilisateurs trouvés: {len(users)}")
        for user in users:
            print(f"  - {user[1]} ({user[2]} {user[3]})")
        
        conn.close()
        
        print("\n✅ Base de données OK")
        print("🚀 L'application devrait fonctionner maintenant")
        print("\nUtilisateurs de test disponibles:")
        print("• directeur / directeur123")
        print("• comptable / comptable123") 
        print("• secretaire / secretaire123")
        print("• surveillant / surveillant123")
        print("• admin / admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_application()
