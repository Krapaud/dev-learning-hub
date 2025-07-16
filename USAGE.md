# Guide d'Utilisation - Dev Learning Hub

## 🚀 Démarrage rapide

### 1. Installation
```bash
# Cloner le projet
git clone <votre-repo>
cd dev-learning-hub

# Créer l'environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### 2. Lancement
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer l'application
python app.py
```

### 3. Accès
Ouvrir votre navigateur sur : http://localhost:5000

## 📖 Fonctionnalités principales

### Pour les utilisateurs :
1. **Inscription** - Créer un compte avec un nom d'utilisateur unique
2. **Connexion** - Se connecter à son compte
3. **Cours** - Accéder aux 5 cours disponibles :
   - Shell/Terminal
   - HTML5
   - CSS3
   - Langage C
   - Python
4. **Leçons** - Suivre les leçons de manière séquentielle
5. **Points** - Gagner 10 points par leçon complétée
6. **Niveaux** - Progression automatique (1 niveau = 100 points)
7. **Trophées** - Débloquer des récompenses selon les objectifs

### Système de trophées :
- **Bronze** : Premier Pas (1 leçon), Étudiant Assidu (10 leçons)
- **Argent** : Collectionneur de Points (100 points), Maître du Code (1 cours)
- **Or** : Polyglotte (3 cours)

## 🛠️ Structure technique

### Base de données :
- **Users** : Comptes utilisateurs avec points et niveau
- **Courses** : Les 5 cours avec leurs métadonnées
- **Lessons** : Leçons organisées par cours
- **CompletedLessons** : Suivi de progression
- **Trophies** : Définition des trophées
- **UserTrophies** : Trophées obtenus par utilisateur

### Routes principales :
- `/` - Page d'accueil
- `/register` - Inscription
- `/login` - Connexion
- `/dashboard` - Tableau de bord utilisateur
- `/course/<id>` - Détail d'un cours
- `/lesson/<id>` - Détail d'une leçon
- `/trophies` - Page des trophées
- `/complete_lesson/<id>` - API pour marquer une leçon comme terminée

## 🎨 Personnalisation

### Couleurs (dans static/css/style.css) :
```css
:root {
    --accent-primary: #00ff88;      /* Vert Matrix */
    --accent-secondary: #00d4ff;    /* Bleu Cyber */
    --accent-tertiary: #ff6b35;     /* Orange néon */
    --accent-quaternary: #ffd93d;   /* Jaune électrique */
    --bg-primary: #0d1117;          /* Noir profond */
    /* ... */
}
```

### Ajouter un nouveau cours :
1. Modifier la fonction `init_database()` dans `app.py`
2. Ajouter les données du cours dans `courses_data`
3. Définir les leçons correspondantes

### Ajouter un nouveau trophée :
1. Modifier `trophies_data` dans `init_database()`
2. Mettre à jour la fonction `check_trophies()` si nécessaire

## 🔧 Développement

### Mode debug :
Le mode debug est activé par défaut. Pour le désactiver :
```python
app.run(debug=False)
```

### Base de données :
La base de données SQLite est créée automatiquement au premier lancement.
Pour réinitialiser : supprimer le fichier `dev_learning_hub.db`

### Logs :
Les erreurs sont affichées dans la console et dans le navigateur (mode debug)

## 📱 Responsive Design

L'interface s'adapte automatiquement :
- **Desktop** : Layout complet avec sidebar
- **Tablette** : Layout adapté avec navigation simplifiée  
- **Mobile** : Interface optimisée, effet Matrix désactivé pour les performances

## 🎮 Gamification

### Système de points :
- 10 points par leçon complétée
- Progression sauvegardée automatiquement
- Calcul automatique du niveau (100 points = 1 niveau)

### Trophées :
- Vérification automatique après chaque leçon
- Notification en temps réel
- Collection persistante

## 🚀 Déploiement

Pour un déploiement en production :
1. Utiliser une base de données plus robuste (PostgreSQL)
2. Configurer un serveur web (Nginx)
3. Utiliser un serveur WSGI (Gunicorn)
4. Configurer les variables d'environnement
5. Activer HTTPS

Exemple avec Gunicorn :
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```
