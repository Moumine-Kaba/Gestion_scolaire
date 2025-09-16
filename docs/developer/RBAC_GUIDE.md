# 🔐 Système RBAC (Role-Based Access Control) - EduManager+

## Vue d'ensemble

Le système RBAC d'EduManager+ permet de contrôler précisément l'accès aux vues et fonctionnalités selon le rôle de l'utilisateur. Il garantit que seules les personnes autorisées peuvent accéder aux différentes sections de l'application.

## 🏗️ Architecture

### Composants principaux

1. **RBACSystem** (`rbac_system.py`) - Système de gestion des rôles et permissions
2. **RBACViewManager** (`rbac_view_manager.py`) - Gestionnaire de vues avec contrôle d'accès
3. **RBACConfig** (`rbac_config.py`) - Configuration centralisée
4. **Décorateurs RBAC** (`rbac_decorators.py`) - Protection des méthodes et vues

### Rôles par défaut

| Rôle | Description | Permissions principales |
|------|-------------|------------------------|
| **Directeur** | Accès complet | Toutes les vues en ADMIN |
| **Comptable** | Gestion financière | Paiements (ADMIN) + lecture données scolaires |
| **Secrétaire** | Gestion administrative | Élèves, Classes, Présences (ADMIN) - pas Paiements |
| **Surveillant** | Surveillance | Présences, Emplois (ADMIN) + lecture Élèves |

## 🚀 Installation et Configuration

### 1. Initialisation du système

```bash
# Exécuter le script d'initialisation
python init_rbac_system.py
```

### 2. Test du système

```bash
# Vérifier le bon fonctionnement
python test_rbac_system.py
```

### 3. Mode développement

Pour désactiver temporairement les restrictions RBAC :

```python
# Dans rbac_config.py
RBAC_CONFIG = {
    "DEV_MODE": True,  # Désactive toutes les restrictions
    # ...
}
```

## 📋 Utilisation

### Intégration dans une vue

```python
from src.modules.auth.models.rbac_view_manager import RBACViewManager
from src.modules.auth.models.rbac_decorators import RBACProtectedView, require_permission

class MaVue(RBACProtectedView):
    def __init__(self, master, rbac_manager, user_id):
        super().__init__(rbac_manager, user_id)
        # Initialisation de la vue...
    
    @require_permission("eleves", PermissionLevel.WRITE)
    def ajouter_eleve(self):
        # Cette méthode nécessite des permissions WRITE sur "eleves"
        pass
    
    @require_permission("eleves", PermissionLevel.ADMIN)
    def supprimer_eleve(self):
        # Cette méthode nécessite des permissions ADMIN sur "eleves"
        pass
```

### Gestionnaire de vues avec sidebar

```python
# Créer le gestionnaire RBAC
rbac_manager = RBACViewManager(db_path, dev_mode=False)

# Définir l'utilisateur actuel
rbac_manager.set_current_user(user_id)

# Créer la sidebar avec navigation filtrée
sidebar = RBACSidebar(master, rbac_manager)

# Enregistrer les callbacks des vues
rbac_manager.register_view_callback("eleves", self.open_eleves_view)
rbac_manager.register_view_callback("paiements", self.open_paiements_view)

# Définir le callback d'accès refusé
rbac_manager.set_access_denied_callback(self.show_access_denied)
```

### Vérification des permissions

```python
# Vérifier l'accès à une vue
if rbac_manager.can_access_view("paiements"):
    # Ouvrir la vue des paiements
    pass

# Récupérer le niveau de permission
permission_level = rbac_manager.get_view_permission_level("eleves")
if permission_level == PermissionLevel.ADMIN:
    # Afficher les boutons d'administration
    pass

# Obtenir la navigation filtrée
filtered_nav = rbac_manager.get_filtered_navigation()
```

## 🔧 Configuration

### Ajouter une nouvelle vue

1. **Définir dans la configuration** (`rbac_config.py`) :

```python
VIEW_PERMISSIONS = {
    "nouvelle_vue": {
        "title": "Nouvelle Vue",
        "description": "Description de la nouvelle vue",
        "section": "ADMINISTRATION",
        "icon": "icon_name",
        "default_permission": "read"
    }
}
```

