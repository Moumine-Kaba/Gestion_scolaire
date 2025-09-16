#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module core - Composants centraux de l'application
"""

from .database_config import (
    get_db_path,
    connect_db,
    get_stats_count,
    get_moyennes_par_matiere,
    get_recent_events,
    get_user_info
)

from .view_manager import (
    ViewManager,
    PlaceholderView,
    view_manager
)

from .permissions import (
    PermissionManager,
    permission_manager
)

from .icon_manager import (
    IconManager,
    icon_manager
)

__all__ = [
    # Database
    'get_db_path',
    'connect_db', 
    'get_stats_count',
    'get_moyennes_par_matiere',
    'get_recent_events',
    'get_user_info',
    
    # Views
    'ViewManager',
    'PlaceholderView',
    'view_manager',
    
    # Permissions
    'PermissionManager',
    'permission_manager',
    
    # Icons
    'IconManager',
    'icon_manager'
]

