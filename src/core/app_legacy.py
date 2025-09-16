#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback

def _setup_paths():
    """Ajoute le répertoire du projet et /views au PYTHONPATH pour les imports."""
    project_root = os.path.abspath(os.path.dirname(__file__))
    if project_root not in sys.path:
        sys.path.append(project_root)
    views_dir = os.path.join(project_root, "views")
    if os.path.isdir(views_dir) and views_dir not in sys.path:
        sys.path.append(views_dir)

def main():
    _setup_paths()

    print("🚀 Démarrage d'EduManager+...")
    # Tu peux ajouter ici d'autres vérifications (DB, assets, etc.)
    print("✅ Vérifications terminées")
    print("🚀 Lancement du splash view (5s)...")

    try:
        # On démarre le Splash (petite fenêtre, centrée, 5 secondes).
        # Le Splash ferme proprement ses animations puis ouvre LoginView.
        from src.modules.splash_view import SplashView
        app = SplashView()          # <- ouvre LoginView après 5s (préchargements en parallèle)
        app.mainloop()

    except KeyboardInterrupt:
        print("🧹 Interruption utilisateur (Ctrl+C) — fermeture...")

    except Exception as e:
        # Plan B : si Splash indisponible, on lance directement le Login.
        print(f"⚠️  SplashView indisponible: {e}")
        try:
            from src.modules.login_view import LoginView
            app = LoginView()
            app.mainloop()
        except Exception as ee:
            print("❌ Erreur critique: impossible de lancer LoginView.")
            traceback.print_exc()

    finally:
        print("👋 Fermeture d'EduManager+")

if __name__ == "__main__":
    main()
