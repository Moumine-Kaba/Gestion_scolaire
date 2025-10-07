from database.connection import get_db_connection

def create_table_paiements():
    """Supprime et recrée la table paiements avec la bonne structure"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Vérifier si la table existe
        cur.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME = 'paiements'
        """)
        
        table_exists = cur.fetchone()[0] > 0
        
        if table_exists:
            # Supprimer la table existante
            cur.execute("DROP TABLE paiements")
            print("Table 'paiements' supprimée")
        
        # Créer la nouvelle table avec la bonne structure
        cur.execute("""
            CREATE TABLE paiements (
                id_paiement INT IDENTITY(1,1) PRIMARY KEY,
                id_eleve INT NOT NULL,
                montant DECIMAL(10,2) NOT NULL,
                date_paiement DATE NOT NULL,
                mode_paiement VARCHAR(50) NOT NULL,
                description TEXT,
                date_creation DATETIME DEFAULT GETDATE(),
                statut VARCHAR(20) DEFAULT 'validé',
                reference VARCHAR(50),
                FOREIGN KEY(id_eleve) REFERENCES eleves(id_eleve)
            )
        """)
        conn.commit()
        print("SUCCES - Table 'paiements' recréée avec succès")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERREUR - Erreur recréation table paiements: {e}")
        return False

def insert_sample_payments():
    """Insère des données de test dans la table paiements"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Récupérer quelques élèves pour créer des paiements de test
        cur.execute("SELECT TOP 5 id_eleve FROM eleves")
        eleves = cur.fetchall()
        
        if not eleves:
            print("⚠️ Aucun élève trouvé pour créer des paiements de test")
            conn.close()
            return
        
        # Données de test
        sample_payments = [
            (eleves[0][0], 500000, '2024-01-15', 'Espèces', 'Frais de scolarité - 1er trimestre', 'validé', 'PAY001'),
            (eleves[1][0] if len(eleves) > 1 else eleves[0][0], 300000, '2024-01-20', 'Mobile Money', 'Frais d\'inscription', 'validé', 'PAY002'),
            (eleves[2][0] if len(eleves) > 2 else eleves[0][0], 750000, '2024-02-10', 'Chèque', 'Frais de scolarité - 2ème trimestre', 'en_attente', 'PAY003'),
            (eleves[3][0] if len(eleves) > 3 else eleves[0][0], 250000, '2024-02-15', 'Carte Bancaire', 'Frais de transport', 'validé', 'PAY004'),
            (eleves[4][0] if len(eleves) > 4 else eleves[0][0], 400000, '2024-03-01', 'Virement', 'Frais de cantine', 'validé', 'PAY005')
        ]
        
        # Insérer les données de test
        for eleve_id, montant, date_paiement, mode_paiement, description, statut, reference in sample_payments:
            cur.execute("""
                INSERT INTO paiements (id_eleve, montant, date_paiement, mode_paiement, description, statut, reference)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (eleve_id, montant, date_paiement, mode_paiement, description, statut, reference))
        
        conn.commit()
        conn.close()
        print(f"✅ {len(sample_payments)} paiements de test insérés")
        
    except Exception as e:
        print(f"❌ Erreur insertion données de test: {e}")

def get_all_paiements(eleve_id=None):
    conn = get_db_connection()
    cur = conn.cursor()
    if eleve_id:
        cur.execute("""
            SELECT id_paiement, montant, date_paiement, mode_paiement, description, statut, reference
            FROM paiements WHERE id_eleve=? ORDER BY date_paiement DESC
        """, (eleve_id,))
    else:
        cur.execute("""
            SELECT id_paiement, id_eleve, montant, date_paiement, mode_paiement, description, statut, reference
            FROM paiements ORDER BY date_paiement DESC
        """)
    rows = cur.fetchall()
    conn.close()
    return rows

def add_paiement(eleve_id, montant, date, mode_paiement, description, statut='validé', reference=None):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Générer une référence automatique si non fournie
    if not reference:
        import random
        reference = f"PAY{random.randint(1000, 9999)}"
    
    cur.execute("""
        INSERT INTO paiements (id_eleve, montant, date_paiement, mode_paiement, description, statut, reference)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (eleve_id, montant, date, mode_paiement, description, statut, reference))
    conn.commit()
    conn.close()

def update_paiement(paiement_id, eleve_id, montant, date, mode_paiement, description):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE paiements SET id_eleve=?, montant=?, date_paiement=?, mode_paiement=?, description=?
        WHERE id_paiement=?
    """, (eleve_id, montant, date, mode_paiement, description, paiement_id))
    conn.commit()
    conn.close()

def delete_paiement(paiement_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM paiements WHERE id_paiement=?", (paiement_id,))
    conn.commit()
    conn.close()
