import sqlite3
import os
from datetime import datetime

# Chemin de base de données centralisé
DB_PATH = "database/edumanager.db"

# =================== CACHE MÉMOIRE SIMPLE ===================
# Objectif: éviter des lectures répétées coûteuses en DB.
_CACHE = {
    "cours_all": None,
    "enseignements_all": None,
    "emplois_all": None,
    "stats": None,
}

def _invalidate_cache(*keys):
    if not keys:
        for k in list(_CACHE.keys()):
            _CACHE[k] = None
        return
    for k in keys:
        if k in _CACHE:
            _CACHE[k] = None

def preload_academic_cache():
    """Précharge les principales données académiques en cache.
    À appeler au démarrage de l'application (splash/login)."""
    try:
        # Cours unifiés
        _CACHE["cours_all"] = get_all_cours()
        # Enseignements
        _CACHE["enseignements_all"] = get_all_enseignements()
        # Emplois du temps
        _CACHE["emplois_all"] = get_all_emplois()
        # Statistiques
        _CACHE["stats"] = get_cours_stats()
        # Note: listes auxiliaires (profs/classes/matières/salles) sont rapides et appelées à la demande
        print("⚡ Préchargement académique terminé")
    except Exception as e:
        print(f"⚠️ Erreur lors du préchargement du cache académique: {e}")

def _connect():
    """Connexion à la base de données avec gestion d'erreur"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
        # PRAGMA de performance
        try:
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.execute("PRAGMA synchronous=NORMAL;")
            conn.execute("PRAGMA temp_store=MEMORY;")
            conn.execute("PRAGMA mmap_size=134217728;")  # 128MB
            conn.execute("PRAGMA cache_size=-20000;")     # ~20MB cache
        except Exception:
            pass
        return conn
    except Exception as e:
        print(f"❌ Erreur connexion DB: {e}")
        return None

def _ensure_tables():
    """Crée la table unifiée si elle n'existe pas"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            
            # Table unifiée des cours
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cours (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT NOT NULL DEFAULT 'enseignement',
                    professeur_id INTEGER NOT NULL,
                    classe_id INTEGER NOT NULL,
                    matiere_id INTEGER NOT NULL,
                    salle_id INTEGER,
                    jour TEXT DEFAULT 'Lundi',
                    heure TEXT DEFAULT '08:00',
                    duree INTEGER DEFAULT 60,
                    statut TEXT DEFAULT 'Actif',
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            print("✅ Table unifiée cours créée/vérifiée avec succès")
            # Index pour accélérer les jointures et filtres
            try:
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_prof ON cours(professeur_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_classe ON cours(classe_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_matiere ON cours(matiere_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_salle ON cours(salle_id);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_type ON cours(type);")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_cours_jour_heure ON cours(jour, heure);")
                conn.commit()
            except Exception as ie:
                print(f"⚠️ Erreur création index cours: {ie}")
            
    except Exception as e:
        print(f"❌ Erreur création table: {e}")

# Initialiser les tables au chargement du module
_ensure_tables()

# =================== FONCTIONS UNIFIÉES COURS ===================

def get_all_cours():
    """Récupère tous les cours avec les noms associés (sans distinction de type)"""
    try:
        # Cache
        if _CACHE.get("cours_all") is not None:
            return _CACHE["cours_all"]
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id_cours, c.professeur_id, c.classe_id, c.matiere_id, c.salle_id,
                    c.date, c.heure_debut, c.heure_fin, c.statut, c.nom as description,
                    p.nom as professeur_nom,
                    p.prenom as professeur_prenom,
                    cl.nom as classe_nom,
                    cl.niveau as classe_niveau,
                    m.nom as matiere_nom,
                    s.nom as salle_nom
                FROM cours c
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN classes cl ON c.classe_id = cl.id_classe
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                ORDER BY c.date DESC, c.heure_debut DESC
            """)
            data = [dict(row) for row in cursor.fetchall()]
            _CACHE["cours_all"] = data
            return data
    except Exception as e:
        print(f"❌ Erreur get_all_cours: {e}")
        return []

def get_all_enseignements():
    """Récupère tous les enseignements avec les noms associés"""
    try:
        if _CACHE.get("enseignements_all") is not None:
            return _CACHE["enseignements_all"]
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id_cours, c.professeur_id, c.classe_id, c.matiere_id, c.salle_id,
                    c.date, c.heure_debut, c.heure_fin, c.statut, c.nom as description,
                    p.nom as professeur_nom,
                    p.prenom as professeur_prenom,
                    cl.nom as classe_nom,
                    cl.niveau as classe_niveau,
                    m.nom as matiere_nom,
                    s.nom as salle_nom
                FROM cours c
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN classes cl ON c.classe_id = cl.id_classe
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                ORDER BY c.date DESC, c.heure_debut DESC
            """)
            data = [dict(row) for row in cursor.fetchall()]
            _CACHE["enseignements_all"] = data
            return data
    except Exception as e:
        print(f"❌ Erreur get_all_enseignements: {e}")
        return []

def add_cours(professeur_id, classe_id, matiere_id, salle_id=None, jour='Lundi', heure='08:00', duree=60, statut='Actif', description=''):
    """Ajoute un nouveau cours (unifié)"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cours (professeur_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (professeur_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description))
            conn.commit()
            print(f"✅ Cours ajouté: Prof {professeur_id}, Classe {classe_id}, Matière {matiere_id}")
            _invalidate_cache("cours_all", "enseignements_all", "emplois_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur add_cours: {e}")
        return False

def update_cours(id, professeur_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description=''):
    """Met à jour un cours existant"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cours 
                SET professeur_id=?, classe_id=?, matiere_id=?, salle_id=?, jour=?, heure=?, duree=?, statut=?, description=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (professeur_id, classe_id, matiere_id, salle_id, jour, heure, duree, statut, description, id))
            conn.commit()
            print(f"✅ Cours {id} mis à jour")
            _invalidate_cache("cours_all", "enseignements_all", "emplois_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur update_cours: {e}")
        return False

def delete_cours(id):
    """Supprime un cours"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cours WHERE id=?", (id,))
            conn.commit()
            print(f"✅ Cours {id} supprimé")
            _invalidate_cache("cours_all", "enseignements_all", "emplois_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur delete_cours: {e}")
        return False

def get_cours_by_id(id):
    """Récupère un cours par son ID"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id, c.professeur_id, c.classe_id, c.matiere_id, c.salle_id,
                    c.jour, c.heure, c.duree, c.statut, c.description,
                    p.nom || ' ' || p.prenom as professeur_nom,
                    cl.nom_classe as classe_nom,
                    m.nom_matiere as matiere_nom,
                    s.nom_salle as salle_nom
                FROM cours c
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN classes cl ON c.classe_id = cl.id_classe
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                WHERE c.id = ?
            """, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"❌ Erreur get_cours_by_id: {e}")
        return None

def add_enseignement(professeur_id, classe_id, matiere_id, salle_id=None, jours_cours=None, duree_cours=60, statut='Actif'):
    """Ajoute un nouvel enseignement"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cours (type, professeur_id, classe_id, matiere_id, salle_id, jour, duree, statut)
                VALUES ('enseignement', ?, ?, ?, ?, ?, ?, ?)
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut))
            conn.commit()
            print(f"✅ Enseignement ajouté: Prof {professeur_id}, Classe {classe_id}, Matière {matiere_id}")
            return True
    except Exception as e:
        print(f"❌ Erreur add_enseignement: {e}")
        return False

