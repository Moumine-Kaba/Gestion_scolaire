# -*- coding: utf-8 -*-
"""
Fichier de compatibilité pour enseignements_view.py
Redirige vers la nouvelle vue unifiée des cours
"""

# Import de la nouvelle vue unifiée
from src.modules.academic.classes.views.cours_view import CoursManagerView

# Alias pour compatibilité
EnseignementsView = CoursManagerView

# Export pour le système de registre
__all__ = ['EnseignementsView']
