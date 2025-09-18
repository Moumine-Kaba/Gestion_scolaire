#!/usr/bin/env python3
"""
SYSTÈME DE PRÉCHARGEMENT INTELLIGENT POUR VUES
==============================================

Ce module implémente un système de préchargement intelligent qui charge
les données des vues en arrière-plan pour éviter les délais de 10 secondes.

Fonctionnalités :
- Préchargement automatique des données critiques
- Pool de données en mémoire
- Chargement asynchrone
- Gestion intelligente des priorités
- Compatible avec l'architecture existante
"""

from database.connection import get_db_connection
from database.connection import get_db_connection
from database.connection import get_db_connection
import threading
import time
import queue
from typing import Dict, List, Any, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from enum import Enum
# Remplacé par SQL Server  # Remplacé par SQL Server
import os

class Priority(Enum):
    """Priorités de préchargement"""
    CRITICAL = 1  # Données essentielles (élèves, classes)
    HIGH = 2      # Données importantes (matières, notes)
    MEDIUM = 3    # Données moyennement utilisées (cours, professeurs)
    LOW = 4       # Données rarement utilisées (statistiques, rapports)

@dataclass
class PreloadTask:
    """Tâche de préchargement"""
    name: str
    priority: Priority
    function: Callable
    args: tuple = ()
    kwargs: dict = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}
        if self.dependencies is None:
            self.dependencies = []

