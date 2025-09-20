# 🏫 Vue Avancée des Présences - EduManager+

## 📋 Description

La vue avancée des présences est un système complet de gestion des présences pour établissements scolaires, intégrant toutes les fonctionnalités modernes nécessaires à une gestion efficace.

## 🚀 Fonctionnalités

### 📊 Gestion des Présences
- **Saisie en temps réel** des présences par classe et date
- **Actions en masse** : valider tout présent, marquer tout absent, réinitialiser
- **Statuts multiples** : Présent, Absent, Retard, Justifié
- **Recherche et filtrage** des élèves

### 🔔 Notifications Automatiques
- **Notifications d'absence** aux parents par email
- **Alertes d'absences répétées** avec seuils configurables
- **Rapports mensuels** automatiques aux familles
- **Rappels de justification** d'absences

### 📄 Export et Rapports
- **Export PDF** des feuilles de présence quotidiennes
- **Export Excel** des rapports mensuels détaillés
- **Historique complet** des élèves en PDF
- **Rapports de synthèse** avec statistiques avancées

### 📎 Gestion des Justificatifs
- **Upload de justificatifs** (PDF, images, documents)
- **Validation des justificatifs** par le personnel
- **Stockage sécurisé** avec organisation par élève
- **Suivi des justificatifs en attente**

### 🚨 Système d'Alertes
- **Alertes automatiques** selon les seuils configurés
- **Détection d'élèves à risque** avec scoring
- **Alertes par niveau** (Info, Warning, Critical, Emergency)
- **Rapports d'alertes** avec recommandations

### 📅 Planification et Calendrier
- **Calendrier scolaire** avec jours fériés et vacances
- **Planning de présence** par classe et période
- **Analyse des tendances** mensuelles et hebdomadaires
- **Prédictions de présence** basées sur l'historique

## 🏗️ Architecture

```
src/modules/academic/attendance/
├── models/
│   └── attendance_model.py          # Modèles de données
├── controllers/
│   ├── attendance_controller.py     # Contrôleur principal
│   ├── attendance_stats_controller.py # Statistiques
│   └── attendance_history_controller.py # Historique
├── services/
│   ├── attendance_service.py        # Service principal
│   ├── attendance_notification_service.py # Notifications
│   ├── attendance_export_service.py # Export/Rapports
│   ├── attendance_justification_service.py # Justificatifs
│   ├── attendance_alert_service.py  # Alertes
│   └── attendance_calendar_service.py # Calendrier
└── views/
    ├── attendance_main_view.py      # Vue principale
    └── advanced_attendance_view.py  # Vue avancée complète
```

## 🚀 Installation et Utilisation

### 1. Vérification des Dépendances
```bash
pip install customtkinter pandas openpyxl fpdf matplotlib pillow
```

### 2. Test d'Intégration
```bash
python test_complete_integration.py
```

### 3. Lancement Rapide
```bash
python launch_advanced_view.py
```

### 4. Intégration dans le Dashboard
La vue avancée est automatiquement intégrée dans le dashboard principal. Elle remplace l'ancienne vue des présences.

## 📱 Interface Utilisateur

### Panneau de Gauche
- **Sélection de classe** et date
- **Recherche et filtrage** des élèves
- **Actions en masse** (valider, marquer absent, réinitialiser)
- **Liste des élèves** avec statuts colorés
- **Statistiques** en temps réel

### Panneau de Droite
- **Détails de l'élève** sélectionné
- **Modification du statut** avec boutons segmentés
- **Commentaires** et justificatifs
- **Historique complet** avec export PDF
- **Système d'alertes** intégré

## ⚙️ Configuration

### Seuils d'Alerte
```python
thresholds = {
    'absence_warning': 3,      # Alerte après 3 absences
    'absence_critical': 5,     # Critique après 5 absences
    'absence_emergency': 10,   # Urgence après 10 absences
    'attendance_rate_warning': 85,  # Alerte si taux < 85%
    'attendance_rate_critical': 75,  # Critique si taux < 75%
    'consecutive_absences': 3,  # Alerte après 3 absences consécutives
    'late_arrivals': 5         # Alerte après 5 retards
}
```

### Calendrier Scolaire
```python
school_config = {
    'academic_year_start': '2024-09-01',
    'academic_year_end': '2025-06-30',
    'school_days_per_week': 5,
    'school_hours': {'start': '08:00', 'end': '17:00'},
    'periods_per_day': 6,
    'period_duration': 50
}
```

## 🧪 Tests

### Tests Disponibles
1. **test_complete_integration.py** - Test complet de l'intégration
2. **test_integration_advanced_view.py** - Test d'intégration spécifique
3. **test_advanced_attendance_features.py** - Test de toutes les fonctionnalités
4. **launch_advanced_view.py** - Lancement rapide pour test

### Exécution des Tests
```bash
# Test complet
python test_complete_integration.py

# Test d'intégration
python test_integration_advanced_view.py

# Test des fonctionnalités
python test_advanced_attendance_features.py

# Lancement rapide
python launch_advanced_view.py
```

## 📊 Avantages

### Pour les Établissements
- **Efficacité** : Automatisation des tâches répétitives
- **Transparence** : Rapports détaillés pour tous les acteurs
- **Prévention** : Détection précoce des problèmes
- **Communication** : Notifications automatiques aux familles
- **Conformité** : Gestion complète des justificatifs
- **Analyse** : Données pour améliorer la gestion

### Pour les Enseignants
- **Interface intuitive** et moderne
- **Actions en masse** pour gagner du temps
- **Alertes automatiques** pour les élèves problématiques
- **Export facile** des rapports

### Pour les Parents
- **Notifications automatiques** des absences
- **Rapports mensuels** détaillés
- **Suivi en temps réel** de la présence

## 🔧 Maintenance

### Logs et Monitoring
- Tous les services incluent des logs détaillés
- Gestion d'erreurs robuste avec messages explicites
- Monitoring des performances

### Mise à Jour
- Architecture modulaire facilitant les mises à jour
- Services indépendants pour une maintenance ciblée
- Tests automatisés pour vérifier la compatibilité

## 📞 Support

Pour toute question ou problème :
1. Vérifiez les logs d'erreur
2. Exécutez les tests de diagnostic
3. Consultez la documentation des services
4. Contactez l'équipe de développement

## 🎉 Conclusion

La vue avancée des présences transforme la gestion des présences en un système moderne, efficace et complet, répondant à tous les besoins des établissements scolaires contemporains.

**Fonctionnalités clés :**
- ✅ Gestion complète des présences
- ✅ Notifications automatiques
- ✅ Export de rapports
- ✅ Gestion des justificatifs
- ✅ Système d'alertes
- ✅ Planification et calendrier
- ✅ Interface moderne et intuitive
- ✅ Architecture modulaire et extensible
