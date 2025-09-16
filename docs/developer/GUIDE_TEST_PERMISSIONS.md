# Guide de Test des Permissions

## 🎯 Objectif

Ce guide vous permet de tester que le système de permissions fonctionne correctement et que chaque utilisateur ne voit que les vues appropriées à son rôle.

## 🚀 Démarrage Rapide

### 1. Lancer l'Application
```bash
python main.py
```

### 2. Tester avec Différents Comptes

#### Compte Admin (Accès Complet)
- **Username:** `admin`
- **Password:** `admin123`
- **Rôle:** Super Administrateur
- **Attendu:** Toutes les vues visibles

#### Compte Directeur (Accès Étendu)
- **Username:** `directeur`
- **Password:** `directeur123`
- **Rôle:** Directeur
- **Attendu:** Vues de gestion, pas d'accès aux paramètres système

#### Compte Professeur (Accès Pédagogique)
- **Username:** `professeur`
- **Password:** `prof123`
- **Rôle:** Professeur
- **Attendu:** Modules pédagogiques uniquement

#### Compte Élève (Accès Limité)
- **Username:** `eleve`
- **Password:** `eleve123`
- **Rôle:** Élève
- **Attendu:** Consultation uniquement de ses données

## 🔍 Points de Test

### Test 1: Vérification de la Sidebar
1. Connectez-vous avec un compte
2. Observez la sidebar (menu de gauche)
3. Vérifiez que seules les sections appropriées sont visibles
4. Comptez le nombre de vues disponibles

### Test 2: Accès aux Vues
1. Cliquez sur différentes vues dans la sidebar
2. Vérifiez que vous pouvez accéder aux vues autorisées
3. Testez l'accès aux vues qui devraient être restreintes
4. Vérifiez que les messages d'erreur s'affichent correctement

### Test 3: Comparaison des Rôles
1. Testez avec au moins 3 comptes différents
2. Comparez les vues disponibles
3. Vérifiez que les restrictions sont respectées

## 📊 Résultats Attendus

### Super Administrateur (admin)
```
✅ SCOLARITÉ: 5 vues (dashboard, eleves, profs, classes, salles)
✅ PÉDAGOGIE: 6 vues (enseignements, matieres, notes, presences, bulletins, emplois)
✅ FINANCES: 1 vue (paiements)
✅ ADMINISTRATION: 5 vues (utilisateurs, actualites, annonces, notifications, taches)
✅ OUTILS: 11 vues (biblio, calendriers, carrieres, competences, documents, maintenances, messagerie, objectifs, personnel, transfert, settings)
```

### Directeur
```
✅ SCOLARITÉ: 5 vues
✅ PÉDAGOGIE: 6 vues
✅ FINANCES: 1 vue
✅ ADMINISTRATION: 3 vues (actualites, annonces, notifications)
✅ OUTILS: 10 vues
❌ Pas d'accès: utilisateurs, taches, settings
```

### Professeur
```
✅ SCOLARITÉ: 3 vues (dashboard, eleves, classes)
✅ PÉDAGOGIE: 5 vues (matieres, notes, presences, bulletins, emplois)
✅ OUTILS: 4 vues (calendriers, messagerie, objectifs, competences)
❌ Pas d'accès: profs, salles, enseignements, paiements, utilisateurs
```

### Élève
```
✅ SCOLARITÉ: 1 vue (dashboard)
✅ PÉDAGOGIE: 3 vues (notes, bulletins, emplois)
✅ OUTILS: 4 vues (calendriers, messagerie, objectifs, competences)
❌ Pas d'accès: eleves, profs, classes, salles, enseignements, matieres, presences, paiements, utilisateurs
```

## 🐛 Dépannage

### Problème: Toutes les vues sont visibles
**Cause possible:** L'utilisateur n'a pas de rôle assigné
**Solution:** Vérifiez que l'utilisateur a un rôle dans la base de données

### Problème: Erreur lors de la connexion
**Cause possible:** Tables de permissions non initialisées
**Solution:** Exécutez `python init_roles_simple.py`

### Problème: Certaines vues ne s'affichent pas
**Cause possible:** Vue non définie dans les permissions du rôle
**Solution:** Vérifiez la configuration dans `models/view_permissions.py`

### Problème: Messages d'erreur inappropriés
**Cause possible:** Gestion d'erreur non configurée
**Solution:** Vérifiez les logs de l'application

## 📝 Logs à Surveiller

### Logs de Connexion
```
✅ Connexion réussie pour [username]
✅ Rôle [role] détecté pour [username]
```

### Logs de Permissions
```
✅ Accès autorisé à la vue [view] pour [username]
❌ Accès refusé à la vue [view] pour [username]
```

### Logs d'Erreur
```
⚠️ Erreur vérification accès vue [view] pour utilisateur [id]: [error]
```

## 🎯 Critères de Validation

### ✅ Test Réussi Si:
- [ ] Chaque utilisateur voit uniquement ses vues autorisées
- [ ] Les sections vides ne s'affichent pas
- [ ] Les messages d'erreur sont appropriés
- [ ] La navigation est intuitive et adaptée
- [ ] Aucune vue restreinte n'est accessible

### ❌ Test Échoué Si:
- [ ] Toutes les vues sont visibles pour tous
- [ ] Les restrictions ne sont pas respectées
- [ ] Erreurs lors de la vérification des permissions
- [ ] Interface incohérente ou cassée

## 🔄 Tests Recommandés

### Test de Base
1. Connexion avec chaque type de compte
2. Vérification de la sidebar
3. Test d'accès aux vues principales

### Test de Sécurité
1. Tentative d'accès aux vues restreintes
2. Vérification des messages d'erreur
3. Test de contournement des restrictions

### Test de Robustesse
1. Connexion/déconnexion rapide
2. Changement de vues fréquent
3. Test avec des données volumineuses

## 📞 Support

En cas de problème :
1. Vérifiez les logs de l'application
2. Consultez `GUIDE_PERMISSIONS_VUES.md`
3. Testez avec `python test_simple_permissions.py`
4. Vérifiez la structure de la base de données

## 🎉 Validation Finale

Une fois tous les tests passés, votre système de permissions est **opérationnel** et **sécurisé** !

Chaque utilisateur ne verra que ce qui lui est approprié selon son rôle dans l'établissement scolaire.

