# -*- coding: utf-8 -*-
"""
Schéma de Base de Données pour le Module Paiements
EduManager+ - Gestion Complète des Paiements Scolaires

Ce module contient les fonctions de création et gestion des tables
nécessaires pour un système de paiements scolaires complet.
"""

from database.connection import get_db_connection
from datetime import datetime, timedelta

def create_types_frais_table():
    """Crée la table types_frais pour gérer les différents types de frais scolaires"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'types_frais'
        """)
        
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            # Désactiver temporairement les contraintes de clés étrangères
            cur.execute("ALTER TABLE types_frais NOCHECK CONSTRAINT ALL")
            cur.execute("DROP TABLE types_frais")
            print(" Table 'types_frais' supprimée")
        
        # Créer la nouvelle table
        cur.execute("""
            CREATE TABLE types_frais (
                id_type_frais INT IDENTITY(1,1) PRIMARY KEY,
                nom VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                montant_standard DECIMAL(10,2) NOT NULL,
                periodicite VARCHAR(20) NOT NULL CHECK (periodicite IN ('trimestriel', 'annuel', 'ponctuel', 'mensuel')),
                niveau_educatif VARCHAR(20) CHECK (niveau_educatif IN ('primaire', 'college', 'lycee', 'tous')),
                est_obligatoire BIT DEFAULT 1,
                est_actif BIT DEFAULT 1,
                date_creation DATETIME DEFAULT GETDATE(),
                date_modification DATETIME DEFAULT GETDATE()
            )
        """)
        conn.commit()
        print("SUCCES - Table 'types_frais' créée avec succès")
        
        # Insérer des types de frais par défaut
        insert_default_types_frais()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur création table types_frais: {e}")
        return False

def insert_default_types_frais():
    """Insère les types de frais par défaut du système éducatif guinéen"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Types de frais standards
        default_frais = [
            ("Frais de scolarité", "Frais de scolarité annuels", 500000, "annuel", "tous", 1),
            ("Frais d'inscription", "Frais d'inscription pour nouveaux élèves", 100000, "ponctuel", "tous", 1),
            ("Frais de cantine", "Repas et collations", 50000, "mensuel", "tous", 0),
            ("Frais de transport", "Transport scolaire", 75000, "mensuel", "tous", 0),
            ("Frais de matériel", "Fournitures et matériel scolaire", 25000, "trimestriel", "tous", 0),
            ("Frais d'examen", "Frais d'inscription aux examens officiels", 15000, "ponctuel", "college,lycee", 1),
            ("Frais de laboratoire", "Utilisation des laboratoires", 30000, "trimestriel", "college,lycee", 0),
            ("Frais de bibliothèque", "Accès à la bibliothèque", 10000, "trimestriel", "tous", 0),
            ("Frais d'activités", "Sorties et activités extra-scolaires", 20000, "ponctuel", "tous", 0),
            ("Frais de sécurité", "Sécurité et surveillance", 15000, "mensuel", "tous", 0)
        ]
        
        for nom, description, montant, periodicite, niveau, obligatoire in default_frais:
            cur.execute("""
                INSERT INTO types_frais (nom, description, montant_standard, periodicite, niveau_educatif, est_obligatoire)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (nom, description, montant, periodicite, niveau, obligatoire))
        
        conn.commit()
        conn.close()
        print(f"SUCCES - {len(default_frais)} types de frais par défaut insérés")
        
    except Exception as e:
        print(f"ERREUR - Erreur insertion types de frais par défaut: {e}")

