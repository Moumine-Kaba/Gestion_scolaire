#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exceptions Personnalisées pour EduManager+
=========================================

Définition des exceptions spécifiques à l'application.
"""

from typing import Optional, Any, Dict


class EduManagerException(Exception):
    """Exception de base pour toutes les exceptions de l'application"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self):
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class AuthenticationError(EduManagerException):
    """Erreur d'authentification"""
    
    def __init__(self, message: str = "Erreur d'authentification", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class AuthorizationError(EduManagerException):
    """Erreur d'autorisation (permissions insuffisantes)"""
    
    def __init__(self, message: str = "Permissions insuffisantes", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTHZ_ERROR", details)


class ValidationError(EduManagerException):
    """Erreur de validation des données"""
    
    def __init__(self, message: str = "Données invalides", field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        if field:
            message = f"Champ '{field}': {message}"
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class DatabaseError(EduManagerException):
    """Erreur de base de données"""
    
    def __init__(self, message: str = "Erreur de base de données", operation: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        if operation:
            message = f"Opération '{operation}': {message}"
        super().__init__(message, "DB_ERROR", details)
        self.operation = operation


class NotFoundError(EduManagerException):
    """Ressource non trouvée"""
    
    def __init__(self, resource_type: str, resource_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        message = f"{resource_type} non trouvé"
        if resource_id:
            message += f" (ID: {resource_id})"
        super().__init__(message, "NOT_FOUND", details)
        self.resource_type = resource_type
        self.resource_id = resource_id


class DuplicateError(EduManagerException):
    """Ressource en double"""
    
    def __init__(self, resource_type: str, field: str, value: str, details: Optional[Dict[str, Any]] = None):
        message = f"{resource_type} avec {field}='{value}' existe déjà"
        super().__init__(message, "DUPLICATE", details)
        self.resource_type = resource_type
        self.field = field
        self.value = value


class ConfigurationError(EduManagerException):
    """Erreur de configuration"""
    
    def __init__(self, message: str = "Erreur de configuration", config_key: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        if config_key:
            message = f"Configuration '{config_key}': {message}"
        super().__init__(message, "CONFIG_ERROR", details)
        self.config_key = config_key


class ServiceError(EduManagerException):
    """Erreur de service"""
    
    def __init__(self, service_name: str, message: str = "Erreur de service", details: Optional[Dict[str, Any]] = None):
        message = f"Service '{service_name}': {message}"
        super().__init__(message, "SERVICE_ERROR", details)
        self.service_name = service_name


class UIError(EduManagerException):
    """Erreur d'interface utilisateur"""
    
    def __init__(self, component: str, message: str = "Erreur d'interface", details: Optional[Dict[str, Any]] = None):
        message = f"Interface '{component}': {message}"
        super().__init__(message, "UI_ERROR", details)
        self.component = component


class NetworkError(EduManagerException):
    """Erreur réseau"""
    
    def __init__(self, message: str = "Erreur réseau", url: Optional[str] = None, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        if url:
            message = f"URL '{url}': {message}"
        if status_code:
            message += f" (Code: {status_code})"
        super().__init__(message, "NETWORK_ERROR", details)
        self.url = url
        self.status_code = status_code


class TimeoutError(EduManagerException):
    """Erreur de timeout"""
    
    def __init__(self, operation: str, timeout_seconds: int, details: Optional[Dict[str, Any]] = None):
        message = f"Opération '{operation}' a expiré après {timeout_seconds} secondes"
        super().__init__(message, "TIMEOUT", details)
        self.operation = operation
        self.timeout_seconds = timeout_seconds


class ResourceError(EduManagerException):
    """Erreur de ressource (fichier, image, etc.)"""
    
    def __init__(self, resource_path: str, message: str = "Erreur de ressource", details: Optional[Dict[str, Any]] = None):
        message = f"Ressource '{resource_path}': {message}"
        super().__init__(message, "RESOURCE_ERROR", details)
        self.resource_path = resource_path


# Fonction utilitaire pour créer des exceptions avec contexte
def create_exception(exception_class: type, message: str, **kwargs) -> EduManagerException:
    """Crée une exception avec un message formaté et des détails"""
    return exception_class(message, **kwargs)


# Fonction pour logger les exceptions
def log_exception(exception: EduManagerException, logger=None):
    """Log une exception avec ses détails"""
    if logger:
        logger.error(f"Exception: {exception}")
        if exception.details:
            logger.error(f"Détails: {exception.details}")
        if exception.error_code:
            logger.error(f"Code d'erreur: {exception.error_code}")
    else:
        print(f"Exception: {exception}")
        if exception.details:
            print(f"Détails: {exception.details}")
        if exception.error_code:
            print(f"Code d'erreur: {exception.error_code}")

