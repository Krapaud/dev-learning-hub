# 🚀 Dev Learning Hub

**Plateforme d'apprentissage gamifiée pour la programmation avec un thème cyberpunk Matrix**

[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/Krapaud/dev-learning-hub)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](https://flask.palletsprojects.com)

## ✨ Fonctionnalités

### 🎮 Gamification
- **Système de points** : Gagnez des points en complétant des leçons
- **Trophées** : Débloquez des trophées uniques pour vos réalisations
- **Niveaux** : Progressez et montez en niveau selon vos points
- **Progression visuelle** : Barres de progression animées et statistiques détaillées

### 📚 Cours Disponibles
- **Shell/Terminal** - Maîtrisez la ligne de commande
- **HTML5** - Créez la structure de vos pages web
- **CSS3** - Stylisez et animez vos interfaces
- **Langage C** - Apprenez les fondamentaux de la programmation
- **Python** - Découvrez le langage polyvalent du développement moderne

### 🎨 Interface Moderne
- **Thème Geek Sombre** - Design inspiré de Matrix et de l'univers cyberpunk
- **Animations fluides** - Transitions et effets visuels immersifs
- **Responsive Design** - Compatible desktop, tablette et mobile
- **Effets néon** - Éléments brillants et colorés

### 🔐 Système d'Authentification
- **Inscription/Connexion** sécurisée
- **Gestion des sessions** utilisateur
- **Profils personnalisés** avec statistiques
- **Sauvegarde automatique** de la progression

## 🛠️ Technologies Utilisées

### Backend
- **Python 3.8+** - Langage principal
- **Flask** - Framework web minimaliste et puissant
- **SQLAlchemy** - ORM pour la gestion de base de données
- **Flask-Login** - Gestion d'authentification
- **SQLite** - Base de données légère et intégrée

### Frontend
- **HTML5** - Structure sémantique moderne
- **CSS3** - Styles avancés avec variables CSS et animations
- **JavaScript ES6+** - Interactivité et effets dynamiques
- **Font Awesome** - Icônes vectorielles
- **Google Fonts** - Typographies JetBrains Mono et Inter

### Design
- **Thème sombre** avec palette de couleurs cyberpunk
- **Animations CSS** et transitions fluides
- **Effet Matrix** en arrière-plan
- **Interface utilisateur** intuitive et moderne

## 🚀 Installation et Configuration

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Git (optionnel)

### Installation

1. **Cloner le projet** (ou télécharger les fichiers)
```bash
git clone https://github.com/votre-username/dev-learning-hub.git
cd dev-learning-hub
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv venv

# Sur Linux/macOS
source venv/bin/activate

# Sur Windows
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Lancer l'application**
```bash
python app.py
```

5. **Ouvrir dans le navigateur**
```
http://localhost:5000
```

## 📁 Structure du Projet

```
dev-learning-hub/
├── app.py                 # Application Flask principale
├── requirements.txt       # Dépendances Python
├── README.md             # Documentation du projet
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css     # Styles CSS principaux
│   ├── js/
│   │   └── main.js       # JavaScript principal
│   └── images/           # Images et assets
├── templates/            # Templates HTML
│   ├── base.html         # Template de base
│   ├── index.html        # Page d'accueil
│   ├── login.html        # Page de connexion
│   ├── register.html     # Page d'inscription
│   ├── dashboard.html    # Dashboard utilisateur
│   ├── course_detail.html # Détail des cours
│   ├── lesson_detail.html # Détail des leçons
│   └── trophies.html     # Page des trophées
└── dev_learning_hub.db   # Base de données SQLite (créée automatiquement)
```

## 🎯 Utilisation

### Pour les Étudiants

1. **Créer un compte** - Inscrivez-vous avec un nom d'utilisateur unique
2. **Explorer les cours** - Parcourez les 5 langages disponibles
3. **Suivre les leçons** - Progression séquentielle avec contenu interactif
4. **Gagner des points** - 10 points par leçon complétée
5. **Débloquer des trophées** - Objectifs à atteindre pour collectionner
6. **Suivre sa progression** - Dashboard personnel avec statistiques

### Pour les Développeurs

- **Code modulaire** et bien documenté
- **Architecture MVC** avec Flask
- **Base de données** facilement extensible
- **Thème personnalisable** via variables CSS
- **APIs RESTful** pour les actions utilisateur

## 🏆 Système de Trophées

### 🥉 Bronze
- **Premier Pas** - Complétez votre première leçon
- **Étudiant Assidu** - Complétez 10 leçons

### 🥈 Argent
- **Collectionneur de Points** - Gagnez 100 points
- **Maître du Code** - Complétez votre premier cours

### 🥇 Or
- **Polyglotte** - Complétez 3 cours différents

### 💎 Platine
- **Ninja du Terminal** - Maîtrisez le Shell
- **Architecte Web** - Terminez HTML + CSS
- **Programmeur Confirmé** - Terminez C + Python

## 🔧 Personnalisation

### Modifier le Thème
Les couleurs sont définies dans `static/css/style.css` avec des variables CSS :
```css
:root {
    --accent-primary: #00ff88;    /* Vert Matrix */
    --accent-secondary: #00d4ff;  /* Bleu Cyber */
    --bg-primary: #0d1117;        /* Noir profond */
    /* ... autres variables */
}
```

### Ajouter de Nouveaux Cours
1. Modifier `init_db()` dans `app.py`
2. Ajouter les données du cours et des leçons
3. Créer le contenu détaillé dans `lesson_detail.html`

### Nouveaux Trophées
Ajouter dans la section `trophies_data` de `app.py` :
```python
{
    'name': 'Nom du Trophée',
    'description': 'Description',
    'icon': '🏆',
    'requirement_type': 'points',  # ou 'courses_completed', 'lessons_completed'
    'requirement_value': 50,
    'rarity': 'bronze'  # bronze, silver, gold, platinum
}