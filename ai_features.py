"""
Module IA pour Dev Learning Hub
Fonctionnalités d'intelligence artificielle et de personnalisation
"""

import os
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import current_app

class AIRecommendationEngine:
    """Moteur de recommandations personnalisées"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.course_vectors = None
        self.user_preferences = {}
        
    def get_personalized_recommendations(self, user_id: int, completed_courses: List[int]) -> List[Dict]:
        """Génère des recommandations personnalisées pour un utilisateur"""
        # Import dans la fonction pour éviter les problèmes de contexte
        with current_app.app_context():
            from app import Course, User, CompletedLesson, Lesson
            
            user = User.query.get(user_id)
            if not user:
                return []
                
            # Analyser les préférences de l'utilisateur
            user_profile = self._build_user_profile(user_id)
            
            # Obtenir tous les cours disponibles
            all_courses = Course.query.all()
            available_courses = [c for c in all_courses if c.id not in completed_courses]
            
            # Calculer les scores de recommandation
            recommendations = []
            for course in available_courses:
                score = self._calculate_recommendation_score(user_profile, course)
                recommendations.append({
                    'course': course,
                    'score': score,
                    'reason': self._get_recommendation_reason(user_profile, course)
                })
            
            # Trier par score et retourner les meilleures recommandations
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            return recommendations[:3]
        return recommendations[:3]
    
    def _build_user_profile(self, user_id: int) -> Dict:
        """Construit le profil d'apprentissage d'un utilisateur"""
        with current_app.app_context():
            from app import CompletedLesson, Lesson, Course
            
            completed_lessons = CompletedLesson.query.filter_by(user_id=user_id).all()
            
            profile = {
                'completed_courses': set(),
                'favorite_topics': [],
                'learning_speed': 'medium',
                'difficulty_preference': 'beginner',
                'time_patterns': []
            }
            
            for completed in completed_lessons:
                lesson = completed.lesson
                course = lesson.course
                profile['completed_courses'].add(course.name.lower())
                
                # Analyser les patterns temporels
                profile['time_patterns'].append(completed.completed_at.hour)
            
            # Déterminer la vitesse d'apprentissage
            if len(completed_lessons) > 15:
                profile['learning_speed'] = 'fast'
            elif len(completed_lessons) < 5:
                profile['learning_speed'] = 'slow'
                
            return profile
    
    def _calculate_recommendation_score(self, user_profile: Dict, course) -> float:
        """Calcule le score de recommandation pour un cours"""
        score = 0.5  # Score de base
        
        # Bonus selon les cours complétés
        if 'html5' in user_profile['completed_courses'] and course.name.lower() == 'css3':
            score += 0.4
        elif 'css3' in user_profile['completed_courses'] and course.name.lower() == 'javascript':
            score += 0.4
        elif 'shell/terminal' in user_profile['completed_courses'] and course.name.lower() == 'python':
            score += 0.3
            
        # Bonus selon la vitesse d'apprentissage
        if user_profile['learning_speed'] == 'fast' and course.name.lower() in ['langage c', 'python']:
            score += 0.2
        elif user_profile['learning_speed'] == 'slow' and course.name.lower() in ['html5', 'css3']:
            score += 0.2
            
        # Ajouter un peu d'aléatoire pour la diversité
        score += random.uniform(-0.1, 0.1)
        
        return min(score, 1.0)
    
    def _get_recommendation_reason(self, user_profile: Dict, course) -> str:
        """Génère une explication pour la recommandation"""
        reasons = [
            f"Basé sur votre progression actuelle, {course.name} semble être le prochain défi idéal",
            f"Votre vitesse d'apprentissage ({user_profile['learning_speed']}) correspond bien à {course.name}",
            f"Les utilisateurs ayant un profil similaire ont excellé dans {course.name}",
            f"{course.name} complète parfaitement vos connaissances actuelles"
        ]
        return random.choice(reasons)

class AIAssistant:
    """Assistant IA pour l'aide contextuelle"""
    
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        
    def get_contextual_help(self, lesson_content: str, user_question: str = None) -> Dict:
        """Fournit une aide contextuelle pour une leçon"""
        
        # Analyser le contenu de la leçon
        lesson_topics = self._extract_topics(lesson_content)
        
        # Générer des explications et exemples
        help_data = {
            'explanation': self._generate_explanation(lesson_topics),
            'examples': self._get_relevant_examples(lesson_topics),
            'tips': self._get_learning_tips(lesson_topics),
            'common_mistakes': self._get_common_mistakes(lesson_topics)
        }
        
        # Si une question spécifique est posée
        if user_question:
            help_data['specific_answer'] = self._answer_question(user_question, lesson_topics)
            
        return help_data
    
    def _load_knowledge_base(self) -> Dict:
        """Charge la base de connaissances"""
        return {
            'html': {
                'concepts': ['tags', 'attributes', 'elements', 'structure'],
                'examples': [
                    '<h1>Titre principal</h1>',
                    '<p>Paragraphe de texte</p>',
                    '<a href="url">Lien</a>'
                ],
                'tips': ['Toujours fermer les tags', 'Utiliser la sémantique HTML5'],
                'mistakes': ['Oublier de fermer les tags', 'Imbriquer incorrectement']
            },
            'css': {
                'concepts': ['selectors', 'properties', 'values', 'cascade'],
                'examples': [
                    'h1 { color: blue; }',
                    '.classe { background: red; }',
                    '#id { margin: 10px; }'
                ],
                'tips': ['Utiliser les classes plutôt que les IDs', 'Organiser le CSS par composants'],
                'mistakes': ['Oublier les points-virgules', 'Spécificité trop élevée']
            },
            'python': {
                'concepts': ['variables', 'functions', 'loops', 'conditions'],
                'examples': [
                    'print("Hello World")',
                    'def ma_fonction(): pass',
                    'for i in range(10): print(i)'
                ],
                'tips': ['Respecter PEP 8', 'Utiliser des noms explicites'],
                'mistakes': ['Indentation incorrecte', 'Variables non définies']
            }
        }
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extrait les sujets principaux du contenu"""
        topics = []
        content_lower = content.lower()
        
        for topic, data in self.knowledge_base.items():
            if topic in content_lower:
                topics.append(topic)
                
        return topics if topics else ['general']
    
    def _generate_explanation(self, topics: List[str]) -> str:
        """Génère une explication contextuelle"""
        if not topics or topics == ['general']:
            return "Cette leçon couvre des concepts fondamentaux importants pour votre apprentissage."
            
        topic = topics[0]
        explanations = {
            'html': "HTML est le langage de balisage qui structure le contenu web. Chaque élément a un rôle spécifique.",
            'css': "CSS contrôle l'apparence et la mise en page. Il utilise des sélecteurs pour cibler les éléments.",
            'python': "Python est un langage de programmation lisible et puissant, parfait pour débuter.",
            'shell': "Le shell vous permet d'interagir directement avec le système d'exploitation."
        }
        
        return explanations.get(topic, "Concept important pour votre progression.")
    
    def _get_relevant_examples(self, topics: List[str]) -> List[str]:
        """Retourne des exemples pertinents"""
        if not topics or topics == ['general']:
            return ["Exemple pratique à venir..."]
            
        topic = topics[0]
        if topic in self.knowledge_base:
            return self.knowledge_base[topic]['examples'][:2]
            
        return ["Exemple contextuel généré automatiquement"]
    
    def _get_learning_tips(self, topics: List[str]) -> List[str]:
        """Retourne des conseils d'apprentissage"""
        general_tips = [
            "Pratiquez régulièrement pour consolider vos acquis",
            "N'hésitez pas à expérimenter et faire des erreurs",
            "Créez des projets personnels pour appliquer vos connaissances"
        ]
        
        if not topics or topics == ['general']:
            return general_tips[:2]
            
        topic = topics[0]
        if topic in self.knowledge_base:
            return self.knowledge_base[topic]['tips']
            
        return general_tips[:2]
    
    def _get_common_mistakes(self, topics: List[str]) -> List[str]:
        """Retourne les erreurs communes à éviter"""
        if not topics or topics == ['general']:
            return ["Aller trop vite sans comprendre les bases"]
            
        topic = topics[0]
        if topic in self.knowledge_base:
            return self.knowledge_base[topic]['mistakes']
            
        return ["Erreurs courantes spécifiques au contexte"]
    
    def _answer_question(self, question: str, topics: List[str]) -> str:
        """Répond à une question spécifique"""
        question_lower = question.lower()
        
        # Réponses basiques selon le contexte
        if 'comment' in question_lower or 'how' in question_lower:
            return "Voici une approche étape par étape pour résoudre cette question..."
        elif 'pourquoi' in question_lower or 'why' in question_lower:
            return "Cette concept est important car il constitue une base fondamentale..."
        elif 'exemple' in question_lower or 'example' in question_lower:
            return f"Voici un exemple pratique : {self._get_relevant_examples(topics)[0]}"
        else:
            return "Basé sur le contexte de la leçon, voici une explication détaillée..."

