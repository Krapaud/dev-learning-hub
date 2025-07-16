# Dev Learning Hub

## 📚 Plateforme d'apprentissage pour développeurs

Dev Learning Hub est une plateforme web complète dédiée à l'apprentissage de la programmation, conçue avec un thème geek sombre moderne. Cette plateforme propose des cours structurés, un système d'authentification, un suivi de progression et un système de succès pour motiver les apprenants.

## 🚀 Fonctionnalités

### 🎯 Cours disponibles
- **HTML5** - Les bases du langage de balisage web (15 leçons)
- **CSS3** - Maîtrisez les feuilles de style (20 leçons)
- **Langage C** - Programmation système (25 leçons)
- **Python** - Langage idéal pour débuter (30 leçons)

### 👤 Système d'authentification
- Inscription et connexion sécurisées
- Profils utilisateur personnalisés
- Sauvegarde locale des données
- Gestion des sessions

### 📊 Suivi de progression
- Progression détaillée par cours
- Statistiques d'apprentissage
- Temps passé sur chaque cours
- Série d'apprentissage (streak)
- Historique d'activité

### 🏆 Système de succès
- 10+ succès à débloquer
- Récompenses pour la régularité
- Badges de progression
- Notifications de succès

### 🎨 Interface moderne
- Thème geek sombre avec effets de lumière
- Design responsive (mobile-friendly)
- Animations fluides
- Typographie monospace
- Effets de parallaxe

## 🛠️ Technologies utilisées

### Frontend
- **HTML5** - Structure sémantique
- **CSS3** - Styles avancés avec variables CSS
- **JavaScript (ES6+)** - Logique applicative moderne
- **Font Awesome** - Icônes

### Fonctionnalités JavaScript
- Classes ES6
- LocalStorage pour la persistance
- Intersection Observer API
- Event Delegation
- Modular Architecture

## 📁 Structure du projet

```
dev-learning-hub/
├── index.html              # Page principale
├── css/
│   └── style.css           # Styles principaux
├── js/
│   ├── app.js             # Logique principale
│   ├── auth.js            # Système d'authentification
│   ├── courses.js         # Gestion des cours
│   └── progress.js        # Suivi de progression
└── README.md              # Documentation
```

## 🚀 Installation et utilisation

1. **Clonez le repository**
   ```bash
   git clone https://github.com/Krapaud/dev-learning-hub.git
   cd dev-learning-hub
   ```

2. **Ouvrez le projet**
   - Ouvrez `index.html` dans votre navigateur
   - Ou utilisez un serveur local :
   ```bash
   # Avec Python
   python -m http.server 8000
   
   # Avec Node.js (http-server)
   npx http-server
   
   # Avec PHP
   php -S localhost:8000
   ```

3. **Accédez à l'application**
   - Ouvrez votre navigateur
   - Visitez `http://localhost:8000`

## 📖 Guide d'utilisation

### Première utilisation
1. Cliquez sur "Inscription" pour créer un compte
2. Remplissez le formulaire d'inscription
3. Connectez-vous avec vos identifiants
4. Explorez les cours disponibles

### Navigation
- **Accueil** - Présentation de la plateforme
- **Cours** - Catalogue des cours avec filtres par difficulté
- **Progression** - Statistiques personnelles
- **Succès** - Badges et récompenses

### Apprentissage
1. Cliquez sur un cours dans la section "Cours"
2. Suivez les leçons dans l'ordre
3. Votre progression est automatiquement sauvegardée
4. Débloquez des succès en atteignant certains objectifs

## 🎯 Cours détaillés

### HTML5 (Débutant)
- Introduction au HTML
- Balises de titre
- Paragraphes et texte
- Listes et liens
- Images et multimédia
- Formulaires
- Tableaux
- HTML sémantique

### CSS3 (Débutant)
- Introduction au CSS
- Sélecteurs
- Propriétés de base
- Box Model
- Flexbox
- Grid
- Animations
- Responsive Design

### Langage C (Intermédiaire)
- Introduction au C
- Variables et types
- Structures de contrôle
- Fonctions
- Pointeurs
- Tableaux
- Structures
- Fichiers

### Python (Débutant)
- Introduction à Python
- Variables et types
- Structures de données
- Structures de contrôle
- Fonctions
- Modules
- Programmation orientée objet
- Manipulation de fichiers

## 🏆 Système de succès

### Succès disponibles
- **Premier pas** - Terminer votre première leçon
- **Apprenti HTML** - Terminer 5 leçons HTML
- **Styliste CSS** - Terminer 5 leçons CSS
- **Apprenant dévoué** - Passer 5 heures à apprendre
- **Maître du cours** - Terminer un cours complet
- **Polyglotte** - Commencer 3 langages différents
- **Apprenant rapide** - Terminer 10 leçons en une journée
- **Régularité** - Apprendre 7 jours consécutifs
- **Oiseau de nuit** - Apprendre après minuit
- **Lève-tôt** - Apprendre avant 7h du matin

## 💾 Persistance des données

Les données utilisateur sont stockées localement dans le navigateur :
- **localStorage** pour les données utilisateur
- **sessionStorage** pour les données temporaires
- Sauvegarde automatique toutes les 30 secondes

## 🎨 Personnalisation

### Variables CSS
Le thème peut être personnalisé via les variables CSS dans `style.css` :

```css
:root {
    --primary-color: #00ff41;      /* Vert Matrix */
    --secondary-color: #ff6b35;    /* Orange accent */
    --bg-color: #0a0a0a;          /* Noir profond */
    --surface-color: #1a1a1a;     /* Gris sombre */
    --text-primary: #ffffff;       /* Blanc */
    --accent-color: #00ffff;       /* Cyan */
}
```

### Ajout de cours
Pour ajouter un nouveau cours, modifiez `js/courses.js` :

```javascript
nouveauCours: {
    id: 'nouveau',
    title: 'Nouveau Cours',
    icon: 'fas fa-code',
    color: '#couleur',
    difficulty: 'debutant',
    description: 'Description du cours',
    duration: 'X leçons',
    students: 'Y étudiants',
    lessons: [
        {
            id: 1,
            title: 'Première leçon',
            content: 'Contenu HTML de la leçon'
        }
    ]
}
```

## 🔧 Développement

### Structure du code
- **Modular** - Code organisé en modules
- **ES6+ Classes** - Utilisation des classes JavaScript
- **Event-driven** - Architecture basée sur les événements
- **Responsive** - Design adaptatif

### Bonnes pratiques
- Code commenté et documenté
- Séparation des responsabilités
- Gestion d'erreur robuste
- Performance optimisée

## 🌟 Fonctionnalités avancées

### Animations
- Effets de parallaxe
- Animations d'entrée
- Transitions fluides
- Effets de hover

### Accessibilité
- Navigation au clavier
- Contrastes élevés
- Labels appropriés
- Structure sémantique

### Performance
- Code optimisé
- Lazy loading
- Compression d'images
- Minimisation des requêtes

## 📱 Compatibilité

### Navigateurs supportés
- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Résolutions
- Desktop : 1920x1080 et plus
- Tablet : 768x1024
- Mobile : 375x667 et plus

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche feature
3. Committez vos changements
4. Pushez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Krapaud** - Développeur passionné
- GitHub: [@Krapaud](https://github.com/Krapaud)

## 🙏 Remerciements

- Font Awesome pour les icônes
- La communauté open source
- Tous les contributeurs

---

**Dev Learning Hub** - Votre passerelle vers la maîtrise de la programmation ! 🚀
