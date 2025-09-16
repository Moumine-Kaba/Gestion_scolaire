#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues d'Annonces - Module Communication
======================================

Ce package contient toutes les vues liées aux annonces.
"""

from .actualites_view import ActualitesView
from .annonces_view import AnnoncesView
from .bibliotheque_view import BibliothequeView
from .documents_view import DocumentsView
from .calendriers_view import CalendriersView

__all__ = [
    'ActualitesView',
    'AnnoncesView',
    'BibliothequeView',
    'DocumentsView',
    'CalendriersView'
]