def create_echeancier_table():
    """Crée la table echeancier pour gérer les échéances de paiement"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'echeancier'
        """)
        
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            # Désactiver temporairement les contraintes de clés étrangères
            cur.execute("ALTER TABLE echeancier NOCHECK CONSTRAINT ALL")
            cur.execute("DROP TABLE echeancier")
            print(" Table 'echeancier' supprimée")
        
        # Créer la nouvelle table
        cur.execute("""
            CREATE TABLE echeancier (
                id_echeance INT IDENTITY(1,1) PRIMARY KEY,
                id_eleve INT NOT NULL,
                id_type_frais INT NOT NULL,
                annee_scolaire VARCHAR(9) NOT NULL,
                trimestre INT CHECK (trimestre IN (1, 2, 3)),
                montant DECIMAL(10,2) NOT NULL,
                montant_remise DECIMAL(10,2) DEFAULT 0,
                montant_final DECIMAL(10,2) NOT NULL,
                date_echeance DATE NOT NULL,
                date_paiement DATE NULL,
                statut VARCHAR(20) DEFAULT 'en_attente' CHECK (statut IN ('en_attente', 'paye', 'en_retard', 'annule')),
                mode_paiement VARCHAR(50),
                reference_paiement VARCHAR(50),
                penalites DECIMAL(10,2) DEFAULT 0,
                nb_relances INT DEFAULT 0,
                derniere_relance DATE NULL,
                commentaires TEXT,
                date_creation DATETIME DEFAULT GETDATE(),
                date_modification DATETIME DEFAULT GETDATE(),
                FOREIGN KEY(id_eleve) REFERENCES eleves(id_eleve),
                FOREIGN KEY(id_type_frais) REFERENCES types_frais(id_type_frais)
            )
        """)
        conn.commit()
        print("SUCCES - Table 'echeancier' créée avec succès")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur création table echeancier: {e}")
        return False

def create_remises_table():
    """Crée la table remises pour gérer les bourses et réductions"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'remises'
        """)
        
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            cur.execute("DROP TABLE remises")
            print(" Table 'remises' supprimée")
        
        # Créer la nouvelle table
        cur.execute("""
            CREATE TABLE remises (
                id_remise INT IDENTITY(1,1) PRIMARY KEY,
                id_eleve INT NOT NULL,
                id_type_frais INT NULL, -- NULL pour remise globale
                type_remise VARCHAR(50) NOT NULL CHECK (type_remise IN ('bourse', 'reduction', 'exoneration', 'aide_familiale')),
                pourcentage DECIMAL(5,2) NULL, -- Pourcentage de réduction
                montant_fixe DECIMAL(10,2) NULL, -- Montant fixe de réduction
                montant_maximum DECIMAL(10,2) NULL, -- Montant maximum de réduction
                date_debut DATE NOT NULL,
                date_fin DATE NULL,
                statut VARCHAR(20) DEFAULT 'actif' CHECK (statut IN ('actif', 'inactif', 'expire')),
                motif TEXT NOT NULL,
                justificatifs TEXT,
                approbateur VARCHAR(100),
                date_approbation DATE,
                commentaires TEXT,
                date_creation DATETIME DEFAULT GETDATE(),
                date_modification DATETIME DEFAULT GETDATE(),
                FOREIGN KEY(id_eleve) REFERENCES eleves(id_eleve),
                FOREIGN KEY(id_type_frais) REFERENCES types_frais(id_type_frais)
            )
        """)
        conn.commit()
        print("SUCCES - Table 'remises' créée avec succès")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur création table remises: {e}")
        return False

def create_relances_table():
    """Crée la table relances pour gérer les relances de paiement"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'relances'
        """)
        
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            cur.execute("DROP TABLE relances")
            print(" Table 'relances' supprimée")
        
        # Créer la nouvelle table
        cur.execute("""
            CREATE TABLE relances (
                id_relance INT IDENTITY(1,1) PRIMARY KEY,
                id_echeance INT NOT NULL,
                id_eleve INT NOT NULL,
                type_relance VARCHAR(30) NOT NULL CHECK (type_relance IN ('email', 'sms', 'courrier', 'appel', 'visite')),
                date_relance DATE NOT NULL,
                statut VARCHAR(20) DEFAULT 'envoyee' CHECK (statut IN ('envoyee', 'lue', 'ignoree', 'erreur')),
                contenu_message TEXT,
                destinataire VARCHAR(200),
                reponse_eleve TEXT,
                date_reponse DATE,
                frais_relance DECIMAL(10,2) DEFAULT 0,
                commentaires TEXT,
                date_creation DATETIME DEFAULT GETDATE(),
                FOREIGN KEY(id_echeance) REFERENCES echeancier(id_echeance),
                FOREIGN KEY(id_eleve) REFERENCES eleves(id_eleve)
            )
        """)
        conn.commit()
        print("SUCCES - Table 'relances' créée avec succès")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur création table relances: {e}")
        return False

