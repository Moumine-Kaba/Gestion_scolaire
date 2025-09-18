#!/usr/bin/env python3
"""
SYSTÈME DE PROCÉDURES STOCKÉES OPTIMISÉES
==========================================

Ce module implémente des procédures stockées simulées en Python pour optimiser
les performances de l'application EduManager+.

Basé sur l'analyse de votre architecture :
- 43 tables dans la base de données
- Structure modulaire (academic, administrative, auth, communication)
- Contrôleurs avec cache mémoire existant
- Problème : 10 secondes de chargement quand il y a des données

SOLUTION : Procédures stockées avec cache intelligent et préchargement
"""

# Remplacé par SQL Server  # Remplacé par SQL Server
from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import threading
import time
from typing import Dict, List, Any, Optional, Tuple
from functools import lru_cache
import json
import os
from datetime import datetime, timedelta

class StoredProcedureManager:
    """
    Gestionnaire de procédures stockées optimisées
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, db_path: str):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, db_path: str):
        if self._initialized:
            return
            
        self.db_path = db_path
        self.cache = {}
        self.cache_timestamps = {}
        self.cache_duration = 300  # 5 minutes par défaut
        self.procedures = {}
        self.stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'db_queries': 0,
            'total_time_saved': 0
        }
        
        self._initialize_procedures()
        self._initialized = True
        print("✅ StoredProcedureManager initialisé")
    
    def _connect(self):
        """Connexion optimisée à la base de données"""
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        # Optimisations SQLite
        # 50MB cache
        # 256MB mmap
        
        return conn
    
    def _initialize_procedures(self):
        """Initialise toutes les procédures stockées"""
        
        # === PROCÉDURES ÉLÈVES ===
        self.procedures['sp_get_all_eleves'] = self._sp_get_all_eleves
        self.procedures['sp_get_eleves_by_classe'] = self._sp_get_eleves_by_classe
        self.procedures['sp_get_eleve_stats'] = self._sp_get_eleve_stats
        self.procedures['sp_search_eleves'] = self._sp_search_eleves
        
        # === PROCÉDURES CLASSES ===
        self.procedures['sp_get_all_classes'] = self._sp_get_all_classes
        self.procedures['sp_get_classe_stats'] = self._sp_get_classe_stats
        self.procedures['sp_get_classes_by_niveau'] = self._sp_get_classes_by_niveau
        
        # === PROCÉDURES MATIÈRES ===
        self.procedures['sp_get_all_matieres'] = self._sp_get_all_matieres
        self.procedures['sp_get_matieres_by_classe'] = self._sp_get_matieres_by_classe
        
        # === PROCÉDURES NOTES ===
        self.procedures['sp_get_notes_by_eleve'] = self._sp_get_notes_by_eleve
        self.procedures['sp_get_notes_stats'] = self._sp_get_notes_stats
        self.procedures['sp_get_moyennes_by_classe'] = self._sp_get_moyennes_by_classe
        
        # === PROCÉDURES COURS ===
        self.procedures['sp_get_all_cours'] = self._sp_get_all_cours
        self.procedures['sp_get_cours_by_classe'] = self._sp_get_cours_by_classe
        self.procedures['sp_get_cours_stats'] = self._sp_get_cours_stats
        
        # === PROCÉDURES PROFESSEURS ===
        self.procedures['sp_get_all_professeurs'] = self._sp_get_all_professeurs
        self.procedures['sp_get_professeur_stats'] = self._sp_get_professeur_stats
        
        # === PROCÉDURES DASHBOARD ===
        self.procedures['sp_get_dashboard_stats'] = self._sp_get_dashboard_stats
        self.procedures['sp_get_global_stats'] = self._sp_get_global_stats
        
        print(f"✅ {len(self.procedures)} procédures stockées initialisées")
    
    def execute(self, procedure_name: str, *args, **kwargs) -> Any:
        """
        Exécute une procédure stockée avec cache intelligent
        """
        start_time = time.time()
        
        # Vérifier le cache
        cache_key = f"{procedure_name}:{hash(str(args) + str(kwargs))}"
        
        if self._is_cache_valid(cache_key):
            self.stats['cache_hits'] += 1
            self.stats['total_time_saved'] += time.time() - start_time
            print(f"📋 Cache hit: {procedure_name}")
            return self.cache[cache_key]
        
        # Exécuter la procédure
        if procedure_name not in self.procedures:
            raise ValueError(f"Procédure '{procedure_name}' non trouvée")
        
        self.stats['cache_misses'] += 1
        self.stats['db_queries'] += 1
        
        result = self.procedures[procedure_name](*args, **kwargs)
        
        # Mettre en cache
        self.cache[cache_key] = result
        self.cache_timestamps[cache_key] = time.time()
        
        execution_time = time.time() - start_time
        print(f"⚡ {procedure_name} exécutée en {execution_time:.3f}s")
        
        return result
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Vérifie si le cache est valide"""
        if cache_key not in self.cache:
            return False
        
        cache_age = time.time() - self.cache_timestamps[cache_key]
        return cache_age < self.cache_duration
    
    def invalidate_cache(self, pattern: str = None):
        """Invalide le cache (tout ou par pattern)"""
        if pattern is None:
            self.cache.clear()
            self.cache_timestamps.clear()
            print("🗑️ Cache complètement vidé")
        else:
            keys_to_remove = [k for k in self.cache.keys() if pattern in k]
            for key in keys_to_remove:
                del self.cache[key]
                del self.cache_timestamps[key]
            print(f"🗑️ Cache vidé pour pattern: {pattern}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques de performance"""
        total_requests = self.stats['cache_hits'] + self.stats['cache_misses']
        hit_rate = (self.stats['cache_hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'db_queries': self.stats['db_queries'],
            'time_saved': f"{self.stats['total_time_saved']:.2f}s",
            'cache_size': len(self.cache)
        }
    
    # ===== PROCÉDURES STOCKÉES =====
    
    def _sp_get_all_eleves(self) -> List[Dict[str, Any]]:
        """Récupère tous les élèves avec informations complètes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    e.id_eleve,
                    e.nom,
                    e.prenom,
                    e.genre,
                    e.date_naissance,
                    e.adresse,
                    e.telephone,
                    e.email,
                    e.statut,
                    e.date_inscription,
                    e.id_classe,
                    c.nom_classe as classe_nom,
                    c.niveau as classe_niveau,
                    COUNT(n.id_note) as nb_notes,
                    COALESCE(AVG(n.notes), 0) as moyenne_generale
                FROM eleves e
                LEFT JOIN classes c ON e.id_classe = c.id_classe
                LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                GROUP BY e.id_eleve, e.nom, e.prenom, e.genre, e.date_naissance, 
                         e.adresse, e.telephone, e.email, 
                         e.statut, e.date_inscription, e.id_classe, c.nom_classe, c.niveau
                ORDER BY e.nom, e.prenom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_eleves_by_classe(self, classe_id: int) -> List[Dict[str, Any]]:
        """Récupère les élèves d'une classes spécifique"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    e.id_eleve,
                    e.nom,
                    e.prenom,
                    e.genre,
                    e.date_naissance,
                    e.statut,
                    COUNT(n.id_note) as nb_notes,
                    COALESCE(AVG(n.notes), 0) as moyenne_generale
                FROM eleves e
                LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                WHERE e.id_classe = ?
                GROUP BY e.id_eleve, e.nom, e.prenom, e.genre, e.date_naissance, e.statut
                ORDER BY e.nom, e.prenom
            """, (classe_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_eleve_stats(self) -> Dict[str, Any]:
        """Statistiques globales des élèves"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_eleves,
                    COUNT(CASE WHEN statut = 'actif' THEN 1 END) as eleves_actifs,
                    COUNT(CASE WHEN statut = 'inactif' THEN 1 END) as eleves_inactifs,
                    COUNT(CASE WHEN genre = 'M' THEN 1 END) as garcons,
                    COUNT(CASE WHEN genre = 'F' THEN 1 END) as filles,
                    AVG(CASE WHEN statut = 'actif' THEN 1 ELSE 0 END) * 100 as taux_activite
                FROM eleves
            """)
            return dict(cursor.fetchone())
    
    def _sp_search_eleves(self, search_term: str) -> List[Dict[str, Any]]:
        """Recherche d'élèves par nom/prénom"""
        search_pattern = f"%{search_term}%"
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    e.id_eleve,
                    e.nom,
                    e.prenom,
                    e.genre,
                    e.statut,
                    c.nom_classe as classe_nom,
                    c.niveau as classe_niveau
                FROM eleves e
                LEFT JOIN classes c ON e.id_classe = c.id_classe
                WHERE e.nom LIKE ? OR e.prenom LIKE ?
                ORDER BY e.nom, e.prenom
            """, (search_pattern, search_pattern))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_all_classes(self) -> List[Dict[str, Any]]:
        """Récupère toutes les classes avec statistiques"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    c.id_classe,
                    c.nom_classe as nom,
                    c.niveau,
                    c.effectif as capacite,
                    c.statut,
                    COUNT(e.id_eleve) as effectif_reel,
                    COUNT(CASE WHEN e.statut = 'actif' THEN 1 END) as eleves_actifs,
                    COUNT(CASE WHEN e.statut = 'inactif' THEN 1 END) as eleves_inactifs,
                    COALESCE(AVG(n.notes), 0) as moyenne_generale
                FROM classes c
                LEFT JOIN eleves e ON c.id_classe = e.id_classe
                LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                GROUP BY c.id_classe, c.nom_classe, c.niveau, c.effectif, c.statut
                ORDER BY c.niveau, c.nom_classe
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_classe_stats(self) -> Dict[str, Any]:
        """Statistiques globales des classes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_classes,
                    COUNT(CASE WHEN statut = 'actif' THEN 1 END) as classes_actives,
                    AVG(capacite) as capacite_moyenne,
                    SUM(capacite) as capacite_totale
                FROM classes
            """)
            return dict(cursor.fetchone())
    
    def _sp_get_classes_by_niveau(self, niveau: str) -> List[Dict[str, Any]]:
        """Récupère les classes d'un niveau spécifique"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    c.id_classe,
                    c.nom_classe as nom,
                    c.niveau,
                    c.effectif as capacite,
                    COUNT(e.id_eleve) as effectif_reel
                FROM classes c
                LEFT JOIN eleves e ON c.id_classe = e.id_classe AND e.statut = 'actif'
                WHERE c.niveau = ?
                GROUP BY c.id_classe, c.nom_classe, c.niveau, c.effectif
                ORDER BY c.nom_classe
            """, (niveau,))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_all_matieres(self) -> List[Dict[str, Any]]:
        """Récupère toutes les matières"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom,
                    m.description,
                    m.coefficient,
                    m.classe_id,
                    c.nom_classe as classe_nom,
                    c.niveau as classe_niveau
                FROM matieres m
                LEFT JOIN classes c ON m.classe_id = c.id_classe
                ORDER BY m.nom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_matieres_by_classe(self, classe_id: int) -> List[Dict[str, Any]]:
        """Récupère les matières d'une classes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom,
                    m.description,
                    m.coefficient
                FROM matieres m
                WHERE m.classe_id = ?
                ORDER BY m.nom
            """, (classe_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_notes_by_eleve(self, eleve_id: int) -> List[Dict[str, Any]]:
        """Récupère les notes d'un élève"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    n.id_note,
                    n.notes,
                    n.coefficient,
                    n.type_evaluation,
                    n.date_evaluation,
                    n.commentaire,
                    m.nom as matiere_nom,
                    m.coefficient as matiere_coefficient,
                    p.nom as professeur_nom,
                    p.prenom as professeur_prenom
                FROM notes n
                LEFT JOIN matieres m ON n.id_matiere = m.id_matiere
                LEFT JOIN professeurs p ON n.id_professeur = p.id_professeur
                WHERE n.id_eleve = ?
                ORDER BY n.date_evaluation DESC
            """, (eleve_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_notes_stats(self) -> Dict[str, Any]:
        """Statistiques globales des notes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_notes,
                    AVG(notes) as moyenne_generale,
                    MIN(notes) as note_min,
                    MAX(notes) as note_max,
                    COUNT(DISTINCT id_eleve) as eleves_avec_notes,
                    COUNT(DISTINCT id_matiere) as matieres_evaluees
                FROM notes
            """)
            return dict(cursor.fetchone())
    
    def _sp_get_moyennes_by_classe(self, classe_id: int) -> List[Dict[str, Any]]:
        """Récupère les moyennes par matière pour une classes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom as matiere_nom,
                    COUNT(n.id_note) as nb_notes,
                    AVG(n.notes) as moyenne_classe,
                    MIN(n.notes) as note_min,
                    MAX(n.notes) as note_max
                FROM matieres m
                LEFT JOIN notes n ON m.id_matiere = n.id_matiere
                LEFT JOIN eleves e ON n.id_eleve = e.id_eleve
                WHERE m.classe_id = ? AND e.id_classe = ?
                GROUP BY m.id_matiere, m.nom
                ORDER BY m.nom
            """, (classe_id, classe_id))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_all_cours(self) -> List[Dict[str, Any]]:
        """Récupère tous les cours"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    c.id_cours,
                    c.nom as cours_nom,
                    c.date,
                    c.heure_debut,
                    c.heure_fin,
                    c.statut,
                    cl.nom as classe_nom,
                    cl.niveau as classe_niveau,
                    m.nom as matiere_nom,
                    p.nom as professeur_nom,
                    p.prenom as professeur_prenom,
                    s.nom as salle_nom
                FROM cours c
                LEFT JOIN classes cl ON c.classe_id = cl.id_classe
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                ORDER BY c.date DESC, c.heure_debut DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_cours_by_classe(self, classe_id: int) -> List[Dict[str, Any]]:
        """Récupère les cours d'une classes"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    c.id_cours,
                    c.nom as cours_nom,
                    c.date,
                    c.heure_debut,
                    c.heure_fin,
                    c.statut,
                    m.nom as matiere_nom,
                    p.nom as professeur_nom,
                    p.prenom as professeur_prenom,
                    s.nom as salle_nom
                FROM cours c
                LEFT JOIN matieres m ON c.matiere_id = m.id_matiere
                LEFT JOIN professeurs p ON c.professeur_id = p.id_professeur
                LEFT JOIN salles s ON c.salle_id = s.id_salle
                WHERE c.classe_id = ?
                ORDER BY c.date DESC, c.heure_debut DESC
            """, (classe_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_cours_stats(self) -> Dict[str, Any]:
        """Statistiques des cours"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_cours,
                    COUNT(CASE WHEN statut = 'termine' THEN 1 END) as cours_termines,
                    COUNT(CASE WHEN statut = 'en_cours' THEN 1 END) as cours_en_cours,
                    COUNT(CASE WHEN statut = 'planifie' THEN 1 END) as cours_planifies,
                    COUNT(DISTINCT classe_id) as classes_concernees,
                    COUNT(DISTINCT matiere_id) as matieres_enseignees
                FROM cours
            """)
            return dict(cursor.fetchone())
    
    def _sp_get_all_professeurs(self) -> List[Dict[str, Any]]:
        """Récupère tous les professeurs"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    p.id_professeur,
                    p.nom,
                    p.prenom,
                    p.email,
                    p.telephone,
                    p.specialite,
                    p.statut,
                    COUNT(DISTINCT c.id_cours) as nb_cours,
                    COUNT(DISTINCT c.classe_id) as nb_classes
                FROM professeurs p
                LEFT JOIN cours c ON p.id_professeur = c.professeur_id
                GROUP BY p.id_professeur, p.nom, p.prenom, p.email, p.telephone, p.specialite, p.statut
                ORDER BY p.nom, p.prenom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _sp_get_professeur_stats(self) -> Dict[str, Any]:
        """Statistiques des professeurs"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_professeurs,
                    COUNT(CASE WHEN statut = 'actif' THEN 1 END) as professeurs_actifs,
                    COUNT(CASE WHEN statut = 'inactif' THEN 1 END) as professeurs_inactifs,
                    COUNT(DISTINCT specialite) as specialites_uniques
                FROM professeurs
            """)
            return dict(cursor.fetchone())
    
    def _sp_get_dashboard_stats(self) -> Dict[str, Any]:
        """Statistiques pour le dashboard principal"""
        with self._connect() as conn:
            # Statistiques élèves
            eleves_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_eleves,
                    COUNT(CASE WHEN statut = 'actif' THEN 1 END) as eleves_actifs
                FROM eleves
            """).fetchone()
            
            # Statistiques classes
            classes_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_classes,
                    COUNT(CASE WHEN statut = 'actif' THEN 1 END) as classes_actives
                FROM classes
            """).fetchone()
            
            # Statistiques notes
            notes_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_notes,
                    AVG(notes) as moyenne_generale
                FROM notes
            """).fetchone()
            
            # Statistiques cours
            cours_stats = conn.execute("""
                SELECT 
                    COUNT(*) as total_cours,
                    COUNT(CASE WHEN statut = 'termine' THEN 1 END) as cours_termines
                FROM cours
            """).fetchone()
            
            return {
                'eleves': dict(eleves_stats),
                'classes': dict(classes_stats),
                'notes': dict(notes_stats),
                'cours': dict(cours_stats)
            }
    
    def _sp_get_global_stats(self) -> Dict[str, Any]:
        """Statistiques globales de l'établissement"""
        with self._connect() as conn:
            cursor = conn.execute("""
                SELECT 
                    (SELECT COUNT(*) FROM eleves WHERE statut = 'actif') as eleves_actifs,
                    (SELECT COUNT(*) FROM classes WHERE statut = 'actif') as classes_actives,
                    (SELECT COUNT(*) FROM professeurs WHERE statut = 'actif') as professeurs_actifs,
                    (SELECT COUNT(*) FROM notes) as total_notes,
                    (SELECT AVG(notes) FROM notes) as moyenne_generale,
                    (SELECT COUNT(*) FROM cours WHERE statut = 'termine') as cours_termines,
                    (SELECT COUNT(DISTINCT matiere_id) FROM matieres) as matieres_uniques
            """)
            return dict(cursor.fetchone())

