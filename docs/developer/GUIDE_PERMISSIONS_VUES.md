# Guide d'Utilisation du Système de Permissions des Vues

## 🎯 Objectif

Ce système permet de contrôler l'accès aux différentes vues de l'application selon le rôle de l'utilisateur connecté. Chaque type d'utilisateur (Directeur, Professeur, Élève, etc.) ne voit que les vues qui lui sont appropriées.

## 🏗️ Architecture

### 1. Configuration des Permissions (`models/view_permissions.py`)

Ce fichier définit quelles vues sont accessibles à chaque rôle :

```python
ROLE_VIEWS = {
    "Directeur": {
        "description": "Gestion des classes, élèves et professeurs",
        "views": ["dashboard", "eleves", "profs", "classes", "salles", ...]
    },
    "Professeur": {
        "description": "Gestion des notes, présences et bulletins",
        "views": ["dashboard", "eleves", "classes", "matieres", "notes", ...]
    },
    "Élève": {
        "description": "Consultation des notes et bulletins",
        "views": ["dashboard", "notes", "bulletins", "emplois", ...]
    }
}
```

### 2. Gestionnaire d'Accès (`models/view_access_manager.py`)

Ce gestionnaire :
- Vérifie les permissions d'un utilisateur
- Filtre les vues accessibles
- Gère les sections de navigation
- Permet des permissions personnalisées

### 3. Intégration Dashboard (`views/dashboard_view.py`)

Le dashboard utilise ces gestionnaires pour :
- Filtrer la sidebar selon le rôle
- Vérifier l'accès avant d'afficher une vue
- Afficher uniquement les sections appropriées

## 🚀 Installation et Configuration

### Étape 1: Initialisation des Rôles

Exécutez le script d'initialisation :

```bash
python init_roles_and_permissions.py
```

Ce script va :
- Créer les tables nécessaires
- Insérer les rôles par défaut
- Créer des utilisateurs de test
- Assigner les rôles appropriés

### Étape 2: Vérification

Testez le système avec le script de test :

```bash
python test_view_permissions.py
```

## 👥 Rôles et Permissions

### Super Administrateur
- **Accès complet** à tous les modules
- Peut gérer tous les utilisateurs et rôles
- Accès aux paramètres système

### Administrateur
- **Gestion complète** de l'établissement
- Accès à tous les modules sauf paramètres système
- Peut créer/modifier/supprimer des données

### Directeur
- **Gestion des classes, élèves et professeurs**
- Accès aux modules pédagogiques et administratifs
- Peut gérer les finances et les rapports

### Professeur
- **Gestion des notes, présences et bulletins**
- Accès aux classes et matières qu'il enseigne
- Peut consulter les emplois du temps

### Secrétaire
- **Gestion administrative et inscriptions**
- Accès aux modules administratifs
- Peut gérer les élèves et les paiements

### Élève
- **Consultation des notes et bulletins**
- Accès limité à ses propres informations
- Peut consulter les emplois du temps

### Parent
- **Consultation des informations de l'élève**
- Accès aux notes et bulletins de son enfant
- Peut consulter les emplois du temps

## 🔧 Personnalisation

### Ajouter un Nouveau Rôle

1. Modifiez `models/view_permissions.py`
2. Ajoutez le rôle dans `ROLE_VIEWS`
3. Définissez ses permissions
4. Ajoutez ses sections de navigation

```python
"Assistant": {
    "description": "Assistant administratif",
    "views": ["dashboard", "eleves", "classes", "presences"]
}
```

### Modifier les Permissions d'un Rôle

1. Localisez le rôle dans `ROLE_VIEWS`
2. Modifiez la liste des `views`
3. Ajustez les sections dans `ROLE_SECTIONS`

### Permissions Personnalisées

Le système permet d'accorder des permissions spécifiques à un utilisateur :

```python
from models.view_access_manager import ViewAccessManager

view_manager = ViewAccessManager("database/edumanager.db")

# Accorder l'accès à une vue spécifique
view_manager.grant_view_access(user_id=5, view_name="utilisateurs", access_level="read")

# Révoquer l'accès
view_manager.revoke_view_access(user_id=5, view_name="utilisateurs")
```

## 🧪 Tests

### Comptes de Test Disponibles

Après l'initialisation, vous pouvez tester avec :

- **admin / admin123** → Super Administrateur
- **directeur / directeur123** → Directeur
- **professeur / prof123** → Professeur
- **secretaire / sec123** → Secrétaire
- **eleve / eleve123** → Élève

### Vérification des Restrictions

1. Connectez-vous avec un compte Élève
2. Vérifiez que seules les vues appropriées sont visibles
3. Testez l'accès aux vues restreintes
4. Vérifiez que les messages d'erreur s'affichent correctement

## 🐛 Dépannage

### Problème: Toutes les vues sont visibles

**Cause possible:** L'utilisateur n'a pas de rôle assigné
**Solution:** Vérifiez la table `user_roles` et assignez un rôle

### Problème: Erreur lors de la vérification des permissions

**Cause possible:** Tables manquantes ou corrompues
**Solution:** Relancez `init_roles_and_permissions.py`

### Problème: Certaines vues ne s'affichent pas

**Cause possible:** Vue non définie dans `ROLE_VIEWS`
**Solution:** Ajoutez la vue au rôle approprié

## 📝 Logs et Debug

Le système génère des logs détaillés :

```
✅ Gestionnaire d'accès aux vues initialisé
✅ Rôle 'Directeur' créé
✅ Accès à la vue 'utilisateurs' accordé à l'utilisateur 5
⚠️ Erreur vérification accès vue 'settings' pour utilisateur 3: ...
```

## 🔒 Sécurité

- Les permissions sont vérifiées côté serveur
- Les vues sont filtrées avant affichage
- Double vérification : rôle + permissions personnalisées
- Logs de toutes les tentatives d'accès

## 📚 Extensions Futures

Le système peut être étendu pour :

- **Permissions granulaires** (lecture/écriture/suppression)
- **Permissions temporelles** (accès limité dans le temps)
- **Permissions conditionnelles** (selon l'heure, la localisation)
- **Audit trail** (historique des accès)
- **Interface d'administration** des permissions

## 🆘 Support

En cas de problème :

1. Vérifiez les logs de l'application
2. Testez avec le script `test_view_permissions.py`
3. Vérifiez la structure de la base de données
4. Consultez ce guide et la documentation du code

