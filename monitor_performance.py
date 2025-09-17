#!/usr/bin/env python3
"""
MONITEUR DE PERFORMANCE EDUMANAGER+
===================================

Ce script surveille les performances du système d'optimisation
et génère des rapports détaillés.
"""

import time
import json
from datetime import datetime
from src.core.optimization.edu_manager_optimizer import get_performance_report

def monitor_performance():
    """Surveille les performances en temps réel"""
    print("📊 Surveillance des performances...")
    
    while True:
        try:
            # Récupérer les statistiques
            stats = get_performance_report()
            
            # Afficher les statistiques
            print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')}")
            print(f"🚀 Temps de démarrage: {stats.get('startup_time', 0):.3f}s")
            print(f"📋 Cache hits: {stats.get('cache_hits', 0)}")
            print(f"❌ Cache misses: {stats.get('cache_misses', 0)}")
            
            if 'stored_procedures' in stats:
                sp_stats = stats['stored_procedures']
                print(f"⚡ Procédures - Hit rate: {sp_stats.get('hit_rate', '0%')}")
            
            if 'intelligent_cache' in stats:
                cache_stats = stats['intelligent_cache']
                print(f"💾 Cache - Hit rate: {cache_stats.get('hit_rate', '0%')}")
            
            # Attendre 30 secondes
            time.sleep(30)
            
        except KeyboardInterrupt:
            print("\n⏹️ Surveillance arrêtée")
            break
        except Exception as e:
            print(f"⚠️ Erreur surveillance: {e}")
            time.sleep(5)

if __name__ == "__main__":
    monitor_performance()
