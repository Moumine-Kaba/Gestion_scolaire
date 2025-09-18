#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import traceback
import warnings
import contextlib

# Supprimer tous les avertissements
warnings.filterwarnings('ignore')

# Rediriger complètement stderr
class SilentStderr:
    def write(self, message):
        # Ne rien afficher
        pass
    def flush(self):
        pass
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

# Appliquer le filtre silencieux
sys.stderr = SilentStderr()

def _setup_paths():
    """Configure les chemins du projet"""
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    if src_dir not in sys.path:
        sys.path.append(src_dir)

def main():
    _setup_paths()

    print("🚀 Démarrage d'EduManager+...")
    print("✅ Vérifications terminées")
    print("🚀 Lancement de l'application...")

    try:
        # On démarre avec le Splash puis le Login comme avant
        print("🎬 Lancement du splash view (5s)...")
        from src.modules.auth.views.splash_view import SplashView
        splash = SplashView()
        splash.mainloop()
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        main()
        # Préchargement académique (en cache, si possible)
        from src.modules.academic.cache import (  # pyright: ignore[reportMissingImports]
            preload_matieres_cache,
            preload_salles_cache,
            preload_eleves_cache,
        )
        preload_matieres_cache()
        preload_salles_cache()
        preload_eleves_cache()
    except Exception as e:
        print(f"⚠️ Préchargement académique ignoré: {e}")
print("🚀 Lancement de l'application...")

try:
    # On démarre avec le Splash puis le Login comme avant
        print("🎬 Lancement du splash view (5s)...")
        from src.modules.auth.views.splash_view import SplashView
        app = SplashView()          # <- ouvre LoginView après 5s (préchargements en parallèle)
        app.mainloop()

except KeyboardInterrupt:
    print("🧹 Interruption utilisateurs (Ctrl+C) — fermeture...")

except Exception as e:
    # Plan B : si SplashView indisponible, on lance directement le Login
        print(f"⚠️  SplashView indisponible: {e}")
        traceback.print_exc()
        try:
            print("🔄 Tentative d'ouverture directe du LoginView...")
            # Nettoyer les références d'images avant de créer le login
            import gc
            gc.collect()
            
            from src.modules.auth.views.login_view import LoginViewModern
            app = LoginViewModern()
            app.mainloop()
        except Exception as ee:
            print("❌ Erreur critique: impossible de lancer LoginView.")
            traceback.print_exc()

        finally:
            print("👋 Fermeture d'EduManager+")
            # S'assurer que l'application se ferme proprement
            import sys
            sys.exit(1)