class DifficultyDetector:
    """Détecteur de difficultés d'apprentissage"""
    
    def __init__(self):
        self.user_patterns = {}
        
    def analyze_user_progress(self, user_id: int) -> Dict:
        """Analyse les patterns de progression d'un utilisateur"""
        from app import User, CompletedLesson
        
        user = User.query.get(user_id)
        completed_lessons = CompletedLesson.query.filter_by(user_id=user_id).order_by(CompletedLesson.completed_at).all()
        
        if len(completed_lessons) < 3:
            return {'status': 'insufficient_data', 'recommendations': []}
        
        # Analyser les patterns temporels
        time_intervals = []
        for i in range(1, len(completed_lessons)):
            interval = (completed_lessons[i].completed_at - completed_lessons[i-1].completed_at).days
            time_intervals.append(interval)
        
        avg_interval = np.mean(time_intervals) if time_intervals else 0
        
        # Détecter les difficultés
        difficulties = []
        
        # Rythme trop lent
        if avg_interval > 7:
            difficulties.append({
                'type': 'slow_pace',
                'severity': 'medium',
                'description': 'Rythme d\'apprentissage ralenti détecté'
            })
        
        # Inactivité récente
        last_lesson = completed_lessons[-1]
        days_since_last = (datetime.utcnow() - last_lesson.completed_at).days
        
        if days_since_last > 14:
            difficulties.append({
                'type': 'inactivity',
                'severity': 'high',
                'description': 'Période d\'inactivité prolongée'
            })
        
        # Générer des recommandations
        recommendations = self._generate_recommendations(difficulties, user)
        
        return {
            'status': 'analyzed',
            'difficulties': difficulties,
            'recommendations': recommendations,
            'avg_interval': avg_interval,
            'last_activity': days_since_last
        }
    
    def _generate_recommendations(self, difficulties: List[Dict], user) -> List[str]:
        """Génère des recommandations basées sur les difficultés détectées"""
        recommendations = []
        
        for difficulty in difficulties:
            if difficulty['type'] == 'slow_pace':
                recommendations.extend([
                    "Essayez de définir des objectifs quotidiens plus petits",
                    "Pratiquez 15-20 minutes par jour plutôt que de longues sessions",
                    "Rejoignez un groupe d'étude pour rester motivé"
                ])
            elif difficulty['type'] == 'inactivity':
                recommendations.extend([
                    "Reprenez avec une leçon de révision",
                    "Fixez-vous un horaire d'étude régulier",
                    "Activez les notifications de rappel"
                ])
        
        if not recommendations:
            recommendations = [
                "Votre progression est excellente, continuez ainsi !",
                "Explorez les projets pratiques pour approfondir",
                "Partagez vos connaissances avec la communauté"
            ]
        
        return recommendations[:3]