def create_all_payment_tables():
    """Crée toutes les tables du système de paiements"""
    print("Creation des tables du systeme de paiements...")
    
    tables_created = []
    
    # Créer les tables dans l'ordre des dépendances
    if create_types_frais_table():
        tables_created.append("types_frais")
    
    if create_echeancier_table():
        tables_created.append("echeancier")
    
    if create_remises_table():
        tables_created.append("remises")
    
    if create_relances_table():
        tables_created.append("relances")
    
    print(f"SUCCES - Tables créées: {', '.join(tables_created)}")
    return len(tables_created) == 4

def get_current_academic_year():
    """Retourne l'année scolaire actuelle"""
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    # En Guinée, l'année scolaire commence en octobre
    if current_month >= 10:
        return f"{current_year}-{current_year + 1}"
    else:
        return f"{current_year - 1}-{current_year}"

def generate_echeancier_for_student(student_id, academic_year=None):
    """Génère automatiquement l'échéancier pour un élève"""
    if not academic_year:
        academic_year = get_current_academic_year()
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Récupérer les types de frais actifs
        cur.execute("""
            SELECT id_type_frais, nom, montant_standard, periodicite, niveau_educatif
            FROM types_frais 
            WHERE est_actif = 1
        """)
        types_frais = cur.fetchall()
        
        # Récupérer les informations de l'élève
        cur.execute("""
            SELECT id_eleve, nom, prenom, id_classe
            FROM eleves 
            WHERE id_eleve = ?
        """, (student_id,))
        eleve = cur.fetchone()
        
        if not eleve:
            print(f"ERREUR - Élève {student_id} non trouvé")
            return False
        
        # Récupérer le niveau de la classe de l'élève
        cur.execute("""
            SELECT niveau FROM classes WHERE id = ?
        """, (eleve[3],))
        classe_info = cur.fetchone()
        niveau_eleve = classe_info[0] if classe_info else "tous"
        
        echeances_created = 0
        
        for type_frais in types_frais:
            tf_id, nom, montant, periodicite, niveau = type_frais
            
            # Vérifier si le type de frais s'applique à cet élève
            if niveau != "tous" and niveau_eleve not in niveau:
                continue
            
            # Calculer les dates d'échéance selon la périodicité
            if periodicite == "annuel":
                # Échéance unique en début d'année scolaire
                date_echeance = f"{academic_year.split('-')[0]}-10-01"
                cur.execute("""
                    INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, montant, montant_final, date_echeance)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (student_id, tf_id, academic_year, montant, montant, date_echeance))
                echeances_created += 1
                
            elif periodicite == "trimestriel":
                # Trois échéances par année scolaire
                for trimestre in [1, 2, 3]:
                    if trimestre == 1:
                        date_echeance = f"{academic_year.split('-')[0]}-10-01"
                    elif trimestre == 2:
                        date_echeance = f"{academic_year.split('-')[0]}-12-15"
                    else:  # trimestre 3
                        date_echeance = f"{academic_year.split('-')[1]}-03-01"
                    
                    cur.execute("""
                        INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, trimestre, montant, montant_final, date_echeance)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (student_id, tf_id, academic_year, trimestre, montant, montant, date_echeance))
                    echeances_created += 1
                    
            elif periodicite == "mensuel":
                # Échéances mensuelles pendant l'année scolaire
                for mois in range(10, 13):  # Octobre à Décembre
                    date_echeance = f"{academic_year.split('-')[0]}-{mois:02d}-01"
                    cur.execute("""
                        INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, montant, montant_final, date_echeance)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (student_id, tf_id, academic_year, montant, montant, date_echeance))
                    echeances_created += 1
                
                for mois in range(1, 7):  # Janvier à Juin
                    date_echeance = f"{academic_year.split('-')[1]}-{mois:02d}-01"
                    cur.execute("""
                        INSERT INTO echeancier (id_eleve, id_type_frais, annee_scolaire, montant, montant_final, date_echeance)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (student_id, tf_id, academic_year, montant, montant, date_echeance))
                    echeances_created += 1
        
        conn.commit()
        conn.close()
        print(f"SUCCES - {echeances_created} échéances générées pour l'élève {student_id}")
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur génération échéancier: {e}")
        return False

if __name__ == "__main__":
    # Test de création des tables
    create_all_payment_tables()

