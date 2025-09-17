#!/usr/bin/env python3
"""
SYSTÈME DE CACHE INTELLIGENT POUR CONTRÔLEURS
=============================================

Ce module fournit un système de cache intelligent qui s'intègre avec
les contrôleurs existants pour optimiser les performances.

Fonctionnalités :
- Cache multi-niveaux (mémoire + disque)
- Invalidation intelligente
- Préchargement automatique
- Statistiques de performance
- Compatible avec l'architecture existante
"""

import sqlite3
import threading
import time
import json
import os
import pickle
from typing import Dict, List, Any, Optional, Callable
from functools import wraps
from datetime import datetime, timedelta
import hashlib

class IntelligentCache:
    """
    Système de cache intelligent pour les contrôleurs
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
            
        self.memory_cache = {}
        self.cache_timestamps = {}
        self.cache_stats = {}
        self.cache_duration = 300  # 5 minutes par défaut
        self.max_memory_size = 100  # Nombre max d'éléments en mémoire
        self.disk_cache_dir = "cache"
        self.stats = {
            'hits': 0,
            'misses': 0,
            'disk_hits': 0,
            'memory_hits': 0,
            'evictions': 0,
            'total_time_saved': 0
        }
        
        # Créer le dossier de cache disque
        os.makedirs(self.disk_cache_dir, exist_ok=True)
        
        self._initialized = True
        print("✅ IntelligentCache initialisé")
    
    def _generate_key(self, func_name: str, *args, **kwargs) -> str:
        """Génère une clé de cache unique"""
        key_data = f"{func_name}:{str(args)}:{str(sorted(kwargs.items()))}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_memory_cache_valid(self, key: str) -> bool:
        """Vérifie si le cache mémoire est valide"""
        if key not in self.memory_cache:
            return False
        
        cache_age = time.time() - self.cache_timestamps[key]
        return cache_age < self.cache_duration
    
    def _is_disk_cache_valid(self, key: str) -> bool:
        """Vérifie si le cache disque est valide"""
        cache_file = os.path.join(self.disk_cache_dir, f"{key}.cache")
        
        if not os.path.exists(cache_file):
            return False
        
        # Vérifier l'âge du fichier
        file_age = time.time() - os.path.getmtime(cache_file)
        return file_age < self.cache_duration
    
    def _load_from_disk(self, key: str) -> Optional[Any]:
        """Charge les données depuis le cache disque"""
        cache_file = os.path.join(self.disk_cache_dir, f"{key}.cache")
        
        try:
            with open(cache_file, 'rb') as f:
                data = pickle.load(f)
                self.stats['disk_hits'] += 1
                return data
        except Exception as e:
            print(f"⚠️ Erreur chargement cache disque {key}: {e}")
            return None
    
    def _save_to_disk(self, key: str, data: Any):
        """Sauvegarde les données sur le cache disque"""
        cache_file = os.path.join(self.disk_cache_dir, f"{key}.cache")
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde cache disque {key}: {e}")
    
    def _evict_oldest(self):
        """Évince l'élément le plus ancien du cache mémoire"""
        if not self.memory_cache:
            return
        
        oldest_key = min(self.cache_timestamps.keys(), 
                        key=lambda k: self.cache_timestamps[k])
        
        # Sauvegarder sur disque avant d'évincer
        if oldest_key in self.memory_cache:
            self._save_to_disk(oldest_key, self.memory_cache[oldest_key])
        
        del self.memory_cache[oldest_key]
        del self.cache_timestamps[oldest_key]
        self.stats['evictions'] += 1
    
    def get(self, func_name: str, *args, **kwargs) -> Optional[Any]:
        """Récupère les données depuis le cache"""
        key = self._generate_key(func_name, *args, **kwargs)
        
        # Vérifier le cache mémoire
        if self._is_memory_cache_valid(key):
            self.stats['hits'] += 1
            self.stats['memory_hits'] += 1
            return self.memory_cache[key]
        
        # Vérifier le cache disque
        if self._is_disk_cache_valid(key):
            data = self._load_from_disk(key)
            if data is not None:
                # Remettre en mémoire pour accès rapide
                self._put_in_memory(key, data)
                self.stats['hits'] += 1
                return data
        
        self.stats['misses'] += 1
        return None
    
    def put(self, func_name: str, data: Any, *args, **kwargs):
        """Met les données en cache"""
        key = self._generate_key(func_name, *args, **kwargs)
        
        # Mettre en mémoire
        self._put_in_memory(key, data)
        
        # Sauvegarder sur disque
        self._save_to_disk(key, data)
    
    def _put_in_memory(self, key: str, data: Any):
        """Met les données en cache mémoire"""
        # Évincer si nécessaire
        if len(self.memory_cache) >= self.max_memory_size:
            self._evict_oldest()
        
        self.memory_cache[key] = data
        self.cache_timestamps[key] = time.time()
    
    def invalidate(self, pattern: str = None):
        """Invalide le cache (tout ou par pattern)"""
        if pattern is None:
            # Vider le cache mémoire
            self.memory_cache.clear()
            self.cache_timestamps.clear()
            
            # Vider le cache disque
            for file in os.listdir(self.disk_cache_dir):
                if file.endswith('.cache'):
                    os.remove(os.path.join(self.disk_cache_dir, file))
            
            print("🗑️ Cache complètement vidé")
        else:
            # Vider par pattern
            keys_to_remove = []
            for key in self.memory_cache.keys():
                if pattern in key:
                    keys_to_remove.append(key)
            
            for key in keys_to_remove:
                del self.memory_cache[key]
                del self.cache_timestamps[key]
            
            # Vider les fichiers disque correspondants
            for file in os.listdir(self.disk_cache_dir):
                if file.endswith('.cache') and pattern in file:
                    os.remove(os.path.join(self.disk_cache_dir, file))
            
            print(f"🗑️ Cache vidé pour pattern: {pattern}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Retourne les statistiques du cache"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'hit_rate': f"{hit_rate:.1f}%",
            'memory_hits': self.stats['memory_hits'],
            'disk_hits': self.stats['disk_hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'memory_size': len(self.memory_cache),
            'time_saved': f"{self.stats['total_time_saved']:.2f}s"
        }

def cached(ttl: int = 300):
    """
    Décorateur pour mettre en cache les fonctions des contrôleurs
    
    Args:
        ttl: Time To Live en secondes (défaut: 5 minutes)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = IntelligentCache()
            
            # Vérifier le cache
            cached_result = cache.get(func.__name__, *args, **kwargs)
            if cached_result is not None:
                return cached_result
            
            # Exécuter la fonction
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Mettre en cache
            cache.put(func.__name__, result, *args, **kwargs)
            
            # Mettre à jour les statistiques
            cache.stats['total_time_saved'] += execution_time
            
            return result
        
        return wrapper
    return decorator

def invalidate_cache(pattern: str = None):
    """Invalide le cache intelligent"""
    cache = IntelligentCache()
    cache.invalidate(pattern)

def get_cache_stats() -> Dict[str, Any]:
    """Retourne les statistiques du cache intelligent"""
    cache = IntelligentCache()
    return cache.get_stats()

# ===== INTÉGRATION AVEC LES CONTRÔLEURS EXISTANTS =====

class ControllerCacheManager:
    """
    Gestionnaire de cache spécialisé pour les contrôleurs
    """
    
    def __init__(self):
        self.cache = IntelligentCache()
        self.controller_stats = {}
    
    def get_eleves_all(self) -> List[Dict[str, Any]]:
        """Cache pour get_all_eleves"""
        return self.cache.get('get_all_eleves') or []
    
    def put_eleves_all(self, data: List[Dict[str, Any]]):
        """Met en cache get_all_eleves"""
        self.cache.put('get_all_eleves', data)
    
    def get_classes_all(self) -> List[Dict[str, Any]]:
        """Cache pour get_all_classes"""
        return self.cache.get('get_all_classes') or []
    
    def put_classes_all(self, data: List[Dict[str, Any]]):
        """Met en cache get_all_classes"""
        self.cache.put('get_all_classes', data)
    
    def get_matieres_all(self) -> List[Dict[str, Any]]:
        """Cache pour get_all_matieres"""
        return self.cache.get('get_all_matieres') or []
    
    def put_matieres_all(self, data: List[Dict[str, Any]]):
        """Met en cache get_all_matieres"""
        self.cache.put('get_all_matieres', data)
    
    def get_notes_by_eleve(self, eleve_id: int) -> List[Dict[str, Any]]:
        """Cache pour get_notes_by_eleve"""
        return self.cache.get('get_notes_by_eleve', eleve_id) or []
    
    def put_notes_by_eleve(self, eleve_id: int, data: List[Dict[str, Any]]):
        """Met en cache get_notes_by_eleve"""
        self.cache.put('get_notes_by_eleve', data, eleve_id)
    
    def invalidate_eleve_cache(self, eleve_id: int = None):
        """Invalide le cache des élèves"""
        if eleve_id:
            self.cache.invalidate(f'eleve_{eleve_id}')
        else:
            self.cache.invalidate('eleve')
    
    def invalidate_classe_cache(self, classe_id: int = None):
        """Invalide le cache des classes"""
        if classe_id:
            self.cache.invalidate(f'classe_{classe_id}')
        else:
            self.cache.invalidate('classe')
    
    def invalidate_matiere_cache(self, matiere_id: int = None):
        """Invalide le cache des matières"""
        if matiere_id:
            self.cache.invalidate(f'matiere_{matiere_id}')
        else:
            self.cache.invalidate('matiere')
    
    def invalidate_note_cache(self, eleve_id: int = None):
        """Invalide le cache des notes"""
        if eleve_id:
            self.cache.invalidate(f'note_eleve_{eleve_id}')
        else:
            self.cache.invalidate('note')

# Instance globale
controller_cache = ControllerCacheManager()

# ===== FONCTIONS D'UTILITAIRE =====

def preload_controller_cache():
    """Précharge le cache des contrôleurs"""
    print("🚀 Préchargement du cache des contrôleurs...")
    
    try:
        # Importer les contrôleurs
        from src.modules.academic.students.controllers.eleve_controller import get_all_eleves
        from src.modules.academic.classes.controllers.classe_controller import get_all_classes
        from src.modules.academic.subjects.controllers.matiere_controller import get_all_matieres
        
        # Précharger les données
        eleves = get_all_eleves()
        controller_cache.put_eleves_all(eleves)
        print(f"✅ {len(eleves)} élèves préchargés")
        
        classes = get_all_classes()
        controller_cache.put_classes_all(classes)
        print(f"✅ {len(classes)} classes préchargées")
        
        matieres = get_all_matieres()
        controller_cache.put_matieres_all(matieres)
        print(f"✅ {len(matieres)} matières préchargées")
        
        print("✅ Préchargement du cache des contrôleurs terminé")
        
    except Exception as e:
        print(f"⚠️ Erreur préchargement cache contrôleurs: {e}")

def optimize_controller_performance():
    """Optimise les performances des contrôleurs"""
    print("⚡ Optimisation des performances des contrôleurs...")
    
    # Précharger le cache
    preload_controller_cache()
    
    # Afficher les statistiques
    stats = get_cache_stats()
    print(f"📊 Statistiques cache: {stats}")
    
    print("✅ Optimisation terminée")

if __name__ == "__main__":
    # Test du système de cache intelligent
    print("🧪 Test du système de cache intelligent...")
    
    # Optimiser les performances
    optimize_controller_performance()
    
    # Afficher les statistiques finales
    stats = get_cache_stats()
    print(f"📊 Statistiques finales: {stats}")
    
    print("✅ Test terminé")
