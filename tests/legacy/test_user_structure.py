#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from models.auth import AuthManager

def test_user_structure():
    try:
        auth = AuthManager('database/edumanager.db')
        user = auth.authenticate_user('admin', 'admin123')
        
        if user:
            print("✅ Authentification réussie")
            print("Structure utilisateur admin:")
            for k, v in user.items():
                print(f"  {k}: {v}")
        else:
            print("❌ Échec authentification")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_user_structure()
