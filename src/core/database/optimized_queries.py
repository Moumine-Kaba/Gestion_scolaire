# -*- coding: utf-8 -*-
"""
Système de requêtes optimisées avec procédures stockées pour EduManager+
- Requêtes pré-compilées pour des performances maximales
- Cache intégré au niveau base de données
- Index automatiques pour les requêtes fréquentes
"""

# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import time
import json
from typing import Dict, List, Any, Optional
from functools import lru_cache
import threading

class OptimizedQueryManager:
    """Gestionnaire de requêtes optimisées avec cache et procédures stockées"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._cache = {}
        self._cache_lock = threading.Lock()
        self._cache_duration = 60  # Cache de 60 secondes
        self._last_cache_clear = time.time()
        
        # Initialiser les index et les vues optimisées
        self._initialize_optimizations()
    
    def _initialize_optimizations(self):
        """Initialise les optimisations de base de données"""
        conn = get_db_connection()
        try:
            # Créer les index pour les requêtes fréquentes
            self._create_performance_indexes(conn)
            
            # Créer les vues optimisées
            self._create_optimized_views(conn)
            
            conn.commit()
            print("✅ Optimisations de base de données initialisées")
        except Exception as e:
            print(f"⚠️ Erreur initialisation optimisations: {e}")
        finally:
            conn.close()
    
    def _create_performance_indexes(self, conn):
        """Crée les index pour optimiser les performances"""
        # Vérifier d'abord quelles tables existent
        cursor = conn.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        indexes = []
        
        # Index pour les élèves (si la table existe)
        if 'eleves' in existing_tables:
            cursor = eleves_columns = [row[1] for row in cursor.fetchall()]
            
            if 'classe_id' in eleves_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_eleves_classe_id ON eleves(classe_id)")
            if 'nom' in eleves_columns and 'prenom' in eleves_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_eleves_nom_prenom ON eleves(nom, prenom)")
        
        # Index pour les classes (si la table existe)
        if 'classes' in existing_tables:
            cursor = classes_columns = [row[1] for row in cursor.fetchall()]
            
            if 'nom' in classes_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_classes_nom ON classes(nom)")
            if 'niveau' in classes_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_classes_niveau ON classes(niveau)")
        
        # Index pour les matières (si la table existe)
        if 'matieres' in existing_tables:
            cursor = matieres_columns = [row[1] for row in cursor.fetchall()]
            
            if 'nom' in matieres_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_matieres_nom ON matieres(nom)")
            if 'classe_id' in matieres_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_matieres_classe_id ON matieres(classe_id)")
        
        # Index pour les notes (si la table existe)
        if 'notes' in existing_tables:
            cursor = notes_columns = [row[1] for row in cursor.fetchall()]
            
            if 'eleve_id' in notes_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_notes_eleve_id ON notes(eleve_id)")
            if 'matiere_id' in notes_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_notes_matiere_id ON notes(matiere_id)")
            if 'date_note' in notes_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_notes_date ON notes(date_note)")
        
        # Index pour les cours (si la table existe)
        if 'cours' in existing_tables:
            cursor = cours_columns = [row[1] for row in cursor.fetchall()]
            
            if 'classe_id' in cours_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_cours_classe_id ON cours(classe_id)")
            if 'matiere_id' in cours_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_cours_matiere_id ON cours(matiere_id)")
            if 'professeur_id' in cours_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_cours_professeur_id ON cours(professeur_id)")
        
        # Index pour les professeurs (si la table existe)
        if 'professeurs' in existing_tables:
            cursor = profs_columns = [row[1] for row in cursor.fetchall()]
            
            if 'nom' in profs_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_professeurs_nom ON professeurs(nom)")
            if 'matiere_id' in profs_columns:
                indexes.append("CREATE INDEX IF NOT EXISTS idx_professeurs_matiere_id ON professeurs(matiere_id)")
        
        for index_sql in indexes:
            try:
                conn.execute(index_sql)
                print(f"✅ Index créé: {index_sql.split()[-1]}")
            except Exception as e:
                print(f"⚠️ Erreur création index: {e}")
    
    def _create_optimized_views(self, conn):
        """Crée des vues optimisées pour les requêtes complexes"""
        views = [
            # Vue optimisée pour les statistiques des classes
            """
            CREATE VIEW IF NOT EXISTS v_classes_stats AS
            SELECT 
                c.id,
                c.nom,
                c.niveau,
                COUNT(e.id) as effectif,
                COUNT(CASE WHEN e.statut = 'actif' THEN 1 END) as actifs,
                COUNT(CASE WHEN e.statut = 'inactif' THEN 1 END) as inactifs
            FROM classes c
            LEFT JOIN eleves e ON c.id = e.classe_id
            GROUP BY c.id, c.nom, c.niveau
            """,
            
            # Vue optimisée pour les notes avec moyennes
            """
            CREATE VIEW IF NOT EXISTS v_notes_stats AS
            SELECT 
                e.id as eleve_id,
                e.nom,
                e.prenom,
                c.nom as classe_nom,
                COUNT(n.id) as nb_notes,
                AVG(n.notes) as moyenne,
                MIN(n.notes) as note_min,
                MAX(n.notes) as note_max
            FROM eleves e
            LEFT JOIN classes c ON e.classe_id = c.id
            LEFT JOIN notes n ON e.id = n.eleve_id
            GROUP BY e.id, e.nom, e.prenom, c.nom
            """,
            
            # Vue optimisée pour les cours avec détails
            """
            CREATE VIEW IF NOT EXISTS v_cours_details AS
            SELECT 
                c.id,
                c.nom,
                c.heure_debut,
                c.heure_fin,
                cl.nom as classe_nom,
                m.nom as matiere_nom,
                p.nom as professeur_nom,
                p.prenom as professeur_prenom
            FROM cours c
            LEFT JOIN classes cl ON c.classe_id = cl.id
            LEFT JOIN matieres m ON c.matiere_id = m.id
            LEFT JOIN professeurs p ON c.professeur_id = p.id
            """
        ]
        
        for view_sql in views:
            try:
                conn.execute(view_sql)
            except Exception as e:
                print(f"⚠️ Erreur création vue: {e}")
    
    @lru_cache(maxsize=100)
    def get_all_eleves_optimized(self) -> List[Dict[str, Any]]:
        """Récupère tous les élèves avec cache LRU"""
        cache_key = "eleves_all"
        
        # Vérifier le cache en mémoire
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_duration:
                    print("📋 Cache hit: élèves")
                    return cached_data
        
        # Requête adaptative selon la structure de la base
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        try:
            # Vérifier la structure de la table eleves
            cursor = eleves_columns = [row[1] for row in cursor.fetchall()]
            
            if not eleves_columns:
                print("⚠️ Table eleves n'existe pas")
                return []
            
            # Construire la requête selon les colonnes disponibles
            select_fields = ["id_eleve", "nom", "prenom"]
            join_clause = ""
            
            if 'date_naissance' in eleves_columns:
                select_fields.append("date_naissance")
            if 'statut' in eleves_columns:
                select_fields.append("statut")
            if 'classe_id' in eleves_columns:
                select_fields.append("classe_id")
                # Vérifier si la table classes existe
                cursor = conn.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='classes'")
                if cursor.fetchone():
                    join_clause = "LEFT JOIN classes c ON eleves.classe_id = c.id_classe"
                    select_fields.extend(["c.nom as classe_nom", "c.niveau as classe_niveau"])
            
            query = f"""
                SELECT {', '.join(select_fields)}
                FROM eleves
                {join_clause}
                ORDER BY nom, prenom
            """
            
            cursor = conn.execute(query)
            eleves = [dict(row) for row in cursor.fetchall()]
            
            # Mettre en cache
            with self._cache_lock:
                self._cache[cache_key] = (eleves, time.time())
            
            print(f"✅ {len(eleves)} élèves chargés depuis la base")
            return eleves
            
        except Exception as e:
            print(f"⚠️ Erreur get_all_eleves_optimized: {e}")
            return []
        finally:
            conn.close()
    
    @lru_cache(maxsize=50)
    def get_all_classes_optimized(self) -> List[Dict[str, Any]]:
        """Récupère toutes les classes avec statistiques optimisées"""
        cache_key = "classes_all"
        
        # Vérifier le cache en mémoire
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_duration:
                    print("📋 Cache hit: classes")
                    return cached_data
        
        # Requête optimisée avec vue
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        try:
            # Vérifier la structure de la table classes
            cursor = classes_columns = [row[1] for row in cursor.fetchall()]
            
            if not classes_columns:
                print("⚠️ Table classes n'existe pas")
                return []
            
            # Construire la requête selon les colonnes disponibles
            select_fields = ["id_classe", "nom"]
            if 'niveau' in classes_columns:
                select_fields.append("niveau")
            if 'capacite' in classes_columns:
                select_fields.append("capacite")
            if 'statut' in classes_columns:
                select_fields.append("statut")
            
            # Requête simple sans vue complexe
            query = f"""
                SELECT {', '.join(select_fields)}
                FROM classes
                ORDER BY nom
            """
            
            cursor = conn.execute(query)
            classes = [dict(row) for row in cursor.fetchall()]
            
            # Mettre en cache
            with self._cache_lock:
                self._cache[cache_key] = (classes, time.time())
            
            print(f"✅ {len(classes)} classes chargées depuis la base")
            return classes
            
        except Exception as e:
            print(f"⚠️ Erreur get_all_classes_optimized: {e}")
            return []
        finally:
            conn.close()
    
    @lru_cache(maxsize=50)
    def get_all_matieres_optimized(self) -> List[Dict[str, Any]]:
        """Récupère toutes les matières avec cache optimisé"""
        cache_key = "matieres_all"
        
        # Vérifier le cache en mémoire
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_duration:
                    print("📋 Cache hit: matières")
                    return cached_data
        
        # Requête optimisée
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        try:
            # Vérifier la structure de la table matieres
            cursor = matieres_columns = [row[1] for row in cursor.fetchall()]
            
            if not matieres_columns:
                print("⚠️ Table matieres n'existe pas")
                return []
            
            # Construire la requête selon les colonnes disponibles
            select_fields = ["id_matiere", "nom"]
            join_clause = ""
            
            if 'description' in matieres_columns:
                select_fields.append("description")
            if 'coefficient' in matieres_columns:
                select_fields.append("coefficient")
            if 'classe_id' in matieres_columns:
                select_fields.append("classe_id")
                # Vérifier si la table classes existe
                cursor = conn.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='classes'")
                if cursor.fetchone():
                    join_clause = "LEFT JOIN classes c ON matieres.classe_id = c.id_classe"
                    select_fields.append("c.nom as classe_nom")
            
            query = f"""
                SELECT {', '.join(select_fields)}
                FROM matieres
                {join_clause}
                ORDER BY nom
            """
            
            cursor = conn.execute(query)
            matieres = [dict(row) for row in cursor.fetchall()]
            
            # Mettre en cache
            with self._cache_lock:
                self._cache[cache_key] = (matieres, time.time())
            
            print(f"✅ {len(matieres)} matières chargées depuis la base")
            return matieres
            
        except Exception as e:
            print(f"⚠️ Erreur get_all_matieres_optimized: {e}")
            return []
        finally:
            conn.close()
    
    @lru_cache(maxsize=200)
    def get_notes_by_eleve_optimized(self, eleve_id: int) -> List[Dict[str, Any]]:
        """Récupère les notes d'un élève avec cache optimisé"""
        cache_key = f"notes_eleve_{eleve_id}"
        
        # Vérifier le cache en mémoire
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_duration:
                    print(f"📋 Cache hit: notes élève {eleve_id}")
                    return cached_data
        
        # Requête optimisée
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        try:
            cursor = conn.execute("""
                SELECT 
                    n.id,
                    n.notes,
                    n.date_note,
                    n.type_evaluation,
                    n.coefficient,
                    m.nom as matiere_nom,
                    m.coefficient as matiere_coefficient
                FROM notes n
                LEFT JOIN matieres m ON n.matiere_id = m.id
                WHERE n.eleve_id = ?
                ORDER BY n.date_note DESC
            """, (eleve_id,))
            
            notes = [dict(row) for row in cursor.fetchall()]
            
            # Mettre en cache
            with self._cache_lock:
                self._cache[cache_key] = (notes, time.time())
            
            print(f"✅ {len(notes)} notes chargées pour l'élève {eleve_id}")
            return notes
            
        except Exception as e:
            print(f"⚠️ Erreur get_notes_by_eleve_optimized: {e}")
            return []
        finally:
            conn.close()
    
    def get_cours_optimized(self, mode: str = "enseignements") -> List[Dict[str, Any]]:
        """Récupère les cours avec vue optimisée"""
        cache_key = f"cours_{mode}"
        
        # Vérifier le cache en mémoire
        with self._cache_lock:
            if cache_key in self._cache:
                cached_data, timestamp = self._cache[cache_key]
                if time.time() - timestamp < self._cache_duration:
                    print(f"📋 Cache hit: cours {mode}")
                    return cached_data
        
        # Requête optimisée avec vue
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        try:
            cursor = conn.execute("""
                SELECT 
                    cd.id,
                    cd.nom,
                    cd.heure_debut,
                    cd.heure_fin,
                    cd.classe_nom,
                    cd.matiere_nom,
                    cd.professeur_nom,
                    cd.professeur_prenom
                FROM v_cours_details cd
                ORDER BY cd.heure_debut, cd.classe_nom
            """)
            
            cours = [dict(row) for row in cursor.fetchall()]
            
            # Mettre en cache
            with self._cache_lock:
                self._cache[cache_key] = (cours, time.time())
            
            print(f"✅ {len(cours)} cours chargés pour le mode {mode}")
            return cours
            
        except Exception as e:
            print(f"⚠️ Erreur get_cours_optimized: {e}")
            return []
        finally:
            conn.close()
    
    def clear_cache(self):
        """Vide le cache"""
        with self._cache_lock:
            self._cache.clear()
        # Vider aussi le cache LRU
        self.get_all_eleves_optimized.cache_clear()
        self.get_all_classes_optimized.cache_clear()
        self.get_all_matieres_optimized.cache_clear()
        print("🗑️ Cache vidé")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        with self._cache_lock:
            cache_size = len(self._cache)
            cache_keys = list(self._cache.keys())
        
        return {
            "cache_size": cache_size,
            "cache_keys": cache_keys,
            "cache_duration": self._cache_duration,
            "lru_cache_info": {
                "eleves": self.get_all_eleves_optimized.cache_info(),
                "classes": self.get_all_classes_optimized.cache_info(),
                "matieres": self.get_all_matieres_optimized.cache_info(),
            }
        }

