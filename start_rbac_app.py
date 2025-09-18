#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de démarrage complet pour EduManager+ avec RBAC
Initialise le système RBAC et lance l'application avec tous les composants intégrés
"""

import os
import sys
import sqlite3
from pathlib import Path
import customtkinter as ctk

# Configuration du thème
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Ajouter le répertoire src au path
project_root = Path(__file__).resolve().parent
src_dir = project_root / "src"
if str(src_dir) not in sys.path:
    sys.path.append(str(src_dir))

def init_rbac_system():
    """Initialise le système RBAC"""
    print("🔧 Initialisation du système RBAC...")
    
    try:
        from src.modules.auth.models.rbac_system import RBACSystem
        
        db_path = project_root / "database" / "edumanager.db"
        rbac = RBACSystem(str(db_path), dev_mode=False)
        
        print("✅ Système RBAC initialisé avec succès")
        return rbac
    except Exception as e:
        print(f"❌ Erreur initialisation RBAC: {e}")
        return None

def verify_users_exist():
    """Vérifie que les utilisateurs RBAC existent"""
    print("👥 Vérification des utilisateurs...")
    
    try:
        db_path = project_root / "database" / "edumanager.db"
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        
        # Vérifier la table utilisateurs
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='utilisateurs'")
        if not cursor.fetchone():
            print("❌ Table utilisateurs manquante")
            conn.close()
            return False
        
        # Compter les utilisateurs
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        user_count = cursor.fetchone()[0]
        
        # Vérifier les rôles RBAC
        cursor.execute("SELECT COUNT(*) FROM rbac_roles")
        role_count = cursor.fetchone()[0]
        
        # Vérifier les attributions de rôles
        cursor.execute("SELECT COUNT(*) FROM rbac_user_roles")
        assignment_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ {user_count} utilisateurs trouvés")
        print(f"✅ {role_count} rôles configurés")
        print(f"✅ {assignment_count} attributions de rôles")
        
        return user_count > 0 and role_count > 0 and assignment_count > 0
        
    except Exception as e:
        print(f"❌ Erreur vérification utilisateurs: {e}")
        return False

def create_default_users_if_needed():
    """Crée les utilisateurs par défaut si nécessaire"""
    print("👤 Création des utilisateurs par défaut...")
    
    try:
        db_path = project_root / "database" / "edumanager.db"
        
        # Vérifier si des utilisateurs existent déjà
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM utilisateurs")
        user_count = cursor.fetchone()[0]
        conn.close()
        
        if user_count > 0:
            print("✅ Utilisateurs déjà existants")
            return True
        
        # Créer la table utilisateurs si elle n'existe pas
        conn = sqlite3.connect(str(db_path), timeout=30)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS utilisateurs (
                id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_utilisateur TEXT UNIQUE NOT NULL,
                mot_de_passe TEXT NOT NULL,
                email TEXT,
                nom TEXT,
                prenom TEXT,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                derniere_connexion TIMESTAMP,
                est_actif BOOLEAN DEFAULT 1
            )
        ''')
        conn.commit()
        conn.close()
        
        # Initialiser RBAC
        from src.modules.auth.models.rbac_system import RBACSystem
        rbac = RBACSystem(str(db_path), dev_mode=False)
        
        # Créer les utilisateurs par défaut
        users_data = [
            {"username": "directeur", "password": "directeur123", "email": "directeur@ecole.com", "nom": "Dupont", "prenom": "Jean", "roles": "Directeur"},
            {"username": "comptable", "password": "comptable123", "email": "comptable@ecole.com", "nom": "Martin", "prenom": "Marie", "roles": "Comptable"},
            {"username": "secretaire", "password": "secretaire123", "email": "secretaire@ecole.com", "nom": "Bernard", "prenom": "Sophie", "roles": "Secrétaire"},
            {"username": "surveillant", "password": "surveillant123", "email": "surveillant@ecole.com", "nom": "Petit", "prenom": "Pierre", "roles": "Surveillant"},
            {"username": "admin", "password": "admin123", "email": "admin@ecole.com", "nom": "Administrateur", "prenom": "Système", "roles": "Directeur"}
        ]
        
        created_count = 0
        for user_data in users_data:
            try:
                conn = sqlite3.connect(str(db_path), timeout=30)
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, email, nom, prenom)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_data["username"], user_data["password"], user_data["email"], user_data["nom"], user_data["prenom"]))
                user_id = cursor.lastrowid
                conn.commit()
                conn.close()
                
                if rbac.assign_role_to_user(user_id, user_data["roles"]):
                    print(f"✅ {user_data['username']} ({user_data['nom']} {user_data['prenom']}) → {user_data['roles']}")
                    created_count += 1
                else:
                    print(f"❌ Échec attribution rôle pour {user_data['username']}")
            except Exception as e:
                print(f"❌ Erreur création utilisateurs {user_data['username']}: {e}")
        
        print(f"✅ {created_count} utilisateurs créés avec leurs rôles")
        return created_count > 0
        
    except Exception as e:
        print(f"❌ Erreur création utilisateurs: {e}")
        return False

def launch_login():
    """Lance l'interface de login avec RBAC intégré"""
    print("🚀 Lancement de l'interface de login...")
    
    try:
        from src.modules.auth.views.login_view import LoginViewModern
        
        # Lancer la vue de login
        login_window = LoginViewModern()
        login_window.mainloop()
        
    except Exception as e:
        print(f"❌ Erreur lancement login: {e}")
        # Fallback vers une interface simple
        launch_simple_login()

