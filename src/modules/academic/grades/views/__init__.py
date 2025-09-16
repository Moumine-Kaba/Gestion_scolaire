#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues des Notes - Module Academic
================================

Ce package contient toutes les vues liées à la gestion des notes.
"""

from .notes_view import NotesView
from .bulletins_view import BulletinsView

__all__ = [
    'NotesView',
    'BulletinsView'
]
