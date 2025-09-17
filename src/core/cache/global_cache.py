# -*- coding: utf-8 -*-
"""
Système de cache global avancé pour EduManager+
- Cache multi-niveaux (mémoire + disque)
- Invalidation intelligente
- Préchargement des données critiques
- Synchronisation thread-safe
"""

import time
import json
import pickle
import threading
import os
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
import hashlib

class GlobalCacheManager:
    """Gestionnaire de cache global avec invalidation intelligente"""
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        self._memory_cache = {}
        self._cache_lock = threading.RLock()
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "invalidations": 0
        }
        
        # Créer le dossier de cache
        os.makedirs(cache_dir, exist_ok=True)
        
        # Configuration du cache
        self.default_ttl = 300  # 5 minutes par défaut
        self.max_memory_items = 1000
        self.max_disk_size_mb = 100
        
        print(f"✅ Cache global initialisé: {cache_dir}")
    
    def _get_cache_key(self, key: str, namespace: str = "default") -> str:
        """Génère une clé de cache unique"""
        return f"{namespace}:{key}"
    
    def _get_file_path(self, cache_key: str) -> str:
        """Retourne le chemin du fichier de cache"""
        # Utiliser un hash pour éviter les noms de fichiers trop longs
        hash_key = hashlib.md5(cache_key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{hash_key}.cache")
    
    def get(self, key: str, namespace: str = "default") -> Optional[Any]:
        """Récupère une valeur du cache"""
        cache_key = self._get_cache_key(key, namespace)
        
        with self._cache_lock:
            # Vérifier le cache mémoire d'abord
            if cache_key in self._memory_cache:
                data, timestamp, ttl = self._memory_cache[cache_key]
                if time.time() - timestamp < ttl:
                    self._cache_stats["hits"] += 1
                    return data
                else:
                    # Expiré, le supprimer
                    del self._memory_cache[cache_key]
            
            # Vérifier le cache disque
            file_path = self._get_file_path(cache_key)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        cached_data = pickle.load(f)
                    
                    data, timestamp, ttl = cached_data
                    if time.time() - timestamp < ttl:
                        # Remettre en cache mémoire
                        self._memory_cache[cache_key] = cached_data
                        self._cache_stats["hits"] += 1
                        return data
                    else:
                        # Expiré, supprimer le fichier
                        os.remove(file_path)
                except Exception as e:
                    print(f"⚠️ Erreur lecture cache disque: {e}")
            
            self._cache_stats["misses"] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None, namespace: str = "default") -> bool:
        """Stocke une valeur dans le cache"""
        cache_key = self._get_cache_key(key, namespace)
        ttl = ttl or self.default_ttl
        timestamp = time.time()
        
        cached_data = (value, timestamp, ttl)
        
        with self._cache_lock:
            try:
                # Stocker en mémoire
                self._memory_cache[cache_key] = cached_data
                
                # Limiter la taille du cache mémoire
                if len(self._memory_cache) > self.max_memory_items:
                    # Supprimer les éléments les plus anciens
                    oldest_key = min(self._memory_cache.keys(), 
                                   key=lambda k: self._memory_cache[k][1])
                    del self._memory_cache[oldest_key]
                
                # Stocker sur disque
                file_path = self._get_file_path(cache_key)
                with open(file_path, 'wb') as f:
                    pickle.dump(cached_data, f)
                
                self._cache_stats["sets"] += 1
                return True
                
            except Exception as e:
                print(f"⚠️ Erreur écriture cache: {e}")
                return False
    
    def invalidate(self, key: str, namespace: str = "default") -> bool:
        """Invalide une clé de cache"""
        cache_key = self._get_cache_key(key, namespace)
        
        with self._cache_lock:
            removed = False
            
            # Supprimer du cache mémoire
            if cache_key in self._memory_cache:
                del self._memory_cache[cache_key]
                removed = True
            
            # Supprimer du cache disque
            file_path = self._get_file_path(cache_key)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    removed = True
                except Exception as e:
                    print(f"⚠️ Erreur suppression cache disque: {e}")
            
            if removed:
                self._cache_stats["invalidations"] += 1
            
            return removed
    
    def invalidate_namespace(self, namespace: str) -> int:
        """Invalide toutes les clés d'un namespace"""
        removed_count = 0
        
        with self._cache_lock:
            # Supprimer du cache mémoire
            keys_to_remove = [k for k in self._memory_cache.keys() if k.startswith(f"{namespace}:")]
            for key in keys_to_remove:
                del self._memory_cache[key]
                removed_count += 1
            
            # Supprimer du cache disque
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    file_path = os.path.join(self.cache_dir, filename)
                    try:
                        with open(file_path, 'rb') as f:
                            cached_data = pickle.load(f)
                        
                        # Vérifier si c'est du bon namespace (on ne peut pas le savoir directement)
                        # On supprime tous les fichiers et on laisse le système les recréer
                        os.remove(file_path)
                        removed_count += 1
                    except Exception:
                        pass
        
        self._cache_stats["invalidations"] += removed_count
        print(f"🗑️ Namespace '{namespace}' invalidé: {removed_count} éléments")
        return removed_count
    
    def clear_all(self) -> int:
        """Vide tout le cache"""
        removed_count = 0
        
        with self._cache_lock:
            # Vider le cache mémoire
            removed_count += len(self._memory_cache)
            self._memory_cache.clear()
            
            # Vider le cache disque
            for filename in os.listdir(self.cache_dir):
                if filename.endswith('.cache'):
                    file_path = os.path.join(self.cache_dir, filename)
                    try:
                        os.remove(file_path)
                        removed_count += 1
                    except Exception:
                        pass
        
        print(f"🗑️ Cache vidé: {removed_count} éléments")
        return removed_count
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        with self._cache_lock:
            hit_rate = 0
            total_requests = self._cache_stats["hits"] + self._cache_stats["misses"]
            if total_requests > 0:
                hit_rate = self._cache_stats["hits"] / total_requests * 100
            
            return {
                "memory_items": len(self._memory_cache),
                "disk_files": len([f for f in os.listdir(self.cache_dir) if f.endswith('.cache')]),
                "hit_rate": f"{hit_rate:.2f}%",
                "stats": self._cache_stats.copy()
            }
    
    def preload_data(self, data_loader: Callable, key: str, namespace: str = "preload") -> bool:
        """Précharge des données dans le cache"""
        try:
            print(f"🔄 Préchargement: {key}")
            data = data_loader()
            success = self.set(key, data, namespace=namespace)
            if success:
                print(f"✅ Préchargement réussi: {key}")
            return success
        except Exception as e:
            print(f"⚠️ Erreur préchargement {key}: {e}")
            return False