def launch_simple_login():
    """Interface de login simple en cas d'erreur"""
    print("⚠️ Utilisation de l'interface de login simple...")
    
    class SimpleLogin(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("EduManager+ | Connexion Simple")
            self.geometry("400x300")
            
            # Centrer la fenêtre
            self.update_idletasks()
            x = (self.winfo_screenwidth() // 2) - (400 // 2)
            y = (self.winfo_screenheight() // 2) - (300 // 2)
            self.geometry(f"400x300+{x}+{y}")
            
            # Interface simple
            ctk.CTkLabel(self, text="EduManager+", font=("Segoe UI", 24, "bold")).pack(pady=20)
            ctk.CTkLabel(self, text="Connexion", font=("Segoe UI", 16)).pack(pady=10)
            
            # Champs de saisie
            self.username_var = ctk.StringVar()
            self.password_var = ctk.StringVar()
            
            ctk.CTkEntry(self, textvariable=self.username_var, placeholder_text="Nom d'utilisateurs").pack(pady=10, padx=20)
            ctk.CTkEntry(self, textvariable=self.password_var, placeholder_text="Mot de passe", show="*").pack(pady=10, padx=20)
            
            # Bouton de connexion
            ctk.CTkButton(self, text="Se connecter", command=self.login).pack(pady=20)
            
            # Informations de connexion
            info_text = """
Utilisateurs disponibles:
• directeur / directeur123 (Directeur)
• comptable / comptable123 (Comptable)
• secretaire / secretaire123 (Secrétaire)
• surveillant / surveillant123 (Surveillant)
• admin / admin123 (Directeur)
            """
            ctk.CTkLabel(self, text=info_text, font=("Segoe UI", 10), justify="left").pack(pady=10)
        
        def login(self):
            username = self.username_var.get()
            password = self.password_var.get()
            
            if self.authenticate_user(username, password):
                self.destroy()
                self.launch_dashboard(username)
            else:
                from tkinter import messagebox
                messagebox.showerror("Erreur", "Identifiants incorrects")
        
        def authenticate_user(self, username, password):
            try:
                db_path = project_root / "database" / "edumanager.db"
                conn = sqlite3.connect(str(db_path), timeout=30)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id_utilisateur, nom_utilisateur, nom, prenom, email
                    FROM utilisateurs 
                    WHERE nom_utilisateur = ? AND mot_de_passe = ?
                ''', (username, password))
                
                user_row = cursor.fetchone()
                conn.close()
                
                if user_row:
                    user_id, username, nom, prenom, email = user_row
                    
                    # Récupérer le rôle RBAC
                    from src.modules.auth.models.rbac_system import RBACSystem
                    rbac = RBACSystem(str(db_path), dev_mode=False)
                    user_role = rbac.get_user_role(user_id)
                    
                    self.user_info = {
                        "id": user_id,
                        "username": username,
                        "full_name": f"{nom} {prenom}" if nom and prenom else username,
                        "roles": user_role.name if user_role else "Utilisateur",
                        "rbac_role": user_role,
                        "rbac_system": rbac,
                        "email": email
                    }
                    return True
                
                return False
                
            except Exception as e:
                print(f"Erreur authentification: {e}")
                return False
        
        def launch_dashboard(self, username):
            try:
                from src.modules.auth.views.dashboard_view import MainApp
                app = MainApp(self.user_info)
                app.mainloop()
            except Exception as e:
                print(f"Erreur lancement dashboard: {e}")
                from tkinter import messagebox
                messagebox.showerror("Erreur", f"Impossible de lancer le dashboard: {e}")
    
    login_window = SimpleLogin()
    login_window.mainloop()

def main():
    """Fonction principale"""
    print("🚀 Démarrage d'EduManager+ avec RBAC")
    print("=" * 50)
    
    # 1. Initialiser le système RBAC
    rbac = init_rbac_system()
    if not rbac:
        print("❌ Impossible d'initialiser le système RBAC")
        return
    
    # 2. Créer les utilisateurs par défaut si nécessaire
    if not verify_users_exist():
        if not create_default_users_if_needed():
            print("❌ Impossible de créer les utilisateurs par défaut")
            return
    
    # 3. Lancer l'interface de login
    print("\n✅ Système prêt ! Lancement de l'interface...")
    launch_login()

if __name__ == "__main__":
    main()
