# -*- coding: utf-8 -*-
"""
Système de préchargement intelligent des vues pour EduManager+
- Préchargement en arrière-plan
- Chargement paresseux (lazy loading)
- Pool de vues pré-initialisées
- Gestion intelligente de la mémoire
"""

import threading
import time
import queue
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import gc

class ViewLoadPriority(Enum):
    """Priorités de chargement des vues"""
    CRITICAL = 1    # Vues critiques (classes, cours, notes)
    HIGH = 2        # Vues importantes (élèves, professeurs)
    MEDIUM = 3      # Vues moyennement utilisées
    LOW = 4         # Vues rarement utilisées

class ViewPreloader:
    """Gestionnaire de préchargement des vues"""
    
    def __init__(self):
        self._view_pool = {}
        self._loading_queue = queue.PriorityQueue()
        self._loading_threads = []
        self._max_threads = 3
        self._max_pool_size = 10
        self._view_factories = {}
        self._loading_stats = {
            "preloaded": 0,
            "cache_hits": 0,
            "loading_time": 0
        }
        
        # Démarrer les threads de chargement
        self._start_loading_threads()
        
        print("✅ Préchargeur de vues initialisé")
    
    def _start_loading_threads(self):
        """Démarre les threads de chargement en arrière-plan"""
        for i in range(self._max_threads):
            thread = threading.Thread(
                target=self._loading_worker,
                name=f"ViewLoader-{i}",
                daemon=True
            )
            thread.start()
            self._loading_threads.append(thread)
    
    def _loading_worker(self):
        """Worker thread pour charger les vues en arrière-plan"""
        while True:
            try:
                priority, view_key, factory_func, args, kwargs = self._loading_queue.get(timeout=1)
                
                start_time = time.time()
                print(f"🔄 Préchargement: {view_key} (priorité {priority})")
                
                try:
                    # Créer la vue
                    view_instance = factory_func(*args, **kwargs)
                    
                    # Stocker dans le pool
                    with threading.Lock():
                        self._view_pool[view_key] = {
                            "instance": view_instance,
                            "created_at": time.time(),
                            "access_count": 0,
                            "last_access": time.time()
                        }
                    
                    loading_time = time.time() - start_time
                    self._loading_stats["preloaded"] += 1
                    self._loading_stats["loading_time"] += loading_time
                    
                    print(f"✅ Vue préchargée: {view_key} ({loading_time:.2f}s)")
                    
                except Exception as e:
                    print(f"⚠️ Erreur préchargement {view_key}: {e}")
                
                self._loading_queue.task_done()
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"⚠️ Erreur worker thread: {e}")
    
    def register_view_factory(self, view_key: str, factory_func: Callable):
        """Enregistre une factory pour créer une vue"""
        self._view_factories[view_key] = factory_func
        print(f"📝 Factory enregistrée: {view_key}")
        
        # Vérifier si déjà dans le pool
        if view_key in self._view_pool:
            print(f"📋 Vue déjà en pool: {view_key}")
            return True
        
        # Ajouter à la queue de chargement
        factory_func = self._view_factories[view_key]
        self._loading_queue.put((priority.value, view_key, factory_func, args, kwargs))
        
        print(f"📋 Préchargement programmé: {view_key}")
        return True
    
    def get_view(self, view_key: str, *args, **kwargs):
        """Récupère une vue du pool ou la crée si nécessaire"""
        # Vérifier le pool d'abord
        if view_key in self._view_pool:
            pool_item = self._view_pool[view_key]
            pool_item["access_count"] += 1
            pool_item["last_access"] = time.time()
            self._loading_stats["cache_hits"] += 1
            
            print(f"📋 Vue récupérée du pool: {view_key}")
            return pool_item["instance"]
        
        # Créer la vue immédiatement si pas en pool
        if view_key in self._view_factories:
            print(f"🚀 Création immédiate: {view_key}")
            factory_func = self._view_factories[view_key]
            view_instance = factory_func(*args, **kwargs)
            
            # Ajouter au pool
            self._view_pool[view_key] = {
                "instance": view_instance,
                "created_at": time.time(),
                "access_count": 1,
                "last_access": time.time()
            }
            
            return view_instance
        
        print(f"⚠️ Vue non trouvée: {view_key}")
        return None
    
    def cleanup_old_views(self, max_age_seconds: int = 300):
        """Nettoie les vues anciennes du pool"""
        current_time = time.time()
        views_to_remove = []
        
        with threading.Lock():
            for view_key, pool_item in self._view_pool.items():
                age = current_time - pool_item["last_access"]
                if age > max_age_seconds:
                    views_to_remove.append(view_key)
        
        for view_key in views_to_remove:
            self.remove_view(view_key)
            print(f"🗑️ Vue ancienne supprimée: {view_key}")
    
    def remove_view(self, view_key: str):
        """Supprime une vue du pool"""
        if view_key in self._view_pool:
            pool_item = self._view_pool[view_key]
            
            # Nettoyer l'instance
            try:
                if hasattr(pool_item["instance"], 'destroy'):
                    pool_item["instance"].destroy()
            except Exception as e:
                print(f"⚠️ Erreur destruction vue {view_key}: {e}")
            
            del self._view_pool[view_key]
            print(f"🗑️ Vue supprimée du pool: {view_key}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du préchargeur"""
        avg_loading_time = 0
        if self._loading_stats["preloaded"] > 0:
            avg_loading_time = self._loading_stats["loading_time"] / self._loading_stats["preloaded"]
        
        return {
            "pool_size": len(self._view_pool),
            "pool_keys": list(self._view_pool.keys()),
            "registered_factories": len(self._view_factories),
            "queue_size": self._loading_queue.qsize(),
            "stats": {
                **self._loading_stats,
                "avg_loading_time": f"{avg_loading_time:.2f}s"
            }
        }

        for view_key, priority in critical_views:
            if view_key in self._view_factories:
                self.preload_view(view_key, priority)
        
        print("✅ Préchargement des vues critiques programmé")

# Instance globale du préchargeur
_view_preloader = None

def get_view_preloader() -> ViewPreloader:
    """Retourne l'instance globale du préchargeur de vues"""
    global _view_preloader
    if _view_preloader is None:
        _view_preloader = ViewPreloader()
    return _view_preloader

def register_view_factory(view_key: str, factory_func: Callable):
    """Enregistre une factory de vue"""
    preloader = get_view_preloader()
    preloader.register_view_factory(view_key, factory_func)

def preload_view(view_key: str, priority: ViewLoadPriority = ViewLoadPriority.MEDIUM, 
                *args, **kwargs):
    """Programme le préchargement d'une vue"""
    preloader = get_view_preloader()
    return preloader.preload_view(view_key, priority, *args, **kwargs)

def get_preloaded_view(view_key: str, *args, **kwargs):
    """Récupère une vue préchargée"""
    preloader = get_view_preloader()
    return preloader.get_view(view_key, *args, **kwargs)

def cleanup_view_pool():
    """Nettoie le pool de vues"""
    preloader = get_view_preloader()
    preloader.cleanup_old_views()

def preload_critical_views():
    """Précharge les vues critiques"""
    preloader = get_view_preloader()
    preloader.preload_critical_views()
