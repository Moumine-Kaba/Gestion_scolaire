#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues d'Authentification - Module Auth (imports paresseux)
Évite les imports circulaires entre les vues.
"""

__all__ = [
    "LoginView",
    "RegisterView",
    "SplashView",
    "EnhancedLoginView",
    "UtilisateursView",
    "ViewManager",
]

def __getattr__(name):
    if name == "LoginView":
        from .login_view import LoginView
        return LoginView
    if name == "RegisterView":
        from .register_view import RegisterView
        return RegisterView
    if name == "SplashView":
        from .splash_view import SplashView
        return SplashView
    if name == "EnhancedLoginView":
        from .login_enhanced import EnhancedLoginView
        return EnhancedLoginView
    if name == "UtilisateursView":
        from .utilisateurs_view import UtilisateursView
        return UtilisateursView
    if name == "ViewManager":
        from .view_manager import ViewManager
        return ViewManager
    raise AttributeError(f"module 'src.modules.auth.views' has no attribute {name!r}")