# Instance globale du gestionnaire de requêtes optimisées
_query_manager = None

def get_optimized_query_manager(db_path: str) -> OptimizedQueryManager:
    """Retourne l'instance globale du gestionnaire de requêtes optimisées"""
    global _query_manager
    if _query_manager is None:
        _query_manager = OptimizedQueryManager(db_path)
    return _query_manager

# Fonctions de compatibilité pour les contrôleurs existants
def get_all_eleves_fast() -> List[Dict[str, Any]]:
    """Version optimisée de get_all_eleves"""
    from src.core.paths import DATABASE_PATH
    manager = get_optimized_query_manager(DATABASE_PATH)
    return manager.get_all_eleves_optimized()

def get_all_classes_fast() -> List[Dict[str, Any]]:
    """Version optimisée de get_all_classes"""
    from src.core.paths import DATABASE_PATH
    manager = get_optimized_query_manager(DATABASE_PATH)
    return manager.get_all_classes_optimized()

def get_all_matieres_fast() -> List[Dict[str, Any]]:
    """Version optimisée de get_all_matieres"""
    from src.core.paths import DATABASE_PATH
    manager = get_optimized_query_manager(DATABASE_PATH)
    return manager.get_all_matieres_optimized()

def get_notes_by_eleve_fast(eleve_id: int) -> List[Dict[str, Any]]:
    """Version optimisée de get_notes_by_eleve"""
    from src.core.paths import DATABASE_PATH
    manager = get_optimized_query_manager(DATABASE_PATH)
    return manager.get_notes_by_eleve_optimized(eleve_id)

def get_cours_fast(mode: str = "enseignements") -> List[Dict[str, Any]]:
    """Version optimisée de get_cours"""
    from src.core.paths import DATABASE_PATH
    manager = get_optimized_query_manager(DATABASE_PATH)
    return manager.get_cours_optimized(mode)