2. **Ajouter les permissions par rôle** :

```python
DEFAULT_ROLES = {
    "Directeur": {
        "permissions": {
            "nouvelle_vue": "admin",
            # ...
        }
    },
    "Comptable": {
        "permissions": {
            "nouvelle_vue": "none",  # Pas d'accès
            # ...
        }
    }
}
```

### Créer un nouveau rôle

```python
from src.modules.auth.models.rbac_system import RBACSystem, PermissionLevel

rbac = RBACSystem(db_path)

# Définir les permissions
permissions = {
    "dashboard": PermissionLevel.READ,
    "eleves": PermissionLevel.WRITE,
    "paiements": PermissionLevel.NONE,
    # ...
}

# Créer le rôle
rbac.create_role("Assistant", "Assistant pédagogique", permissions)

# Attribuer à un utilisateur
rbac.assign_role_to_user(user_id, "Assistant")
```

## 🛡️ Sécurité

### Contrôles automatiques

- **Vérification des permissions** à chaque accès à une vue
- **Filtrage de la navigation** selon le rôle de l'utilisateur
- **Logs d'accès** pour audit et sécurité
- **Protection contre l'accès direct** aux vues non autorisées

### Bonnes pratiques

1. **Toujours vérifier les permissions** avant d'exécuter une action
2. **Utiliser les décorateurs** pour protéger les méthodes sensibles
3. **Logger les tentatives d'accès** non autorisées
4. **Tester régulièrement** le système avec différents rôles

## 📊 Monitoring

### Logs d'accès

Le système enregistre automatiquement :
- Tentatives d'accès (réussies/échouées)
- Changements de rôles
- Création/modification de permissions

### Statistiques

```python
# Nombre de vues accessibles
views_count = rbac_manager.get_accessible_views_count()

# Informations du rôle
role_info = rbac_manager.get_user_role_info()
print(f"Rôle: {role_info['name']}")
print(f"Vues accessibles: {len(role_info['accessible_views'])}")
```

## 🔄 Maintenance

### Mise à jour des permissions

```python
# Modifier les permissions d'un rôle
new_permissions = {
    "eleves": PermissionLevel.ADMIN,
    "paiements": PermissionLevel.READ,
    # ...
}
rbac.update_role_permissions("Comptable", new_permissions)
```

### Sauvegarde et restauration

```python
# Exporter toutes les permissions
roles = rbac.get_all_roles()
# Sauvegarder dans un fichier JSON...

# Restaurer depuis un fichier
# Importer et recréer les rôles...
```

## 🧪 Tests

### Tests automatisés

Le script `test_rbac_system.py` vérifie :
- Création des rôles par défaut
- Attribution des permissions
- Filtrage de la navigation
- Contrôle d'accès
- Mode développement
- Gestion des rôles

### Tests manuels

1. Se connecter avec chaque rôle
2. Vérifier que seules les vues autorisées apparaissent
3. Tenter d'accéder directement aux vues non autorisées
4. Vérifier les messages d'accès refusé

## 🚨 Dépannage

### Problèmes courants

1. **Utilisateur sans rôle** → Attribuer un rôle avec `assign_role_to_user()`
2. **Vues manquantes** → Vérifier les permissions dans `DEFAULT_ROLES`
3. **Accès refusé** → Vérifier le niveau de permission requis
4. **Mode dev activé** → Désactiver `DEV_MODE` en production

### Commandes de diagnostic

```bash
# Vérifier l'état du système RBAC
python test_rbac_system.py

# Lister tous les rôles
python -c "
from src.modules.auth.models.rbac_system import RBACSystem
rbac = RBACSystem('database/edumanager.db')
for role in rbac.get_all_roles():
    print(f'{role.name}: {role.description}')
"
```

## 📈 Évolutions futures

- **Permissions granulaires** par action (créer, modifier, supprimer)
- **Rôles hiérarchiques** avec héritage de permissions
- **Permissions temporaires** avec expiration
- **Interface d'administration** pour la gestion des rôles
- **Synchronisation** avec un système d'authentification externe

---

**Note** : Ce système RBAC est conçu pour être robuste et sécurisé. Toute modification des permissions doit être effectuée avec précaution et testée en environnement de développement avant d'être appliquée en production.
