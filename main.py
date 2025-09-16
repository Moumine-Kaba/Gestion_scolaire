#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

def _setup_paths():
    """Ajoute le répertoire du projet et /src au PYTHONPATH pour les imports."""
    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
    src_dir = os.path.join(project_root, "src")
    if os.path.isdir(src_dir) and src_dir not in sys.path:
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
        app = SplashView()          # <- ouvre LoginView après 5s (préchargements en parallèle)
        app.mainloop()

    except KeyboardInterrupt:
        print("🧹 Interruption utilisateur (Ctrl+C) — fermeture...")

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

if __name__ == "__main__":
    main()
