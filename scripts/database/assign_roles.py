#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'Assignation des Rôles aux Utilisateurs
EduManager+ - Gestion Scolaire
"""

import os
import sys
import sqlite3

# Ajouter le répertoire racine au path
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

def assign_roles_to_users():
    """Assigne les rôles par défaut aux utilisateurs existants"""
    print("🔐 Assignation des Rôles aux Utilisateurs")
    print("=" * 50)
    
    try:
        db_path = "database/edumanager.db"
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Récupérer tous les utilisateurs
            cursor.execute("SELECT id_utilisateur, username FROM utilisateurs")
            users = cursor.fetchall()
            
            print(f"👥 {len(users)} utilisateurs trouvés")
            
            # Récupérer tous les rôles
            cursor.execute("SELECT id_role, nom FROM roles")
            roles = cursor.fetchall()
            
            print(f"👑 {len(roles)} rôles trouvés")
            
            # Définir les assignations de rôles par défaut
            role_assignments = {
                "admin": "Super Administrateur",
                "directeur": "Directeur",
                "professeur1": "Professeur",
                "professeur2": "Professeur",
                "secretaire": "Secrétaire",
                "eleve1": "Élève",
                "parent1": "Parent"
            }
            
            # Assigner les rôles
            assigned_count = 0
            for user_id, username in users:
                if username in role_assignments:
                    role_name = role_assignments[username]
                    
                    # Trouver l'ID du rôle
                    role_id = None
                    for rid, rname in roles:
                        if rname == role_name:
                            role_id = rid
                            break
                    
                    if role_id:
                        try:
                            # Vérifier si l'assignation existe déjà
                            cursor.execute(
                                "SELECT COUNT(*) FROM user_roles WHERE user_id = ? AND role_id = ?",
                                (user_id, role_id)
                            )
                            exists = cursor.fetchone()[0] > 0
                            
                            if not exists:
                                cursor.execute(
                                    "INSERT INTO user_roles (user_id, role_id) VALUES (?, ?)",
                                    (user_id, role_id)
                                )
                                print(f"✅ {username} -> {role_name}")
                                assigned_count += 1
                            else:
                                print(f"ℹ️ {username} -> {role_name} (déjà assigné)")
                        except Exception as e:
                            print(f"❌ Erreur assignation {username}: {e}")
                    else:
                        print(f"⚠️ Rôle '{role_name}' non trouvé pour {username}")
                else:
                    print(f"ℹ️ Aucun rôle défini pour {username}")
            
            conn.commit()
            print(f"\n🎯 {assigned_count} rôles assignés avec succès")
            
            # Vérifier les assignations
            print("\n📊 Vérification des assignations:")
            cursor.execute('''
                SELECT u.username, r.nom
                FROM user_roles ur
                JOIN utilisateurs u ON ur.user_id = u.id_utilisateur
                JOIN roles r ON ur.role_id = r.id_role
                ORDER BY u.username
            ''')
            
            assignments = cursor.fetchall()
            for username, role_name in assignments:
                print(f"  {username} -> {role_name}")
            
            return True
            
    except Exception as e:
        print(f"❌ Erreur assignation des rôles: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Script d'Assignation des Rôles")
    print("=" * 40)
    
    success = assign_roles_to_users()
    
    if success:
        print("\n🎉 Assignation des rôles terminée avec succès !")
        print("✅ Les utilisateurs ont maintenant des permissions")
    else:
        print("\n❌ Échec de l'assignation des rôles")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
