# Guide des Permissions Avancées - EduManager+

## 🎯 Vue d'ensemble

Ce guide détaille le système de permissions avancées d'EduManager+ qui offre une gestion granulaire et sécurisée des accès utilisateur selon leurs rôles et responsabilités.

## 🔐 Hiérarchie des Rôles

### Niveaux d'Accès (du plus élevé au plus bas)

| Niveau | Rôle | Description | Accès |
|--------|------|-------------|-------|
| 15 | **Super Administrateur** | Accès complet système + gestion des administrateurs | Toutes les fonctionnalités + audit + sécurité |
| 10 | **Administrateur** | Accès complet à toutes les fonctionnalités | Toutes les fonctionnalités |
| 9 | **Directeur Général** | Gestion complète de l'établissement + finances | Tout sauf sauvegardes et logs système |
| 8 | **Directeur Pédagogique** | Gestion pédagogique complète | Pédagogie + administration limitée |
| 7 | **Proviseur** | Gestion pédagogique et administrative | Pédagogie + administration de base |
| 6 | **Censeur** | Gestion de la discipline et surveillance | Discipline + surveillance + lecture |
| 5 | **Surveillant Général** | Gestion des présences et discipline | Présences + discipline + lecture |
| 4 | **Professeur Principal** | Gestion de classe + notes + bulletins | Classe + notes + bulletins |
| 3 | **Professeur** | Gestion des cours et notes de sa matière | Cours + notes de sa matière |
| 3 | **Comptable Principal** | Gestion financière complète | Finances + lecture limitée |
| 2 | **Comptable** | Gestion financière limitée | Finances de base + lecture limitée |
| 2 | **Secrétaire Principal** | Gestion administrative complète | Administration + communication |
| 1 | **Secrétaire** | Gestion administrative limitée | Administration de base |
| 1 | **Élève** | Consultation des informations personnelles | Ses propres données uniquement |
| 1 | **Parent** | Consultation des informations de l'enfant | Données de ses enfants |
| 0 | **Visiteur** | Accès limité aux informations publiques | Informations publiques uniquement |

## 🚫 Restrictions par Rôle

### Super Administrateur & Administrateur
- **Aucune restriction** - Accès complet à toutes les fonctionnalités

### Directeur Général
- `utilisateurs`: Lecture seule
- `system_backup`: Aucun accès
- `audit_logs`: Aucun accès

### Directeur Pédagogique
- `paiements`: Lecture seule
- `utilisateurs`: Lecture seule
- `settings`: Aucun accès

### Proviseur
- `paiements`: Lecture seule
- `utilisateurs`: Lecture seule
- `settings`: Aucun accès

### Censeur
- `notes`: Lecture seule
- `paiements`: Aucun accès
- `utilisateurs`: Lecture seule

### Surveillant Général
- `notes`: Lecture seule
- `paiements`: Aucun accès
- `utilisateurs`: Lecture seule

### Professeur Principal
- `paiements`: Lecture seule
- `utilisateurs`: Lecture seule
- `settings`: Aucun accès

### Professeur
- `paiements`: Lecture seule
- `utilisateurs`: Lecture seule
- `settings`: Aucun accès

### Comptable Principal & Comptable
- `notes`: Lecture seule
- `enseignements`: Lecture seule
- `utilisateurs`: Lecture seule

### Secrétaire Principal & Secrétaire
- `notes`: Lecture seule
- `paiements`: Lecture seule
- `utilisateurs`: Lecture seule

### Élève
- `eleves`: Voir seulement ses propres infos
- `profs`: Voir seulement les profs
- `classes`: Voir seulement sa classe
- `paiements`: Voir seulement ses paiements
- `utilisateurs`: Aucun accès
- `settings`: Aucun accès

### Parent
- `eleves`: Voir seulement ses enfants
- `profs`: Voir seulement les profs
- `classes`: Voir seulement la classe de ses enfants
- `paiements`: Voir seulement les paiements de ses enfants
- `utilisateurs`: Aucun accès
- `settings`: Aucun accès

### Visiteur
- `eleves`: Aucun accès
- `profs`: Voir seulement les profs
- `classes`: Aucun accès
- `notes`: Aucun accès
- `paiements`: Aucun accès
- `utilisateurs`: Aucun accès
- `settings`: Aucun accès

## 🔍 Types de Permissions

### Niveaux de Permission
- **`none`**: Aucun accès
- **`read`**: Lecture seule (view, list, search)
- **`write`**: Lecture + écriture (view, list, search, create, update)
- **`full`**: Accès complet (view, list, search, create, update, delete, export, import)

