# 🎉 EduManager+ avec RBAC - Système Complet et Fonctionnel

## 🚀 Démarrage Rapide

Pour lancer l'application avec le système RBAC intégré :

```bash
python start_rbac_app.py
```

## 👥 Utilisateurs Disponibles

Le système est pré-configuré avec 5 utilisateurs par défaut :

| Utilisateur | Mot de passe | Rôle | Permissions |
|-------------|--------------|------|-------------|
| **directeur** | directeur123 | Directeur | Toutes les vues (ADMIN) |
| **comptable** | comptable123 | Comptable | Paiements (ADMIN) + lecture données scolaires |
| **secretaire** | secretaire123 | Secrétaire | Élèves, Classes, Présences (ADMIN) - pas Paiements |
| **surveillant** | surveillant123 | Surveillant | Présences, Emplois (ADMIN) + lecture Élèves |
| **admin** | admin123 | Directeur | Toutes les vues (ADMIN) |

## 🔐 Fonctionnalités RBAC

### ✅ Contrôle d'Accès
- **Sidebar filtrée** : Seules les vues autorisées apparaissent selon le rôle
- **Accès direct bloqué** : Tentatives d'accès non autorisées refusées
- **Messages d'erreur** : Dialogues personnalisés pour accès refusé
- **Logs d'accès** : Enregistrement de toutes les tentatives d'accès

### ✅ Permissions par Rôle

#### Directeur
- **Accès complet** à toutes les vues (19 vues)
- Permissions **ADMIN** sur toutes les fonctionnalités
- Sections visibles : SCOLARITÉ, PÉDAGOGIE, FINANCES, ADMINISTRATION, OUTILS

#### Comptable
- **13 vues accessibles**
- **ADMIN** sur Paiements
- **READ** sur données scolaires (Élèves, Classes, Notes, etc.)
- **Aucun accès** aux Utilisateurs, Rôles, Paramètres, Maintenance
- Sections visibles : SCOLARITÉ, PÉDAGOGIE, FINANCES

#### Secrétaire
- **14 vues accessibles**
- **ADMIN** sur Élèves, Classes, Présences, Enseignements, Matières, Salles
- **READ** sur Notes, Bulletins, Rapports
- **Aucun accès** aux Paiements, Utilisateurs, Rôles, Paramètres, Maintenance
- Sections visibles : SCOLARITÉ, PÉDAGOGIE, FINANCES (Rapports uniquement), OUTILS

#### Surveillant
- **10 vues accessibles**
- **ADMIN** sur Présences, Emplois du temps
- **READ** sur Élèves, Classes, Professeurs, Salles, Enseignements, Matières
- **Aucun accès** aux Notes, Bulletins, Paiements, Utilisateurs, etc.
- Sections visibles : SCOLARITÉ, PÉDAGOGIE (partielle), OUTILS (Calendrier uniquement)

## 🏗️ Architecture

### Composants Principaux

1. **`start_rbac_app.py`** - Script de démarrage principal
2. **`src/modules/auth/models/rbac_system.py`** - Système RBAC de base
3. **`src/modules/auth/models/rbac_view_manager.py`** - Gestionnaire de vues RBAC
4. **`src/modules/auth/models/rbac_config.py`** - Configuration centralisée
5. **`src/modules/auth/views/login_view.py`** - Interface de login avec RBAC
6. **`src/modules/auth/views/dashboard_view.py`** - Dashboard avec sidebar filtrée

### Base de Données

Le système utilise SQLite avec les tables suivantes :
- `utilisateurs` - Informations des utilisateurs
- `rbac_roles` - Définition des rôles
- `rbac_user_roles` - Attribution des rôles aux utilisateurs
- `rbac_access_logs` - Logs d'accès

## 🔧 Configuration

### Mode Développement

Pour activer le mode développement (toutes les vues accessibles) :

```python
# Dans rbac_config.py
RBAC_CONFIG = {
    "DEV_MODE": True,  # Activer le mode dev
    # ...
}
```

### Ajouter de Nouveaux Rôles

1. Modifier `src/modules/auth/models/rbac_config.py`
2. Ajouter le rôle dans `DEFAULT_ROLES`
3. Redémarrer l'application

### Modifier les Permissions

1. Éditer `src/modules/auth/models/rbac_config.py`
2. Modifier `VIEW_PERMISSIONS` ou `DEFAULT_ROLES`
3. Redémarrer l'application

## 🧪 Tests

Pour tester le système RBAC :

```bash
python test_rbac_system.py
```

## 📝 Utilisation

### Première Utilisation

1. Lancer `python start_rbac_app.py`
2. Le système initialise automatiquement la base de données
3. Les utilisateurs par défaut sont créés
4. L'interface de login s'ouvre

### Connexion

1. Saisir un nom d'utilisateur et mot de passe
2. Le système vérifie les permissions RBAC
3. La sidebar s'affiche avec les vues autorisées
4. Les tentatives d'accès non autorisées sont bloquées

### Navigation

- La sidebar affiche uniquement les vues autorisées
- Les sections vides sont masquées automatiquement
- Les tentatives d'accès direct aux vues non autorisées affichent un message d'erreur

## 🚨 Sécurité

### Fonctionnalités de Sécurité

- **Authentification** : Vérification des identifiants
- **Autorisation** : Contrôle d'accès basé sur les rôles
- **Logs** : Enregistrement des tentatives d'accès
- **Messages d'erreur** : Pas d'exposition d'informations sensibles

### Bonnes Pratiques

- Changer les mots de passe par défaut en production
- Désactiver `DEV_MODE` en production
- Surveiller les logs d'accès
- Former les utilisateurs aux nouveaux rôles

## 🔄 Maintenance

### Réinitialisation des Utilisateurs

```bash
python reset_users_rbac_fixed.py
```

### Sauvegarde de la Base de Données

```bash
cp database/edumanager.db database/edumanager_backup.db
```

### Mise à Jour

1. Sauvegarder la base de données
2. Mettre à jour les fichiers de configuration
3. Redémarrer l'application

## 📞 Support

En cas de problème :

1. Vérifier les logs dans la console
2. S'assurer que la base de données est accessible
3. Vérifier que tous les modules sont importés correctement
4. Utiliser le mode développement pour diagnostiquer

## 🎯 Statut

✅ **SYSTÈME COMPLET ET FONCTIONNEL**

- [x] Système RBAC implémenté
- [x] Interface de login intégrée
- [x] Dashboard avec sidebar filtrée
- [x] Contrôle d'accès opérationnel
- [x] Utilisateurs par défaut créés
- [x] Tests automatisés validés
- [x] Documentation complète

---

*Dernière mise à jour : Système RBAC complet et opérationnel*
