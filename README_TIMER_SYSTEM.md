# 🕐 Système de Minuteur et Notifications pour les Cours - EduManager

## 📋 Description

Système de minuteur/compteur dynamique pour le planning de cours avec :
- **Compte à rebours** avant le début du cours
- **Chronomètre** pendant le cours
- **Notifications élégantes** au lieu de popups intrusifs
- **Mise à jour en temps réel** sans rechargement
- **Design professionnel** inspiré des sites de paris sportifs

## 🔧 Corrections Apportées

### ❌ Problème Identifié
- **Erreur** : `invalid color name "#FFFFFF20"`
- **Cause** : CustomTkinter ne supporte pas les couleurs avec transparence alpha dans le format hexadécimal
- **Impact** : Les notifications ne s'affichaient pas correctement

### ✅ Solution Implémentée
- **Couleurs corrigées** : Remplacement des couleurs avec alpha par des couleurs solides
- **Bouton fermer** : `hover_color="#CCCCCC"` au lieu de `"#FFFFFF20"`
- **Bouton détails** : `fg_color="#333333"` et `hover_color="#555555"` au lieu des couleurs transparentes
- **Compatibilité** : 100% compatible avec CustomTkinter

### 🎯 Résultat
- ✅ **Notifications fonctionnelles** sans erreurs
- ✅ **Design préservé** avec des couleurs appropriées
- ✅ **Performance optimisée** sans erreurs de rendu
- ✅ **Stabilité garantie** pour tous les environnements

## 🎯 Dernières Améliorations Finales

### 🎨 Design des Notifications avec Icônes et Thème EduManager+
- **Icônes réelles** : Utilisation des icônes PNG de votre dossier `resources/icons/`
- **Thème EduManager+** : Couleurs cohérentes avec votre thème sombre
- **Design professionnel** : Notifications avec bordures colorées et coins arrondis
- **Icônes contextuelles** : 
  - 🔔 `bell.png` pour les notifications générales
  - ✅ `check_circle.png` pour les cours terminés
  - 🕐 `clock_icon.png` pour les cours démarrés
  - 📚 `book.png` pour les matières
  - 🏫 `classroom.png` pour les salles
  - 👁️ `view.png` pour le bouton détails
  - ❌ `close.png` pour fermer

### 🔧 Corrections CRUD Complètes
- **Modifier** : Formulaire pré-rempli avec données existantes
- **Supprimer** : Confirmation et gestion d'erreurs améliorée
- **Validation** : Vérification des données avant sauvegarde
- **Feedback** : Messages de succès/erreur appropriés

### ⏰ Heure en Temps Réel
- **Heure actuelle** affichée en gros (20pt) en haut de chaque carte
- **Minuteur détaillé** avec informations contextuelles :
  - ⏳ **En attente** : "Démarre dans XX:XX:XX" + "Début prévu à HH:MM"
  - ▶️ **En cours** : "En cours depuis XX:XX:XX" + "Fin prévue à HH:MM"
  - ✅ **Terminé** : "Terminé - Durée: XX:XX:XX" + "Terminé à HH:MM"

### 🔇 Suppression des Logs
- **Plus de logs dans le terminal** - tout est géré visuellement
- **Notifications silencieuses** - interface propre
- **Historique visuel** via le bouton "📚 Historique"