# ===== FONCTIONS D'ACCÈS RAPIDE =====

def get_sp_manager(db_path: str = "database/edumanager.db") -> StoredProcedureManager:
    """Retourne l'instance singleton du gestionnaire de procédures"""
    return StoredProcedureManager(db_path)

def execute_procedure(procedure_name: str, *args, **kwargs) -> Any:
    """Exécute une procédure stockée"""
    manager = get_sp_manager()
    return manager.execute(procedure_name, *args, **kwargs)

def invalidate_cache(pattern: str = None):
    """Invalide le cache des procédures"""
    manager = get_sp_manager()
    manager.invalidate_cache(pattern)

def get_performance_stats() -> Dict[str, Any]:
    """Retourne les statistiques de performance"""
    manager = get_sp_manager()
    return manager.get_stats()

# ===== PROCÉDURES D'OPTIMISATION SPÉCIALISÉES =====

    # Précharger les données les plus utilisées
    critical_procedures = [
        'sp_get_all_eleves',
        'sp_get_all_classes', 
        'sp_get_all_matieres',
        'sp_get_dashboard_stats',
        'sp_get_global_stats'
    ]
    
    for procedure in critical_procedures:
        try:
            manager.execute(procedure)
            print(f"✅ {procedure} préchargée")
        except Exception as e:
            print(f"⚠️ Erreur préchargement {procedure}: {e}")
    
    print("✅ Préchargement terminé")

