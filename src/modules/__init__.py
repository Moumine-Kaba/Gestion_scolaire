#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modules Package - Modules Métier
================================

Ce package contient tous les modules métier de l'application.
"""

from .auth import *
from .academic import *
from .administrative import *
from .communication import *

__all__ = [
    'auth',
    'academic', 
    'administrative',
    'communication'
]