### 🎨 Design Amélioré
- **Heure actuelle** : Gros caractères bleus (#00D4FF)
- **Minuteur contextuel** : Couleurs dynamiques selon l'état
- **Informations détaillées** : Début/fin prévus, durée écoulée
- **Mise à jour chaque seconde** : Temps réel parfait

## 🎯 Nouvelles Fonctionnalités Ajoutées

### 📚 Bouton Historique des Cours Terminés
- **Bouton "📚 Historique"** dans la barre d'outils de la vue cours
- **Fenêtre dédiée** pour afficher tous les cours terminés
- **Informations complètes** : Matière, Professeur, Classe, Salle, Heure de fin
- **Bouton nettoyer** pour vider l'historique
- **Design moderne** avec cartes élégantes

### ⏰ Minuteur Amélioré dans les Cartes
- **Badge de statut visible** : ⏳ En attente, ▶️ En cours, ✅ Terminé
- **Couleurs dynamiques** selon l'état du cours
- **Minuteur en temps réel** directement dans chaque carte
- **Mise à jour automatique** chaque seconde
- **Design professionnel** avec compteur style 1xBet

### 🔔 Système de Notifications Complet
- **Notifications en haut à droite** au lieu de popups
- **Historique automatique** des cours terminés
- **Plus de logs dans le terminal** - tout est géré visuellement
- **Interface utilisateur intuitive** et non-intrusive

## 🚀 Fonctionnalités

### ⏰ Compte à Rebours
- Affiche le temps restant avant le début du cours
- Format : `HH:MM:SS`
- Couleur verte pour la visibilité
- Texte : "Démarre dans"

### ⏱️ Chronomètre
- Compte le temps écoulé depuis le début du cours
- Format : `HH:MM:SS`
- Couleur bleue vive (#00D4FF)
- Texte : "En cours"

### 🔔 Système de Notifications Élégant
- **Notifications en haut à droite** au lieu de popups
- **Design moderne** avec couleurs dynamiques
- **Boutons d'action intégrés** (Voir détails, Fermer)
- **Auto-suppression** après 10 secondes
- **Types de notifications** :
  - 🎓 **Fin de cours** (rouge)
  - 🚀 **Début de cours** (vert)
  - 📢 **Notifications générales** (bleu)

### 🎨 Design Professionnel
- Gros caractères lisibles
- Couleurs dynamiques selon l'état
- Mise à jour fluide chaque seconde
- Interface moderne et claire
- Notifications non-intrusives

## 📁 Structure des Fichiers

```
src/modules/academic/classes/
├── utils/
│   └── course_timer.py          # Système de minuteur principal
├── views/
│   └── cours_view.py            # Vue des cours avec minuteur intégré
└── controllers/
    └── cours_controller.py      # Contrôleur des cours
```

## 🔧 Utilisation

### 1. Import du Système

```python
from src.modules.academic.classes.utils.course_timer import timer_manager
```

### 2. Intégration dans les Cartes

```python
# Dans votre vue de cours
def create_course_card(self, item, index):
    # ... création de la carte ...
    
    # Section minuteur
    timer_section = ctk.CTkFrame(footer_frame, fg_color="transparent")
    timer_section.pack(side="left", fill="x", expand=True)
    
    # Créer le minuteur
    course_id = item.get('id', index)
    timer_widget = self.timer_manager.add_timer(course_id, timer_section, item)
```

### 3. Nettoyage des Ressources

```python
def destroy(self):
    """Nettoie les ressources lors de la destruction"""
    if hasattr(self, 'timer_manager'):
        self.timer_manager.cleanup_all()
    super().destroy()
```

## 📊 Format des Données

Le système attend des données de cours au format suivant :

```python
course_data = {
    "id": 1,                          # ID unique du cours
    "professeur_nom": "Jean Dupont",  # Nom du professeur
    "classe_nom": "6ème A",           # Nom de la classe
    "matiere_nom": "Mathématiques",   # Nom de la matière
    "salle_nom": "Salle 101",         # Nom de la salle
    "heure": "14:00",                 # Heure de début (HH:MM)
    "duree": 60,                      # Durée en minutes
    "jour": "Lundi"                   # Jour de la semaine
}
```

## 🔔 Système de Notifications

### Types de Notifications

#### 🎓 Fin de Cours
- **Couleur** : Rouge (#F85149)
- **Icône** : 🎓
- **Titre** : "COURS TERMINÉ"
- **Contenu** : Matière, Professeur, Classe, Salle
- **Action** : Bouton "Voir détails"

#### 🚀 Début de Cours
- **Couleur** : Vert (#3FB950)
- **Icône** : 🚀
- **Titre** : "COURS DÉMARRÉ"
- **Contenu** : Informations du cours
- **Action** : Bouton "Voir détails"

#### 📢 Notifications Générales
- **Couleur** : Bleu (#00D4FF)
- **Icône** : 📢
- **Titre** : "NOTIFICATION"
- **Contenu** : Message personnalisé
- **Action** : Bouton "Voir détails"

### Fonctionnalités des Notifications

- **Position** : Haut à droite de l'écran
- **Auto-suppression** : 10 secondes
- **Bouton fermer** : ✕ pour fermer manuellement
- **Bouton détails** : Ouvre une fenêtre avec toutes les informations
- **Animation** : Apparition fluide depuis la droite
- **Empilage** : Plusieurs notifications peuvent s'afficher simultanément

### Utilisation des Notifications

```python
# Ajouter une notification
notification_manager.add_notification(course_data, "course_end")

# Types disponibles
"course_end"     # Fin de cours
"course_start"   # Début de cours
"general"        # Notification générale

# Nettoyer toutes les notifications
notification_manager.clear_all_notifications()
```

## 🎯 États du Minuteur

### 🟢 En Attente (Avant le cours)
- **Couleur** : Vert (#3FB950)
- **Texte** : "Démarre dans HH:MM:SS"
- **État** : Compte à rebours

### 🔵 En Cours (Pendant le cours)
- **Couleur** : Bleu (#00D4FF)
- **Texte** : "En cours HH:MM:SS"
- **État** : Chronomètre

### 🔴 Terminé (Après le cours)
- **Couleur** : Rouge (#F85149)
- **Texte** : "Terminé HH:MM:SS"
- **État** : Durée totale + Alerte

## 🧪 Tests

### Test Simple
```bash
python test_timer_system.py
```

### Démonstration Complète
```bash
python demo_timer_integration.py
```

## ⚙️ Configuration

### Couleurs Personnalisées
```python
# Dans course_timer.py
timer_color = "#00D4FF"  # Bleu principal
countdown_color = "#3FB950"  # Vert compte à rebours
finished_color = "#F85149"  # Rouge terminé
```

### Intervalle de Mise à Jour
```python
# Dans course_timer.py
time.sleep(1)  # Mise à jour chaque seconde
```

## 🔄 Mise à Jour Automatique

Le système utilise des threads pour la mise à jour en temps réel :
- **Thread principal** : Interface utilisateur
- **Thread minuteur** : Calculs et mise à jour
- **Thread-safe** : Mise à jour sécurisée des widgets

## 📱 Responsive Design

- **3 colonnes** par défaut
- **Adaptation automatique** à la taille de l'écran
- **Scrollable** pour de nombreux cours
- **Cartes optimisées** pour la lisibilité

## 🚨 Gestion des Erreurs

- **Gestion des exceptions** dans tous les threads
- **Fallback** en cas d'erreur de parsing d'heure
- **Nettoyage automatique** des ressources
- **Logs détaillés** pour le débogage

## 🎉 Résultat Final Complet

Un système de minuteur et notifications **ultra-professionnel** qui :
- ✅ Affiche le temps restant avant le cours
- ✅ Compte le temps écoulé pendant le cours
- ✅ Notifie élégamment à la fin (sans popups intrusifs)
- ✅ Se met à jour en temps réel
- ✅ A un design moderne et lisible
- ✅ S'intègre parfaitement dans vos cartes existantes
- ✅ Notifications non-intrusives en haut à droite
- ✅ Boutons d'action intégrés dans les notifications
- ✅ Auto-suppression des notifications après 10 secondes
- ✅ **Bouton historique** pour voir tous les cours terminés
- ✅ **Minuteur visible** directement dans chaque carte
- ✅ **Badge de statut** dynamique et coloré
- ✅ **Plus de logs dans le terminal** - tout est visuel
- ✅ **Heure actuelle** affichée en temps réel (20pt)
- ✅ **Minuteur contextuel** avec informations détaillées
- ✅ **Interface silencieuse** - notifications visuelles uniquement
- ✅ **Icônes réelles** de votre dossier `resources/icons/`
- ✅ **Thème EduManager+** cohérent avec votre design
- ✅ **CRUD complet** : Ajouter, Modifier, Supprimer fonctionnels
- ✅ **Formulaire pré-rempli** en mode modification
- ✅ **Validation et feedback** appropriés

**Parfait pour un planning de cours professionnel et moderne !** 🎓✨