class ContentGenerator:
    """Générateur de contenu personnalisé"""
    
    def __init__(self):
        self.exercise_templates = self._load_exercise_templates()
        
    def generate_personalized_exercise(self, user_id: int, lesson_topic: str, difficulty: str = 'medium') -> Dict:
        """Génère un exercice personnalisé"""
        
        exercise_data = {
            'title': f"Exercice personnalisé : {lesson_topic}",
            'description': self._generate_description(lesson_topic, difficulty),
            'tasks': self._generate_tasks(lesson_topic, difficulty),
            'hints': self._generate_hints(lesson_topic),
            'solution': self._generate_solution(lesson_topic),
            'estimated_time': self._estimate_time(difficulty)
        }
        
        return exercise_data
    
    def _load_exercise_templates(self) -> Dict:
        """Charge les templates d'exercices"""
        return {
            'html': {
                'easy': [
                    "Créez une page HTML avec un titre et un paragraphe",
                    "Ajoutez une liste à puces avec 3 éléments",
                    "Insérez une image avec un texte alternatif"
                ],
                'medium': [
                    "Créez un formulaire de contact avec validation",
                    "Structurez une page avec header, main et footer",
                    "Créez une table de données responsive"
                ],
                'hard': [
                    "Implémentez une navigation complexe avec sous-menus",
                    "Créez un layout adaptatif avec CSS Grid",
                    "Développez un composant interactif"
                ]
            },
            'css': {
                'easy': [
                    "Stylisez un titre avec couleur et police",
                    "Créez des boutons avec hover effects",
                    "Appliquez des marges et padding"
                ],
                'medium': [
                    "Créez un layout Flexbox responsive",
                    "Implémentez des animations CSS",
                    "Stylisez un formulaire complet"
                ],
                'hard': [
                    "Créez un thème sombre/clair avec CSS variables",
                    "Implémentez des micro-interactions",
                    "Développez un système de grille personnalisé"
                ]
            },
            'python': {
                'easy': [
                    "Créez une fonction qui calcule la somme de deux nombres",
                    "Affichez les nombres pairs de 1 à 20",
                    "Demandez le nom de l'utilisateur et saluez-le"
                ],
                'medium': [
                    "Créez un jeu de devinettes de nombres",
                    "Implémentez un calculateur simple",
                    "Analysez un fichier texte"
                ],
                'hard': [
                    "Créez un gestionnaire de tâches en ligne de commande",
                    "Implémentez un web scraper simple",
                    "Développez une API REST basique"
                ]
            }
        }
    
    def _generate_description(self, topic: str, difficulty: str) -> str:
        """Génère une description d'exercice"""
        descriptions = {
            'html': f"Cet exercice {difficulty} vous permettra de pratiquer les concepts HTML fondamentaux.",
            'css': f"Appliquez vos connaissances CSS dans cet exercice de niveau {difficulty}.",
            'python': f"Défi Python {difficulty} pour renforcer votre logique de programmation."
        }
        
        topic_key = topic.lower()
        return descriptions.get(topic_key, f"Exercice pratique {difficulty} pour {topic}")
    
    def _generate_tasks(self, topic: str, difficulty: str) -> List[str]:
        """Génère les tâches de l'exercice"""
        topic_key = topic.lower()
        if topic_key in self.exercise_templates and difficulty in self.exercise_templates[topic_key]:
            return random.sample(self.exercise_templates[topic_key][difficulty], 2)
        
        return [f"Tâche 1 pour {topic}", f"Tâche 2 pour {topic}"]
    
    def _generate_hints(self, topic: str) -> List[str]:
        """Génère des indices pour l'exercice"""
        hints = {
            'html': ["Utilisez la documentation MDN", "Testez votre code dans le navigateur"],
            'css': ["Inspectez les éléments pour déboguer", "Utilisez les DevTools"],
            'python': ["Testez votre code étape par étape", "Utilisez print() pour déboguer"]
        }
        
        topic_key = topic.lower()
        return hints.get(topic_key, ["Prenez votre temps", "N'hésitez pas à expérimenter"])
    
    def _generate_solution(self, topic: str) -> str:
        """Génère un exemple de solution"""
        return f"Solution type pour {topic} (à développer selon l'exercice spécifique)"
    
    def _estimate_time(self, difficulty: str) -> int:
        """Estime le temps nécessaire en minutes"""
        time_estimates = {
            'easy': 15,
            'medium': 30,
            'hard': 60
        }
        return time_estimates.get(difficulty, 30)