def optimize_database():
    """Applique les optimisations de base de données"""
    manager = get_sp_manager()
    
    with manager._connect() as conn:
        # Créer des index pour les requêtes fréquentes
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_eleves_classe_statut ON eleves(id_classe, statut)",
            "CREATE INDEX IF NOT EXISTS idx_eleves_nom_prenom ON eleves(nom, prenom)",
            "CREATE INDEX IF NOT EXISTS idx_notes_eleve_date ON notes(id_eleve, date_evaluation)",
            "CREATE INDEX IF NOT EXISTS idx_notes_matiere ON notes(id_matiere)",
            "CREATE INDEX IF NOT EXISTS idx_cours_classe_date ON cours(classe_id, date)",
            "CREATE INDEX IF NOT EXISTS idx_cours_professeur ON cours(professeur_id)",
            "CREATE INDEX IF NOT EXISTS idx_matieres_classe ON matieres(classe_id)",
            "CREATE INDEX IF NOT EXISTS idx_classes_niveau ON classes(niveau)"
        ]
        
        for index_sql in indexes:
            try:
                conn.execute(index_sql)
                print(f"✅ Index créé: {index_sql.split()[-1]}")
            except Exception as e:
                print(f"⚠️ Erreur création index: {e}")
        
        conn.commit()
        print("✅ Optimisations de base de données appliquées")

if __name__ == "__main__":
    # Test des procédures stockées
    print("🧪 Test des procédures stockées...")
    
    # Initialiser le gestionnaire
    manager = get_sp_manager()
    
    # Optimiser la base de données
    optimize_database()
    
    # Précharger les données critiques
    # preload_critical_data()  # Supprimé - système de cache supprimé
    
    # Tester quelques procédures
    try:
        eleves = manager.execute('sp_get_all_eleves')
        print(f"✅ {len(eleves)} élèves récupérés")
        
        classes = manager.execute('sp_get_all_classes')
        print(f"✅ {len(classes)} classes récupérées")
        
        stats = manager.execute('sp_get_dashboard_stats')
        print(f"✅ Statistiques dashboard: {stats}")
        
        # Afficher les statistiques de performance
        perf_stats = manager.get_stats()
        print(f"📊 Statistiques de performance: {perf_stats}")
        
    except Exception as e:
        print(f"❌ Erreur test: {e}")
    
    print("✅ Test terminé")