### Actions Autorisées par Niveau

| Niveau | Actions Autorisées |
|--------|-------------------|
| `none` | Aucune |
| `read` | view, list, search |
| `write` | view, list, search, create, update |
| `full` | view, list, search, create, update, delete, export, import |

## 🛡️ Fonctionnalités de Sécurité

### 1. Logs d'Audit
- Enregistrement de toutes les tentatives d'accès
- Suivi des actions utilisateur
- Historique des connexions

### 2. Gestion des Sessions
- Tokens de session sécurisés
- Expiration automatique des sessions
- Suivi des connexions actives

### 3. Protection contre les Attaques
- Suivi des tentatives de connexion échouées
- Limitation des tentatives de connexion
- Blocage automatique des comptes suspects

### 4. Vérification des Données
- Contrôle d'accès aux données personnelles
- Restriction des vues selon le rôle
- Validation des permissions avant affichage

## 📋 Utilisation du Système

### Initialisation
```python
from models.permission_manager import PermissionManager

# Initialiser le gestionnaire
perm_manager = PermissionManager("database/edumanager.db")
```

### Vérification des Permissions
```python
# Vérifier l'accès à une vue
can_access = perm_manager.can_access_view(user_id, "eleves")

# Vérifier le niveau de permission
permission_level = perm_manager.get_user_permission_level(user_id, "notes")

# Vérifier une action spécifique
can_create = perm_manager.can_perform_action(user_id, "eleves", "create")
```

### Gestion des Rôles
```python
# Assigner un rôle à un utilisateur
success = perm_manager.assign_role_to_user(user_id, "Professeur")

# Récupérer le rôle d'un utilisateur
user_role = perm_manager.get_user_role(user_id)

# Récupérer les restrictions
restrictions = perm_manager.get_restricted_views(user_id)
```

### Logs et Audit
```python
# Enregistrer une tentative d'accès
perm_manager.log_access_attempt(user_id, "notes", "view", True)

# Récupérer les logs d'audit
logs = perm_manager.get_user_audit_logs(user_id, limit=100)
```

## 🔧 Configuration Avancée

### Ajout d'un Nouveau Rôle
1. Ajouter le rôle dans la base de données
2. Définir ses permissions dans `default_permissions`
3. Configurer ses restrictions dans `get_restricted_views`

### Modification des Permissions
1. Mettre à jour la table `role_permissions`
2. Adapter les restrictions dans le code
3. Tester les nouvelles permissions

### Personnalisation des Restrictions
1. Modifier la méthode `get_restricted_views`
2. Ajouter des règles métier spécifiques
3. Implémenter des vérifications personnalisées

## 🧪 Tests et Validation

### Exécuter les Tests
```bash
python test_permissions_advanced.py
```

### Tests Inclus
- ✅ Vérification des rôles créés
- ✅ Test des permissions
- ✅ Simulation d'utilisateurs
- ✅ Vérification des restrictions
- ✅ Test des actions autorisées
- ✅ Test des restrictions pour élèves
- ✅ Vérification de l'accès aux données
- ✅ Test des logs d'audit
- ✅ Test de la hiérarchie des rôles

## 🚨 Bonnes Pratiques

### 1. Sécurité
- Toujours vérifier les permissions avant d'afficher du contenu
- Utiliser les logs d'audit pour tracer les accès
- Implémenter une validation côté serveur

### 2. Performance
- Mettre en cache les permissions utilisateur
- Éviter les requêtes répétées à la base de données
- Optimiser les jointures pour les vérifications

### 3. Maintenance
- Documenter les changements de permissions
- Tester régulièrement le système de permissions
- Maintenir à jour les restrictions selon les besoins

## 🔄 Mise à Jour et Maintenance

### Mise à Jour des Permissions
1. Sauvegarder la base de données
2. Exécuter les scripts de mise à jour
3. Tester les nouvelles permissions
4. Former les utilisateurs si nécessaire

### Surveillance du Système
- Vérifier régulièrement les logs d'audit
- Surveiller les tentatives d'accès non autorisées
- Analyser les patterns d'utilisation

## 📞 Support et Assistance

Pour toute question ou problème avec le système de permissions :
1. Consulter ce guide
2. Exécuter les tests de validation
3. Vérifier les logs d'erreur
4. Contacter l'équipe de développement

---

**Version**: 2.0.0  
**Dernière mise à jour**: Décembre 2024  
**Auteur**: EduManager+ Team