class IntelligentPreloader:
    """
    Système de préchargement intelligent pour les vues
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.data_pool = {}
        self.preload_tasks = {}
        self.task_queue = queue.PriorityQueue()
        self.executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="Preloader")
        self.stats = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'total_time_saved': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
        self.is_running = False
        self.worker_thread = None
        
        self._initialize_preload_tasks()
        self._initialized = True
        print("✅ IntelligentPreloader initialisé")
    
    def _initialize_preload_tasks(self):
        """Initialise les tâches de préchargement"""
        
        # === TÂCHES CRITIQUES (Priorité 1) ===
        self.preload_tasks['eleves_all'] = PreloadTask(
            name='eleves_all',
            priority=Priority.CRITICAL,
            function=self._load_all_eleves,
            dependencies=[]
        )
        
        self.preload_tasks['classes_all'] = PreloadTask(
            name='classes_all',
            priority=Priority.CRITICAL,
            function=self._load_all_classes,
            dependencies=[]
        )
        
        # === TÂCHES HAUTES PRIORITÉS (Priorité 2) ===
        self.preload_tasks['matieres_all'] = PreloadTask(
            name='matieres_all',
            priority=Priority.HIGH,
            function=self._load_all_matieres,
            dependencies=['classes_all']
        )
        
        self.preload_tasks['professeurs_all'] = PreloadTask(
            name='professeurs_all',
            priority=Priority.HIGH,
            function=self._load_all_professeurs,
            dependencies=[]
        )
        
        # === TÂCHES MOYENNES PRIORITÉS (Priorité 3) ===
        self.preload_tasks['cours_all'] = PreloadTask(
            name='cours_all',
            priority=Priority.MEDIUM,
            function=self._load_all_cours,
            dependencies=['classes_all', 'matieres_all', 'professeurs_all']
        )
        
        self.preload_tasks['notes_stats'] = PreloadTask(
            name='notes_stats',
            priority=Priority.MEDIUM,
            function=self._load_notes_stats,
            dependencies=['eleves_all']
        )
        
        # === TÂCHES FAIBLES PRIORITÉS (Priorité 4) ===
        self.preload_tasks['dashboard_stats'] = PreloadTask(
            name='dashboard_stats',
            priority=Priority.LOW,
            function=self._load_dashboard_stats,
            dependencies=['eleves_all', 'classes_all', 'notes_stats']
        )
        
        self.preload_tasks['global_stats'] = PreloadTask(
            name='global_stats',
            priority=Priority.LOW,
            function=self._load_global_stats,
            dependencies=['dashboard_stats']
        )
        
        print(f"✅ {len(self.preload_tasks)} tâches de préchargement initialisées")
    
    def _connect_db(self):
        """Connexion optimisée à la base de données"""
        db_path = "database/edumanager.db"
        conn = get_db_connection()
        # conn.row_factory = sqlite3.Row  # Remplacé par SQL Server
        
        # Optimisations SQLite
        return conn
    
    def _load_all_eleves(self) -> List[Dict[str, Any]]:
        """Charge tous les élèves avec informations complètes"""
        with self._connect_db() as conn:
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
                    c.nom as classe_nom,
                    c.niveau as classe_niveau,
                    COUNT(n.id_note) as nb_notes,
                    COALESCE(AVG(n.notes), 0) as moyenne_generale
                FROM eleves e
                LEFT JOIN classes c ON e.id_classe = c.id_classe
                LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                GROUP BY e.id_eleve, e.nom, e.prenom, e.genre, e.date_naissance, 
                         e.adresse, e.telephone, e.email, 
                         e.statut, e.date_inscription, e.id_classe, c.nom, c.niveau
                ORDER BY e.nom, e.prenom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _load_all_classes(self) -> List[Dict[str, Any]]:
        """Charge toutes les classes avec statistiques"""
        with self._connect_db() as conn:
            cursor = conn.execute("""
                SELECT 
                    c.id_classe,
                    c.nom,
                    c.niveau,
                    c.statut,
                    COUNT(e.id_eleve) as effectif,
                    COUNT(CASE WHEN e.statut = 'actif' THEN 1 END) as eleves_actifs,
                    COUNT(CASE WHEN e.statut = 'inactif' THEN 1 END) as eleves_inactifs,
                    COALESCE(AVG(n.notes), 0) as moyenne_generale
                FROM classes c
                LEFT JOIN eleves e ON c.id_classe = e.id_classe
                LEFT JOIN notes n ON e.id_eleve = n.id_eleve
                GROUP BY c.id_classe, c.nom, c.niveau, c.statut
                ORDER BY c.niveau, c.nom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _load_all_matieres(self) -> List[Dict[str, Any]]:
        """Charge toutes les matières"""
        with self._connect_db() as conn:
            cursor = conn.execute("""
                SELECT 
                    m.id_matiere,
                    m.nom,
                    m.description,
                    m.coefficient,
                    m.classe_id,
                    c.nom as classe_nom,
                    c.niveau as classe_niveau
                FROM matieres m
                LEFT JOIN classes c ON m.classe_id = c.id_classe
                ORDER BY m.nom
            """)
            return [dict(row) for row in cursor.fetchall()]
    
    def _load_all_professeurs(self) -> List[Dict[str, Any]]:
        """Charge tous les professeurs"""
        with self._connect_db() as conn:
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
    
    def _load_all_cours(self) -> List[Dict[str, Any]]:
        """Charge tous les cours"""
        with self._connect_db() as conn:
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
    
    def _load_notes_stats(self) -> Dict[str, Any]:
        """Charge les statistiques des notes"""
        with self._connect_db() as conn:
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
    
    def _load_dashboard_stats(self) -> Dict[str, Any]:
        """Charge les statistiques du dashboard"""
        with self._connect_db() as conn:
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
    
    def _load_global_stats(self) -> Dict[str, Any]:
        """Charge les statistiques globales"""
        with self._connect_db() as conn:
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
    
    def _can_execute_task(self, task: PreloadTask) -> bool:
        """Vérifie si une tâche peut être exécutée (dépendances satisfaites)"""
        for dep in task.dependencies:
            if dep not in self.data_pool:
                return False
        return True
    
    def _worker_thread(self):
        """Thread de travail pour le préchargement"""
        while self.is_running:
            try:
                # Récupérer une tâche de la queue
                priority, task = self.task_queue.get(timeout=1)
                
                # Vérifier les dépendances
                if not self._can_execute_task(task):
                    # Remettre en queue pour plus tard
                    self.task_queue.put((priority, task))
                    continue
                
                # Exécuter la tâche
                start_time = time.time()
                try:
                    result = task.function()
                    self.data_pool[task.name] = result
                    self.stats['tasks_completed'] += 1
                    execution_time = time.time() - start_time
                    print(f"✅ {task.name} préchargé en {execution_time:.3f}s")
                    
                except Exception as e:
                    self.stats['tasks_failed'] += 1
                    print(f"❌ Erreur préchargement {task.name}: {e}")
                
                self.task_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Erreur worker thread: {e}")
    
    def start_preloading(self):
        """Démarre le préchargement intelligent"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Ajouter les tâches à la queue par priorité
        for task in self.preload_tasks.values():
            self.task_queue.put((task.priority.value, task))
        
        # Démarrer le thread de travail
        self.worker_thread = threading.Thread(target=self._worker_thread, daemon=True)
        self.worker_thread.start()
        
        print("🚀 Préchargement intelligent démarré")
    
    def stop_preloading(self):
        """Arrête le préchargement intelligent"""
        self.is_running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        print("⏹️ Préchargement intelligent arrêté")
    
    def get_data(self, data_name: str) -> Optional[Any]:
        """Récupère les données préchargées"""
        if data_name in self.data_pool:
            self.stats['cache_hits'] += 1
            return self.data_pool[data_name]
        
        self.stats['cache_misses'] += 1
        return None

        for task in critical_tasks:
            try:
                start_time = time.time()
                result = task.function()
                self.data_pool[task.name] = result
                execution_time = time.time() - start_time
                print(f"✅ {task.name} préchargé en {execution_time:.3f}s")
                
            except Exception as e:
                print(f"❌ Erreur préchargement {task.name}: {e}")
        
        print("✅ Préchargement des données critiques terminé")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du préchargeur"""
        total_tasks = self.stats['tasks_completed'] + self.stats['tasks_failed']
        success_rate = (self.stats['tasks_completed'] / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            'tasks_completed': self.stats['tasks_completed'],
            'tasks_failed': self.stats['tasks_failed'],
            'success_rate': f"{success_rate:.1f}%",
            'cache_hits': self.stats['cache_hits'],
            'cache_misses': self.stats['cache_misses'],
            'data_pool_size': len(self.data_pool),
            'is_running': self.is_running
        }