def update_enseignement(id, professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut):
    """Met à jour un enseignement existant"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE enseignement
                SET professeur_id=?, classe_id=?, matiere_id=?, salle_id=?, 
                    jours_cours=?, duree_cours=?, statut=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (professeur_id, classe_id, matiere_id, salle_id, jours_cours, duree_cours, statut, id))
            conn.commit()
            print(f"✅ Enseignement {id} mis à jour")
            return True
    except Exception as e:
        print(f"❌ Erreur update_enseignement: {e}")
        return False

def delete_enseignement(id):
    """Supprime un enseignement"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cours WHERE id=? AND type='enseignement'", (id,))
            conn.commit()
            print(f"✅ Enseignement {id} supprimé")
            return True
    except Exception as e:
        print(f"❌ Erreur delete_enseignement: {e}")
        return False

def get_enseignement_by_id(id):
    """Récupère un enseignement par son ID"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    e.id, e.professeur_id, e.classe_id, e.matiere_id, e.salle_id,
                    e.jours_cours, e.duree_cours, e.statut,
                    p.nom || ' ' || p.prenom as professeur_nom,
                    c.nom as classe_nom,
                    m.nom as matiere_nom,
                    s.nom as salle_nom
                FROM enseignement e
                LEFT JOIN professeurs p ON e.professeur_id = p.id
                LEFT JOIN classes c ON e.classe_id = c.id
                LEFT JOIN matieres m ON e.matiere_id = m.id
                LEFT JOIN salles s ON e.salle_id = s.id
                WHERE e.id = ?
            """, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"❌ Erreur get_enseignement_by_id: {e}")
        return None

