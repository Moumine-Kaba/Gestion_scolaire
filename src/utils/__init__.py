# -*- coding: utf-8 -*-
"""
Module utils pour EduManager+
- Utilitaires de base de données
- Fonctions communes
- Helpers
"""

from .db_utils import (
    get_db_connection_wrapper as get_db_connection,
    get_connection,
    execute_query,
    execute_update,
    table_exists,
    get_table_columns,
    get_all_tables,
    backup_database,
    restore_database,
    get_all_eleves,
    get_all_professeurs,
    get_all_classes,
    get_all_matieres,
    get_all_notes,
    get_all_presences,
    get_all_bulletins,
    get_all_paiements,
    get_all_salles,
    get_all_utilisateurs,
    search_eleves,
    search_professeurs,
    search_classes,
    get_stats_eleves,
    get_stats_professeurs,
    get_stats_classes
)

__all__ = [
    'get_db_connection',
    'get_connection',
    'execute_query',
    'execute_update',
    'table_exists',
    'get_table_columns',
    'get_all_tables',
    'backup_database',
    'restore_database',
    'get_all_eleves',
    'get_all_professeurs',
    'get_all_classes',
    'get_all_matieres',
    'get_all_notes',
    'get_all_presences',
    'get_all_bulletins',
    'get_all_paiements',
    'get_all_salles',
    'get_all_utilisateurs',
    'search_eleves',
    'search_professeurs',
    'search_classes',
    'get_stats_eleves',
    'get_stats_professeurs',
    'get_stats_classes'
]