# Instance globale du gestionnaire de cache
_cache_manager = None

def get_global_cache() -> GlobalCacheManager:
    """Retourne l'instance globale du gestionnaire de cache"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = GlobalCacheManager()
    return _cache_manager

def cached(ttl: int = 300, namespace: str = "default"):
    """Décorateur pour mettre en cache les résultats de fonctions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Générer une clé de cache basée sur la fonction et ses arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            cache = get_global_cache()
            
            # Essayer de récupérer du cache
            result = cache.get(cache_key, namespace)
            if result is not None:
                return result
            
            # Exécuter la fonction et mettre en cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl, namespace)
            return result
        
        return wrapper
    return decorator

def invalidate_cache(pattern: str, namespace: str = "default"):
    """Invalide le cache selon un pattern"""
    cache = get_global_cache()
    # Pour l'instant, on invalide tout le namespace
    # Une version plus sophistiquée pourrait utiliser des patterns
    return cache.invalidate_namespace(namespace)

# Fonctions utilitaires pour les vues
def cache_view_data(view_name: str, data: Any, ttl: int = 600):
    """Met en cache les données d'une vue"""
    cache = get_global_cache()
    return cache.set(f"view_data_{view_name}", data, ttl, "views")

def get_cached_view_data(view_name: str) -> Optional[Any]:
    """Récupère les données mises en cache d'une vue"""
    cache = get_global_cache()
    return cache.get(f"view_data_{view_name}", "views")

def invalidate_view_cache(view_name: str):
    """Invalide le cache d'une vue spécifique"""
    cache = get_global_cache()
    return cache.invalidate(f"view_data_{view_name}", "views")

def preload_critical_data():
    """Précharge les données critiques au démarrage de l'application"""
    cache = get_global_cache()
    
    # Précharger les données des vues principales
    from src.core.database.optimized_queries import get_optimized_query_manager
    from src.core.paths import DATABASE_PATH
    
    manager = get_optimized_query_manager(DATABASE_PATH)
    
    print("🚀 Préchargement des données critiques...")
    
    # Précharger les élèves
    cache.preload_data(
        manager.get_all_eleves_optimized,
        "eleves_all",
        "preload"
    )
    
    # Précharger les classes
    cache.preload_data(
        manager.get_all_classes_optimized,
        "classes_all",
        "preload"
    )
    
    # Précharger les matières
    cache.preload_data(
        manager.get_all_matieres_optimized,
        "matieres_all",
        "preload"
    )
    
    print("✅ Préchargement terminé")