class Chatbot:
    """Chatbot d'aide 24/7"""
    
    def __init__(self):
        self.responses = self._load_responses()
        self.context_memory = {}
        
    def process_message(self, user_id: int, message: str, context: str = None) -> Dict:
        """Traite un message utilisateur et génère une réponse"""
        
        # Nettoyer et analyser le message
        message_lower = message.lower().strip()
        
        # Détecter l'intention
        intent = self._detect_intent(message_lower)
        
        # Générer la réponse
        response = self._generate_response(intent, message_lower, context)
        
        # Mémoriser le contexte
        self.context_memory[user_id] = {
            'last_intent': intent,
            'last_message': message,
            'timestamp': datetime.utcnow()
        }
        
        return {
            'response': response,
            'intent': intent,
            'suggestions': self._get_suggestions(intent),
            'helpful_links': self._get_helpful_links(intent)
        }
    
    def _load_responses(self) -> Dict:
        """Charge les réponses prédéfinies"""
        return {
            'greeting': [
                "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
                "Salut ! Je suis là pour répondre à vos questions sur les cours.",
                "Hello ! Que voulez-vous apprendre aujourd'hui ?"
            ],
            'course_info': [
                "Nos cours couvrent HTML, CSS, Python, C et Shell/Terminal. Lequel vous intéresse ?",
                "Chaque cours contient 5 leçons progressives avec des exercices pratiques.",
                "Vous pouvez commencer par n'importe quel cours selon vos objectifs."
            ],
            'technical_help': [
                "Pour les problèmes techniques, vérifiez d'abord votre connexion internet.",
                "Essayez de rafraîchir la page ou de vider le cache de votre navigateur.",
                "Si le problème persiste, contactez le support technique."
            ],
            'motivation': [
                "L'apprentissage prend du temps, soyez patient avec vous-même !",
                "Chaque petite victoire compte. Continuez à progresser !",
                "Vous faites déjà un excellent travail en étant ici !"
            ],
            'default': [
                "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?",
                "Intéressant ! Pouvez-vous me donner plus de détails ?",
                "Je vais faire de mon mieux pour vous aider. Précisez votre question."
            ]
        }
    
    def _detect_intent(self, message: str) -> str:
        """Détecte l'intention du message"""
        
        greetings = ['bonjour', 'salut', 'hello', 'hi', 'bonsoir']
        course_keywords = ['cours', 'leçon', 'apprendre', 'étudier', 'html', 'css', 'python']
        technical_keywords = ['bug', 'erreur', 'problème', 'marche pas', 'fonctionne pas']
        motivation_keywords = ['difficile', 'compliqué', 'découragement', 'motivation', 'abandonner']
        
        if any(word in message for word in greetings):
            return 'greeting'
        elif any(word in message for word in course_keywords):
            return 'course_info'
        elif any(word in message for word in technical_keywords):
            return 'technical_help'
        elif any(word in message for word in motivation_keywords):
            return 'motivation'
        else:
            return 'default'
    
    def _generate_response(self, intent: str, message: str, context: str = None) -> str:
        """Génère une réponse basée sur l'intention"""
        
        if intent in self.responses:
            base_response = random.choice(self.responses[intent])
            
            # Personnaliser selon le contexte
            if context and intent == 'course_info':
                base_response += f" Vous semblez être dans le cours {context}."
            
            return base_response
        
        return random.choice(self.responses['default'])
    
    def _get_suggestions(self, intent: str) -> List[str]:
        """Retourne des suggestions de questions"""
        suggestions = {
            'greeting': [
                "Comment commencer un cours ?",
                "Quels sont les prérequis ?",
                "Comment gagner des points ?"
            ],
            'course_info': [
                "Quel cours me recommandez-vous ?",
                "Combien de temps dure un cours ?",
                "Y a-t-il des certificats ?"
            ],
            'technical_help': [
                "Comment signaler un bug ?",
                "Problème de connexion",
                "Page qui ne charge pas"
            ]
        }
        
        return suggestions.get(intent, [
            "Comment puis-je vous aider ?",
            "Avez-vous d'autres questions ?",
            "Voulez-vous explorer un cours ?"
        ])
    
    def _get_helpful_links(self, intent: str) -> List[Dict]:
        """Retourne des liens utiles"""
        links = {
            'course_info': [
                {'title': 'Guide de démarrage', 'url': '/dashboard'},
                {'title': 'Liste des cours', 'url': '/'},
                {'title': 'Système de points', 'url': '/trophies'}
            ],
            'technical_help': [
                {'title': 'Support technique', 'url': '/support'},
                {'title': 'FAQ', 'url': '/faq'},
                {'title': 'Contact', 'url': '/contact'}
            ]
        }
        
        return links.get(intent, [
            {'title': 'Accueil', 'url': '/'},
            {'title': 'Dashboard', 'url': '/dashboard'}
        ])

# Instance globales des modules IA
recommendation_engine = AIRecommendationEngine()
ai_assistant = AIAssistant()
difficulty_detector = DifficultyDetector()
content_generator = ContentGenerator()
chatbot = Chatbot()