# ===== FONCTIONS D'ACCÈS RAPIDE =====

def get_preloader() -> IntelligentPreloader:
    """Retourne l'instance singleton du préchargeur"""
    return IntelligentPreloader()

def start_intelligent_preloading():
    """Démarre le préchargement intelligent"""
    preloader = get_preloader()
    preloader.start_preloading()

def stop_intelligent_preloading():
    """Arrête le préchargement intelligent"""
    preloader = get_preloader()
    preloader.stop_preloading()

        return []

def get_classes_data() -> List[Dict[str, Any]]:
    """Récupère les données des classes (préchargées ou en temps réel)"""
    data = get_preloaded_data('classes_all')
    if data is not None:
        return data
    
    # Fallback vers le contrôleur
    try:
        from src.modules.academic.classes.controllers.classe_controller import get_all_classes
        return get_all_classes()
    except Exception as e:
        print(f"⚠️ Erreur fallback classes: {e}")
        return []

def get_matieres_data() -> List[Dict[str, Any]]:
    """Récupère les données des matières (préchargées ou en temps réel)"""
    data = get_preloaded_data('matieres_all')
    if data is not None:
        return data
    
    # Fallback vers le contrôleur
    try:
        from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
        return get_all_matieres()
    except Exception as e:
        print(f"⚠️ Erreur fallback matières: {e}")
        return []

def get_dashboard_stats() -> Dict[str, Any]:
    """Récupère les statistiques du dashboard (préchargées ou en temps réel)"""
    data = get_preloaded_data('dashboard_stats')
    if data is not None:
        return data
    
    # Fallback vers le préchargeur
    preloader = get_preloader()
    return preloader._load_dashboard_stats()

if __name__ == "__main__":
    # Test du système de préchargement intelligent
    print("🧪 Test du système de préchargement intelligent...")
    
    # Précharger les données critiques
    # preload_critical_data()  # Supprimé - système de cache supprimé
    
    # Tester l'accès aux données
    eleves = get_eleves_data()
    print(f"✅ {len(eleves)} élèves récupérés")
    
    classes = get_classes_data()
    print(f"✅ {len(classes)} classes récupérées")
    
    matieres = get_matieres_data()
    print(f"✅ {len(matieres)} matières récupérées")
    
    # Afficher les statistiques
    stats = get_preloader_stats()
    print(f"📊 Statistiques: {stats}")
    
    print("✅ Test terminé")