# =================== FONCTIONS EMPLOIS DU TEMPS ===================

def get_all_emplois():
    """Récupère tous les emplois du temps avec les noms associés"""
    try:
        if _CACHE.get("emplois_all") is not None:
            return _CACHE["emplois_all"]
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    c.id, c.professeur_id, c.classe_id, c.matiere_id, c.salle_id,
                    c.jour, c.heure, c.duree, c.statut, c.description,
                    p.nom || ' ' || p.prenom as professeur_nom,
                    cl.nom_classe as classe_nom,
                    m.nom_matiere as matiere_nom,
                    s.nom_salle as salle_nom
                FROM cours c
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN classes cl ON c.classe_id = cl.id_classe
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                WHERE c.type = 'emploi'
                ORDER BY 
                    CASE c.jour 
                        WHEN 'Lundi' THEN 1
                        WHEN 'Mardi' THEN 2
                        WHEN 'Mercredi' THEN 3
                        WHEN 'Jeudi' THEN 4
                        WHEN 'Vendredi' THEN 5
                        WHEN 'Samedi' THEN 6
                        WHEN 'Dimanche' THEN 7
                        ELSE 8
                    END,
                    c.heure
            """)
            data = [dict(row) for row in cursor.fetchall()]
            _CACHE["emplois_all"] = data
            return data
    except Exception as e:
        print(f"❌ Erreur get_all_emplois: {e}")
        return []

def add_emploi(jour, heure, matiere_id, professeur_id, classe_id=None, salle_id=None):
    """Ajoute un nouvel emploi du temps"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cours (type, jour, heure, matiere_id, professeur_id, classe_id, salle_id, duree, statut)
                VALUES ('emploi', ?, ?, ?, ?, ?, ?, 60, 'Actif')
            """, (jour, heure, matiere_id, professeur_id, classe_id, salle_id))
            conn.commit()
            print(f"✅ Emploi ajouté: {jour} {heure} - Matière {matiere_id}")
            _invalidate_cache("emplois_all", "cours_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur add_emploi: {e}")
        return False

def update_emploi(id, jour, heure, matiere_id, professeur_id, classe_id=None, salle_id=None):
    """Met à jour un emploi du temps existant"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE emplois_du_temps
                SET jour=?, heure=?, matiere_id=?, professeur_id=?, classe_id=?, salle_id=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (jour, heure, matiere_id, professeur_id, classe_id, salle_id, id))
            conn.commit()
            print(f"✅ Emploi {id} mis à jour")
            _invalidate_cache("emplois_all", "cours_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur update_emploi: {e}")
        return False

