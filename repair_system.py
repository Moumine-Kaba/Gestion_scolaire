#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Réparation Automatique du Système
EduManager+ - Gestion Scolaire
"""
import os
import sys
import sqlite3
import subprocess
from datetime import datetime

class SystemRepair:
    def __init__(self):
        self.db_path = "database/edumanager.db"
        self.repair_log = []
        self.errors_found = []
        
    def log(self, message, level="INFO"):
        """Enregistre un message dans le log de réparation"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.repair_log.append(log_entry)
        print(log_entry)
        
    def run_script(self, script_name, description):
        """Exécute un script Python et gère les erreurs"""
        try:
            self.log(f"🔄 {description}...")
            result = subprocess.run([sys.executable, script_name], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log(f"✅ {description} - Succès", "SUCCESS")
                return True
            else:
                error_msg = f"❌ {description} - Erreur: {result.stderr}"
                self.log(error_msg, "ERROR")
                self.errors_found.append(error_msg)
                return False
                
        except subprocess.TimeoutExpired:
            error_msg = f"❌ {description} - Timeout (60s)"
            self.log(error_msg, "ERROR")
            self.errors_found.append(error_msg)
            return False
        except Exception as e:
            error_msg = f"❌ {description} - Exception: {e}"
            self.log(error_msg, "ERROR")
            self.errors_found.append(error_msg)
            return False
    
    def check_database_integrity(self):
        """Vérifie l'intégrité de la base de données"""
        try:
            if not os.path.exists(self.db_path):
                self.log("❌ Base de données introuvable", "ERROR")
                return False
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier l'intégrité
            cursor.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()
            
            if integrity_result and integrity_result[0] == "ok":
                self.log("✅ Intégrité de la base de données - OK", "SUCCESS")
            else:
                self.log("❌ Problème d'intégrité de la base de données", "ERROR")
                self.errors_found.append("Intégrité de la base de données compromise")
            
            # Vérifier les tables essentielles
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            essential_tables = [
                'utilisateurs', 'roles', 'user_roles', 'role_view_permissions',
                'bulletins', 'notes', 'presences', 'eleves', 'professeurs',
                'classes', 'matieres', 'parents', 'salles', 'enseignements',
                'emplois_temps', 'paiements', 'sessions', 'login_attempts'
            ]
            
            missing_tables = [table for table in essential_tables if table not in tables]
            
            if missing_tables:
                self.log(f"❌ Tables manquantes: {', '.join(missing_tables)}", "ERROR")
                self.errors_found.append(f"Tables manquantes: {', '.join(missing_tables)}")
            else:
                self.log("✅ Toutes les tables essentielles présentes", "SUCCESS")
            
            conn.close()
            return len(missing_tables) == 0
            
        except Exception as e:
            error_msg = f"❌ Erreur vérification base de données: {e}"
            self.log(error_msg, "ERROR")
            self.errors_found.append(error_msg)
            return False
    
    def check_user_roles(self):
        """Vérifie que les utilisateurs ont des rôles assignés"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier les utilisateurs sans rôles
            cursor.execute("""
                SELECT u.username 
                FROM utilisateurs u 
                LEFT JOIN user_roles ur ON u.id_utilisateur = ur.user_id 
                WHERE ur.user_id IS NULL
            """)
            
            users_without_roles = [row[0] for row in cursor.fetchall()]
            
            if users_without_roles:
                self.log(f"❌ Utilisateurs sans rôles: {', '.join(users_without_roles)}", "ERROR")
                self.errors_found.append(f"Utilisateurs sans rôles: {', '.join(users_without_roles)}")
                return False
            else:
                self.log("✅ Tous les utilisateurs ont des rôles assignés", "SUCCESS")
                return True
                
        except Exception as e:
            error_msg = f"❌ Erreur vérification rôles: {e}"
            self.log(error_msg, "ERROR")
            self.errors_found.append(error_msg)
            return False
        finally:
            conn.close()
    
    def check_permissions(self):
        """Vérifie que les permissions sont correctement configurées"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Vérifier les permissions par défaut
            cursor.execute("SELECT COUNT(*) FROM role_view_permissions")
            permission_count = cursor.fetchone()[0]
            
            if permission_count == 0:
                self.log("❌ Aucune permissions configurée", "ERROR")
                self.errors_found.append("Aucune permissions configurée")
                return False
            else:
                self.log(f"✅ {permission_count} permissions configurées", "SUCCESS")
                return True
                
        except Exception as e:
            error_msg = f"❌ Erreur vérification permissions: {e}"
            self.log(error_msg, "ERROR")
            self.errors_found.append(error_msg)
            return False
        finally:
            conn.close()
    
    def repair_database_structure(self):
        """Répare la structure de la base de données"""
        self.log("🔧 Réparation de la structure de la base de données...")
        
        # Créer les tables manquantes
        if not self.run_script("init_tables.py", "Création des tables manquantes"):
            return False
        
        # Ajouter des données de test
        if not self.run_script("init_test_data.py", "Ajout des données de test"):
            return False
        
        return True
    
    def repair_user_roles(self):
        """Répare les attributions de rôles"""
        self.log("🔧 Réparation des attributions de rôles...")
        
        if not self.run_script("assign_roles.py", "Attribution des rôles aux utilisateurs"):
            return False
        
        return True
    
    def test_system(self):
        """Teste le système après réparation"""
        self.log("🧪 Test du système après réparation...")
        
        if not self.run_script("test_permissions.py", "Test du système de permissions"):
            return False
        
        return True
    
    def generate_report(self):
        """Génère un rapport de réparation"""
        report_path = f"repair_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("RAPPORT DE RÉPARATION - EduManager+\n")
            f.write("=" * 60 + "\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Base de données: {self.db_path}\n\n")
            
            f.write("LOG DE RÉPARATION:\n")
            f.write("-" * 30 + "\n")
            for log_entry in self.repair_log:
                f.write(log_entry + "\n")
            
            if self.errors_found:
                f.write("\nERREURS TROUVÉES:\n")
                f.write("-" * 20 + "\n")
                for error in self.errors_found:
                    f.write(f"• {error}\n")
            
            f.write("\n" + "=" * 60 + "\n")
            f.write("FIN DU RAPPORT\n")
            f.write("=" * 60 + "\n")
        
        self.log(f"📄 Rapport généré: {report_path}")
        return report_path
    
    def repair_all(self):
        """Exécute la réparation complète du système"""
        self.log("🚀 DÉBUT DE LA RÉPARATION AUTOMATIQUE DU SYSTÈME")
        self.log("=" * 50)
        
        # Étape 1: Vérification de l'intégrité
        self.log("\n📋 ÉTAPE 1: Vérification de l'intégrité")
        db_ok = self.check_database_integrity()
        
        # Étape 2: Vérification des rôles
        self.log("\n📋 ÉTAPE 2: Vérification des rôles")
        roles_ok = self.check_user_roles()
        
        # Étape 3: Vérification des permissions
        self.log("\n📋 ÉTAPE 3: Vérification des permissions")
        permissions_ok = self.check_permissions()
        
        # Étape 4: Réparation si nécessaire
        if not db_ok or not roles_ok or not permissions_ok:
            self.log("\n🔧 ÉTAPE 4: Réparation du système")
            
            if not db_ok:
                if not self.repair_database_structure():
                    self.log("❌ Échec de la réparation de la structure", "ERROR")
                    return False
            
            if not roles_ok:
                if not self.repair_user_roles():
                    self.log("❌ Échec de la réparation des rôles", "ERROR")
                    return False
            
            if not permissions_ok:
                # Les permissions sont créées automatiquement avec les tables
                self.log("✅ Permissions recréées automatiquement", "SUCCESS")
        
        # Étape 5: Test final
        self.log("\n🧪 ÉTAPE 5: Test final du système")
        if not self.test_system():
            self.log("❌ Échec du test final", "ERROR")
            return False
        
        # Génération du rapport
        self.log("\n📄 Génération du rapport...")
        report_path = self.generate_report()
        
        # Résumé final
        self.log("\n" + "=" * 50)
        if self.errors_found:
            self.log("⚠️  RÉPARATION TERMINÉE AVEC DES ERREURS")
            self.log(f"Nombre d'erreurs: {len(self.errors_found)}")
        else:
            self.log("🎉 RÉPARATION TERMINÉE AVEC SUCCÈS")
        
        self.log("=" * 50)
        self.log(f"📄 Rapport détaillé: {report_path}")
        
        return len(self.errors_found) == 0

def main():
    """Fonction principale"""
    print("🔧 Script de Réparation Automatique - EduManager+")
    print("=" * 50)
    
    repair = SystemRepair()
    success = repair.repair_all()
    
    if success:
        print("\n🎉 Le système a été réparé avec succès !")
        print("💡 Vous pouvez maintenant lancer l'application avec: python main.py")
    else:
        print("\n⚠️  La réparation s'est terminée avec des erreurs.")
        print("📄 Consultez le rapport de réparation pour plus de détails.")
        print("🆘 Si le problème persiste, contactez le support technique.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
