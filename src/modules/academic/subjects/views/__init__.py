#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues des Matières - Module Academic
===================================

Ce package contient toutes les vues liées à la gestion des matières.
"""

from .matieres_view import MatieresView
from .competences_view import CompetencesView
from .objectifs_view import ObjectifsView

__all__ = [
    'MatieresView',
    'CompetencesView',
    'ObjectifsView'
]