def delete_emploi(id):
    """Supprime un emploi du temps"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM cours WHERE id=? AND type='emploi'", (id,))
            conn.commit()
            print(f"✅ Emploi {id} supprimé")
            _invalidate_cache("emplois_all", "cours_all", "stats")
            return True
    except Exception as e:
        print(f"❌ Erreur delete_emploi: {e}")
        return False

def get_emploi_by_id(id):
    """Récupère un emploi du temps par son ID"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    e.id, e.jour, e.heure, e.matiere_id, e.professeur_id, e.classe_id, e.salle_id,
                    m.nom as matiere_nom,
                    p.nom || ' ' || p.prenom as professeur_nom,
                    c.nom as classe_nom,
                    s.nom as salle_nom
                FROM emplois_du_temps e
                LEFT JOIN matieres m ON e.matiere_id = m.id
                LEFT JOIN professeurs p ON e.professeur_id = p.id
                LEFT JOIN classes c ON e.classe_id = c.id
                LEFT JOIN salles s ON e.salle_id = s.id
                WHERE e.id = ?
            """, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    except Exception as e:
        print(f"❌ Erreur get_emploi_by_id: {e}")
        return None

# =================== FONCTIONS UTILITAIRES ===================

def get_emplois_by_classe(classe_id):
    """Récupère les emplois du temps pour une classe spécifique"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    e.id, e.jour, e.heure, e.matiere_id, e.professeur_id, e.salle_id,
                    m.nom as matiere_nom,
                    p.nom || ' ' || p.prenom as professeur_nom,
                    s.nom as salle_nom
                FROM emplois_du_temps e
                LEFT JOIN matieres m ON e.matiere_id = m.id
                LEFT JOIN professeurs p ON e.professeur_id = p.id
                LEFT JOIN salles s ON e.salle_id = s.id
                WHERE e.classe_id = ?
                ORDER BY 
                    CASE e.jour 
                        WHEN 'Lundi' THEN 1
                        WHEN 'Mardi' THEN 2
                        WHEN 'Mercredi' THEN 3
                        WHEN 'Jeudi' THEN 4
                        WHEN 'Vendredi' THEN 5
                        WHEN 'Samedi' THEN 6
                        WHEN 'Dimanche' THEN 7
                        ELSE 8
                    END,
                    e.heure
            """, (classe_id,))
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_emplois_by_classe: {e}")
        return []

def get_enseignements_by_professeur(professeur_id):
    """Récupère les enseignements pour un professeur spécifique"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    e.id, e.classe_id, e.matiere_id, e.salle_id,
                    e.jours_cours, e.duree_cours, e.statut,
                    c.nom as classe_nom,
                    m.nom as matiere_nom,
                    s.nom as salle_nom
                FROM enseignement e
                LEFT JOIN classes c ON e.classe_id = c.id
                LEFT JOIN matieres m ON e.matiere_id = m.id
                LEFT JOIN salles s ON e.salle_id = s.id
                WHERE e.professeur_id = ?
                ORDER BY e.id DESC
            """, (professeur_id,))
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_enseignements_by_professeur: {e}")
        return []

def get_cours_stats():
    """Récupère les statistiques des cours"""
    try:
        if _CACHE.get("stats") is not None:
            return _CACHE["stats"]
        with _connect() as conn:
            cursor = conn.cursor()
            
            # Statistiques cours (utiliser la vraie table cours)
            cursor.execute("SELECT COUNT(*) as total_cours FROM cours")
            cours_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as cours_termines FROM cours WHERE statut = 'termine'")
            cours_termines = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as cours_en_cours FROM cours WHERE statut = 'en_cours'")
            cours_en_cours = cursor.fetchone()[0]
            
            # Statistiques emplois du temps
            try:
                cursor.execute("SELECT COUNT(*) as total_emplois FROM emplois_du_temps")
                emplois_count = cursor.fetchone()[0]
            except:
                emplois_count = 0
            
            data = {
                'total_cours': cours_count,
                'cours_termines': cours_termines,
                'cours_en_cours': cours_en_cours,
                'total_emplois': emplois_count
            }
            _CACHE["stats"] = data
            return data
    except Exception as e:
        print(f"❌ Erreur get_cours_stats: {e}")
        return {
            'total_cours': 0,
            'cours_termines': 0,
            'cours_en_cours': 0,
            'total_emplois': 0
        }

# =================== FONCTIONS POUR CHARGER LES DONNÉES ===================

def get_all_professeurs():
    """Récupère tous les professeurs"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_professeur, nom, prenom FROM professeurs ORDER BY nom, prenom")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_all_professeurs: {e}")
        return []

def get_all_classes():
    """Récupère toutes les classes"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_classe, nom_classe FROM classes ORDER BY nom_classe")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_all_classes: {e}")
        return []

def get_all_matieres():
    """Récupère toutes les matières"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_matiere, nom_matiere FROM matieres ORDER BY nom_matiere")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_all_matieres: {e}")
        return []

def get_all_salles():
    """Récupère toutes les salles"""
    try:
        with _connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_salle, nom_salle FROM salles ORDER BY nom_salle")
            return [dict(row) for row in cursor.fetchall()]
    except Exception as e:
        print(f"❌ Erreur get_all_salles: {e}")
        return []

# =================== FONCTIONS DE COMPATIBILITÉ ===================

# Alias pour compatibilité avec l'ancien système
def get_all_enseignements_old():
    """Version compatible avec l'ancien système"""
    return get_all_enseignements()

def get_all_emplois_old():
    """Version compatible avec l'ancien système"""
    emplois = get_all_emplois()
    # Convertir en format tuple pour compatibilité
    return [(e['id'], e['jour'], e['heure'], e['matiere_nom'], e['professeur_nom'], e['salle_nom']) for e in emplois]

# Fonctions d'ajout compatibles
def add_emploi_old(jour, heure, matiere, prof, salle):
    """Version compatible avec l'ancien système"""
    # Cette fonction nécessite de trouver les IDs par nom
    # Pour l'instant, on retourne False
    print("⚠️ add_emploi_old: Fonction de compatibilité non implémentée")
    return False

def update_emploi_old(id, jour, heure, matiere, prof, salle):
    """Version compatible avec l'ancien système"""
    print("⚠️ update_emploi_old: Fonction de compatibilité non implémentée")
    return False

def delete_emploi_old(id):
    """Version compatible avec l'ancien système"""
    return delete_emploi(id)
