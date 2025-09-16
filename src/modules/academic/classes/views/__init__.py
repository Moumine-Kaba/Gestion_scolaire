#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues des Classes - Module Academic
==================================

Ce package contient toutes les vues liées à la gestion des classes.
"""

from .classes_view import ClassesManagerView
from .enseignements_view import EnseignementsView
from .emplois_view import EmploisView
from .presences_view import PresenceView

__all__ = [
    'ClassesManagerView',
    'EnseignementsView',
    'EmploisView',
    'PresenceView'
]
