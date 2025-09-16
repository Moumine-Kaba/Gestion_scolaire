import sqlite3
import hashlib

def init_admin():
    db_path = "database/edumanager.db"  # Chemin vers ta base (modifie si besoin)
    username = 'admin'
    password = hashlib.sha256("root".encode()).hexdigest()
    email = 'admin@email.com'
    prenom = 'Admin'
    nom = 'User'
    telephone = '0000000000'
    role = 'admin'
    niveau = None

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Vérifie si déjà existant, supprime si besoin
    cursor.execute("DELETE FROM utilisateurs WHERE nom_utilisateur = ?", (username,))

    cursor.execute("""
        INSERT INTO utilisateurs (nom_utilisateur, prenom, nom, email, telephone, mot_de_passe, role, niveau)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (username, prenom, nom, email, telephone, password, role, niveau))

    conn.commit()
    conn.close()
    print(f"✅ Utilisateur admin créé : username = '{username}' / password = 'root'")

if __name__ == "__main__":
    init_admin()
