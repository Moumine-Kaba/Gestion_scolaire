#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vues du Personnel - Module Administrative
=========================================

Ce package contient toutes les vues liées à la gestion du personnel.
"""

from .personnel_view import PersonnelView
from .carrieres_view import CarrieresView

__all__ = [
    'PersonnelView',
    'CarrieresView'
]
