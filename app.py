from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-learning-hub-secret-key-2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_learning_hub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Filtre Jinja pour les retours à la ligne
@app.template_filter('nl2br')
def nl2br_filter(text):
    return text.replace('\n', '<br>\n')

# Modèles de base de données
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    completed_lessons = db.relationship('CompletedLesson', backref='user', lazy=True)
    user_trophies = db.relationship('UserTrophy', backref='user', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    
    # Relations
    lessons = db.relationship('Lesson', backref='course', lazy=True, order_by='Lesson.order')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Relations
    completed_by = db.relationship('CompletedLesson', backref='lesson', lazy=True)

class CompletedLesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class Trophy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50), nullable=False)
    tier = db.Column(db.String(20), nullable=False)  # bronze, silver, gold, platinum
    condition_type = db.Column(db.String(50), nullable=False)  # points, lessons, courses
    condition_value = db.Column(db.Integer, nullable=False)
    
    # Relations
    earned_by = db.relationship('UserTrophy', backref='trophy', lazy=True)

class UserTrophy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trophy_id = db.Column(db.Integer, db.ForeignKey('trophy.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes principales
@app.route('/')
def index():
    courses = Course.query.all()
    return render_template('index.html', courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà')
            return render_template('register.html')
        
        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Compte créé avec succès!')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    courses = Course.query.all()
    completed_lessons = CompletedLesson.query.filter_by(user_id=current_user.id).all()
    user_trophies = UserTrophy.query.filter_by(user_id=current_user.id).all()
    
    # Calculer les statistiques
    total_lessons = Lesson.query.count()
    completed_count = len(completed_lessons)
    progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    return render_template('dashboard.html', 
                         courses=courses, 
                         completed_lessons=completed_lessons,
                         user_trophies=user_trophies,
                         progress_percentage=progress_percentage)

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    completed_lesson_ids = [cl.lesson_id for cl in CompletedLesson.query.filter_by(user_id=current_user.id).all()]
    return render_template('course_detail.html', course=course, completed_lesson_ids=completed_lesson_ids)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    is_completed = CompletedLesson.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    return render_template('lesson_detail.html', lesson=lesson, is_completed=is_completed)

@app.route('/complete_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Vérifier si déjà complété
    existing = CompletedLesson.query.filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Leçon déjà complétée'})
    
    # Marquer comme complété
    completed = CompletedLesson(user_id=current_user.id, lesson_id=lesson_id)
    db.session.add(completed)
    
    # Ajouter des points
    current_user.points += 10
    current_user.level = (current_user.points // 100) + 1
    
    db.session.commit()
    
    # Vérifier les trophées
    check_trophies(current_user.id)
    
    return jsonify({'success': True, 'points': current_user.points, 'level': current_user.level})

@app.route('/trophies')
@login_required
def trophies():
    all_trophies = Trophy.query.all()
    user_trophy_ids = [ut.trophy_id for ut in UserTrophy.query.filter_by(user_id=current_user.id).all()]
    return render_template('trophies.html', trophies=all_trophies, user_trophy_ids=user_trophy_ids)

# ============== ROUTES IA ==============

@app.route('/api/recommendations')
@login_required
def get_recommendations():
    """API pour obtenir des recommandations personnalisées"""
    # Version simplifiée
    mock_recommendations = [
        {
            'course_id': 1,
            'course_name': 'JavaScript Avancé',
            'course_description': 'Développement web moderne avec JavaScript',
            'course_icon': 'fab fa-js',
            'course_color': '#f7df1e',
            'score': 85,
            'reason': 'Basé sur votre progression en HTML5 et CSS3'
        },
        {
            'course_id': 2,
            'course_name': 'Python Data Science',
            'course_description': 'Analyse de données avec Python',
            'course_icon': 'fab fa-python',
            'course_color': '#3776ab',
            'score': 78,
            'reason': 'Excellent pour étendre vos compétences en programmation'
        }
    ]
    
    return jsonify({
        'success': True,
        'recommendations': mock_recommendations
    })

@app.route('/api/ai-help')
@login_required
def get_ai_help():
    """API pour obtenir de l'aide IA contextuelle"""
    lesson_id = request.args.get('lesson_id')
    question = request.args.get('question', '')
    
    if not lesson_id:
        return jsonify({'success': False, 'error': 'lesson_id required'})
    
    # Aide factice pour le moment
    help_responses = [
        "Voici une explication détaillée du concept...",
        "Pour mieux comprendre, voici un exemple pratique...",
        "Les points clés à retenir sont...",
        "Cette notion est importante car...",
    ]
    
    response = random.choice(help_responses)
    
    return jsonify({
        'success': True,
        'help': {
            'response': response,
            'examples': ['Exemple 1', 'Exemple 2'],
            'tips': ['Conseil 1', 'Conseil 2']
        }
    })

@app.route('/api/difficulty-analysis')
@login_required
def get_difficulty_analysis():
    """API pour l'analyse des difficultés d'apprentissage"""
    # Analyse factice basée sur les leçons complétées
    completed_count = CompletedLesson.query.filter_by(user_id=current_user.id).count()
    
    if completed_count > 10:
        level = 'advanced'
        strengths = ['Persévérance', 'Logique', 'Rapidité d\'apprentissage']
        improvements = ['Approfondissement', 'Projets pratiques']
    elif completed_count > 5:
        level = 'intermediate'
        strengths = ['Bases solides', 'Régularité']
        improvements = ['Pratique', 'Concepts avancés']
    else:
        level = 'beginner'
        strengths = ['Motivation', 'Curiosité']
        improvements = ['Pratique régulière', 'Consolidation des bases']
    
    analysis = {
        'overall_level': level,
        'strengths': strengths,
        'improvements': improvements,
        'recommendations': [
            f'Continuez à pratiquer pour atteindre le niveau suivant',
            f'Concentrez-vous sur : {", ".join(improvements)}',
            f'Vos forces sont : {", ".join(strengths)}'
        ]
    }
    
    return jsonify({
        'success': True,
        'analysis': analysis
    })

@app.route('/api/generate-exercise')
@login_required
def generate_exercise():
    """API pour générer un exercice personnalisé"""
    lesson_id = request.args.get('lesson_id')
    difficulty = request.args.get('difficulty', 'medium')
    
    if not lesson_id:
        return jsonify({'success': False, 'error': 'lesson_id required'})
    
    # Exercices factices selon la difficulté
    exercises = {
        'easy': {
            'content': 'Exercice Facile:\n\nCréez une page HTML simple avec:\n- Un titre h1\n- Un paragraphe\n- Une liste de 3 éléments\n\nBon courage !',
            'solution': '<!DOCTYPE html>\n<html>\n<head>\n  <title>Ma page</title>\n</head>\n<body>\n  <h1>Titre</h1>\n  <p>Paragraphe</p>\n  <ul>\n    <li>Item 1</li>\n    <li>Item 2</li>\n    <li>Item 3</li>\n  </ul>\n</body>\n</html>'
        },
        'medium': {
            'content': 'Exercice Moyen:\n\nCréez une fonction qui:\n- Prend un tableau en paramètre\n- Retourne la somme des nombres pairs\n- Gère les cas d\'erreur\n\nTestez avec [1,2,3,4,5,6]',
            'solution': 'function sumEvenNumbers(arr) {\n  if (!Array.isArray(arr)) return 0;\n  return arr.filter(n => n % 2 === 0).reduce((sum, n) => sum + n, 0);\n}\n\nconsole.log(sumEvenNumbers([1,2,3,4,5,6])); // 12'
        },
        'hard': {
            'content': 'Exercice Difficile:\n\nImplémentez un algorithme de tri fusion (merge sort):\n- Fonction récursive\n- Complexité O(n log n)\n- Triez [64, 34, 25, 12, 22, 11, 90]\n\nBonus: Expliquez la complexité',
            'solution': 'def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    \n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    \n    return merge(left, right)\n\ndef merge(left, right):\n    result = []\n    i = j = 0\n    \n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            result.append(left[i])\n            i += 1\n        else:\n            result.append(right[j])\n            j += 1\n    \n    result.extend(left[i:])\n    result.extend(right[j:])\n    return result'
        }
    }
    
    exercise = exercises.get(difficulty, exercises['medium'])
    
    return jsonify({
        'success': True,
        'exercise': exercise
    })

@app.route('/api/chatbot', methods=['POST'])
@login_required
def chatbot_api():
    """API pour le chatbot d'aide"""
    data = request.get_json()
    message = data.get('message', '')
    context = data.get('context', '')
    
    if not message:
        return jsonify({'success': False, 'error': 'message required'})
    
    # Réponses de chatbot simples basées sur des mots-clés
    responses = {
        'html': "HTML est un langage de balisage pour structurer les pages web. Les balises principales incluent <html>, <head>, <body>, <h1>, <p>, etc.",
        'css': "CSS permet de styliser vos pages HTML. Vous pouvez définir des couleurs, polices, layout avec des sélecteurs et propriétés.",
        'python': "Python est un langage de programmation polyvalent. Commencez par apprendre les variables, les fonctions, les boucles et les conditions.",
        'javascript': "JavaScript rend vos pages web interactives. Vous pouvez manipuler le DOM, gérer les événements et créer des animations.",
        'shell': "Le terminal/shell vous permet d'interagir avec votre système via des commandes texte. Commandes de base: ls, cd, mkdir, cp, mv.",
        'aide': "Je suis là pour vous aider ! Posez-moi des questions sur HTML, CSS, JavaScript, Python ou le terminal.",
        'exercice': "Voulez-vous un exercice pratique ? Je peux générer des exercices adaptés à votre niveau dans différents domaines.",
        'conseils': "Mes conseils pour apprendre efficacement: pratiquez régulièrement, codez tous les jours, faites des projets personnels, et n'hésitez pas à poser des questions!"
    }
    
    # Trouver une réponse appropriée
    message_lower = message.lower()
    response = "Je ne suis pas sûr de comprendre votre question. Pouvez-vous être plus spécifique ? Ou posez-moi des questions sur HTML, CSS, JavaScript, Python ou le terminal."
    
    for keyword, answer in responses.items():
        if keyword in message_lower:
            response = answer
            break
    
    return jsonify({
        'success': True,
        'chatbot_response': {
            'response': response,
            'suggestions': [
                'Comment apprendre plus efficacement ?',
                'Générez-moi un exercice',
                'Expliquez-moi les bases du HTML',
                'Quels sont vos conseils ?'
            ]
        }
    })

@app.route('/ai-dashboard')
@login_required
def ai_dashboard():
    """Dashboard avec les fonctionnalités IA"""
    # Version simplifiée pour éviter les erreurs de contexte
    
    # Recommandations factices pour le moment
    mock_recommendations = [
        {
            'course': {'id': 1, 'name': 'Python Avancé', 'description': 'Programmation Python niveau expert', 'icon': 'fab fa-python', 'color': '#3776ab'},
            'score': 0.9,
            'reason': 'Basé sur votre progression en programmation'
        },
        {
            'course': {'id': 2, 'name': 'JavaScript', 'description': 'Développement web dynamique', 'icon': 'fab fa-js', 'color': '#f7df1e'},
            'score': 0.8,
            'reason': 'Complément parfait à vos compétences HTML/CSS'
        }
    ]
    
    # Analyse factice des difficultés
    mock_difficulty_analysis = {
        'overall_level': 'intermediate',
        'strengths': ['HTML5', 'CSS3', 'Logique'],
        'improvements': ['JavaScript', 'Algorithmique'],
        'recommendations': [
            'Pratiquez plus d\'exercices JavaScript',
            'Explorez les concepts d\'algorithmique',
            'Participez aux défis de code'
        ]
    }
    
    # Statistiques utilisateur
    courses = Course.query.all()
    completed_lessons = CompletedLesson.query.filter_by(user_id=current_user.id).all()
    user_trophies = UserTrophy.query.filter_by(user_id=current_user.id).all()
    
    total_lessons = Lesson.query.count()
    completed_count = len(completed_lessons)
    progress_percentage = (completed_count / total_lessons * 100) if total_lessons > 0 else 0
    
    return render_template('ai_dashboard.html', 
                         courses=courses,
                         completed_lessons=completed_lessons,
                         user_trophies=user_trophies,
                         progress_percentage=progress_percentage,
                         recommendations=mock_recommendations,
                         difficulty_analysis=mock_difficulty_analysis)

def get_user_completed_courses(user_id):
    """Obtient la liste des cours complétés par un utilisateur"""
    completed_courses = []
    courses = Course.query.all()
    
    for course in courses:
        total_lessons = len(course.lessons)
        completed_lessons = CompletedLesson.query.join(Lesson).filter(
            CompletedLesson.user_id == user_id,
            Lesson.course_id == course.id
        ).count()
        
        if total_lessons > 0 and completed_lessons == total_lessons:
            completed_courses.append(course.id)
    
    return completed_courses

def check_trophies(user_id):
    user = User.query.get(user_id)
    completed_lessons_count = CompletedLesson.query.filter_by(user_id=user_id).count()
    completed_courses = get_completed_courses_count(user_id)
    
    trophies_to_check = [
        (1, 'lessons', 1),      # Premier Pas
        (2, 'lessons', 10),     # Étudiant Assidu
        (3, 'points', 100),     # Collectionneur de Points
        (4, 'courses', 1),      # Maître du Code
        (5, 'courses', 3),      # Polyglotte
    ]
    
    for trophy_id, condition_type, condition_value in trophies_to_check:
        # Vérifier si l'utilisateur a déjà ce trophée
        existing = UserTrophy.query.filter_by(user_id=user_id, trophy_id=trophy_id).first()
        if existing:
            continue
            
        earned = False
        if condition_type == 'lessons' and completed_lessons_count >= condition_value:
            earned = True
        elif condition_type == 'points' and user.points >= condition_value:
            earned = True
        elif condition_type == 'courses' and completed_courses >= condition_value:
            earned = True
            
        if earned:
            user_trophy = UserTrophy(user_id=user_id, trophy_id=trophy_id)
            db.session.add(user_trophy)
    
    db.session.commit()

def get_completed_courses_count(user_id):
    courses = Course.query.all()
    completed_courses = 0
    
    for course in courses:
        total_lessons = len(course.lessons)
        completed_lessons = CompletedLesson.query.join(Lesson).filter(
            CompletedLesson.user_id == user_id,
            Lesson.course_id == course.id
        ).count()
        
        if total_lessons > 0 and completed_lessons == total_lessons:
            completed_courses += 1
    
    return completed_courses

def init_database():
    with app.app_context():
        db.create_all()
        
        # Créer les cours si ils n'existent pas
        if Course.query.count() == 0:
            courses_data = [
                {
                    'name': 'Shell/Terminal',
                    'description': 'Maîtrisez la ligne de commande et les outils système',
                    'icon': 'fas fa-terminal',
                    'color': '#00ff88'
                },
                {
                    'name': 'HTML5',
                    'description': 'Créez la structure de vos pages web',
                    'icon': 'fab fa-html5',
                    'color': '#ff6b35'
                },
                {
                    'name': 'CSS3',
                    'description': 'Stylisez et animez vos interfaces',
                    'icon': 'fab fa-css3-alt',
                    'color': '#00d4ff'
                },
                {
                    'name': 'Langage C',
                    'description': 'Apprenez les fondamentaux de la programmation',
                    'icon': 'fas fa-code',
                    'color': '#a8e6cf'
                },
                {
                    'name': 'Python',
                    'description': 'Découvrez le langage polyvalent du développement moderne',
                    'icon': 'fab fa-python',
                    'color': '#ffd93d'
                }
            ]
            
            for course_data in courses_data:
                course = Course(**course_data)
                db.session.add(course)
            
            db.session.commit()
            
            # Ajouter des leçons pour chaque cours
            courses = Course.query.all()
            for course in courses:
                if course.name == 'Shell/Terminal':
                    lessons = [
                        'Introduction au Terminal',
                        'Navigation dans les dossiers',
                        'Manipulation des fichiers',
                        'Variables d\'environnement',
                        'Scripts et automatisation'
                    ]
                elif course.name == 'HTML5':
                    lessons = [
                        'Structure HTML de base',
                        'Éléments et attributs',
                        'Formulaires HTML',
                        'Sémantique HTML5',
                        'Intégration multimédia'
                    ]
                elif course.name == 'CSS3':
                    lessons = [
                        'Sélecteurs CSS',
                        'Mise en page avec Flexbox',
                        'Animations et transitions',
                        'Variables CSS',
                        'Design responsive'
                    ]
                elif course.name == 'Langage C':
                    lessons = [
                        'Variables et types de données',
                        'Structures de contrôle',
                        'Fonctions et pointeurs',
                        'Gestion de la mémoire',
                        'Structures et fichiers'
                    ]
                elif course.name == 'Python':
                    lessons = [
                        'Variables et types Python',
                        'Structures de données',
                        'Fonctions et modules',
                        'Programmation orientée objet',
                        'Gestion des erreurs'
                    ]
                
                for i, lesson_title in enumerate(lessons, 1):
                    lesson = Lesson(
                        title=lesson_title,
                        content=f"Contenu de la leçon: {lesson_title}. Cette leçon couvre les concepts fondamentaux et les pratiques essentielles.",
                        order=i,
                        course_id=course.id
                    )
                    db.session.add(lesson)
            
            db.session.commit()
        
        # Créer les trophées si ils n'existent pas
        if Trophy.query.count() == 0:
            trophies_data = [
                {
                    'name': 'Premier Pas',
                    'description': 'Complétez votre première leçon',
                    'icon': 'fas fa-baby',
                    'tier': 'bronze',
                    'condition_type': 'lessons',
                    'condition_value': 1
                },
                {
                    'name': 'Étudiant Assidu',
                    'description': 'Complétez 10 leçons',
                    'icon': 'fas fa-graduation-cap',
                    'tier': 'bronze',
                    'condition_type': 'lessons',
                    'condition_value': 10
                },
                {
                    'name': 'Collectionneur de Points',
                    'description': 'Gagnez 100 points',
                    'icon': 'fas fa-coins',
                    'tier': 'silver',
                    'condition_type': 'points',
                    'condition_value': 100
                },
                {
                    'name': 'Maître du Code',
                    'description': 'Complétez votre premier cours',
                    'icon': 'fas fa-crown',
                    'tier': 'silver',
                    'condition_type': 'courses',
                    'condition_value': 1
                },
                {
                    'name': 'Polyglotte',
                    'description': 'Complétez 3 cours différents',
                    'icon': 'fas fa-language',
                    'tier': 'gold',
                    'condition_type': 'courses',
                    'condition_value': 3
                }
            ]
            
            for trophy_data in trophies_data:
                trophy = Trophy(**trophy_data)
                db.session.add(trophy)
            
            db.session.commit()

# Nouvelles routes pour les fonctionnalités avancées

@app.route('/course/<int:course_id>/quiz')
@login_required
def course_quiz(course_id):
    """Page de quiz pour un cours"""
    course = Course.query.get_or_404(course_id)
    return render_template('quiz.html', course=course)

@app.route('/course/<int:course_id>/exercises')
@login_required
def course_exercises(course_id):
    """Page d'exercices pour un cours"""
    course = Course.query.get_or_404(course_id)
    return render_template('exercises.html', course=course)

@app.route('/api/quiz/<int:course_id>')
@login_required
def api_quiz_questions(course_id):
    """API pour récupérer les questions de quiz"""
    course = Course.query.get_or_404(course_id)
    
    # Questions générées dynamiquement basées sur le cours
    questions = generate_quiz_questions(course)
    
    return jsonify({
        'success': True,
        'questions': questions
    })

@app.route('/api/exercises/<int:course_id>')
@login_required
def api_exercises(course_id):
    """API pour récupérer les exercices"""
    course = Course.query.get_or_404(course_id)
    
    # Exercices générés dynamiquement basés sur le cours
    exercises = generate_exercises(course)
    
    return jsonify({
        'success': True,
        'exercises': exercises
    })

@app.route('/api/quiz/results', methods=['POST'])
@login_required
def api_quiz_results():
    """Sauvegarder les résultats de quiz"""
    data = request.get_json()
    
    # Ici vous pourriez sauvegarder en base de données
    # Pour l'instant, on retourne juste un succès
    
    return jsonify({
        'success': True,
        'message': 'Résultats sauvegardés'
    })

@app.route('/certificate/<int:course_id>')
@login_required
def course_certificate(course_id):
    """Afficher le certificat de réussite d'un cours"""
    course = Course.query.get_or_404(course_id)
    
    # Vérifier que l'utilisateur a terminé le cours
    completed_lessons = CompletedLesson.query.filter_by(user_id=current_user.id).all()
    completed_lesson_ids = [cl.lesson_id for cl in completed_lessons]
    course_lesson_ids = [lesson.id for lesson in course.lessons]
    
    # Vérifier si toutes les leçons du cours sont terminées
    all_completed = all(lesson_id in completed_lesson_ids for lesson_id in course_lesson_ids)
    
    if not all_completed:
        flash('Vous devez terminer toutes les leçons du cours pour obtenir votre certificat.', 'warning')
        return redirect(url_for('course_detail', course_id=course_id))
    
    # Calculer les statistiques de réussite
    completion_stats = {
        'lessons_completed': len(course_lesson_ids),
        'quiz_score': 85,  # Score simulé - à implémenter avec de vraies données
        'total_points': len(course_lesson_ids) * 10
    }
    
    # Date de completion (simulée)
    from datetime import datetime
    completion_date = datetime.now()
    
    return render_template('certificate.html', 
                         course=course, 
                         completion_stats=completion_stats,
                         completion_date=completion_date)

@app.route('/learning-paths')
def learning_paths():
    """Page des parcours d'apprentissage"""
    return render_template('learning_paths.html')

def generate_quiz_questions(course):
    """Générer des questions de quiz basées sur le cours"""
    
    # Questions personnalisées par technologie
    questions_by_tech = {
        'HTML': [
            {
                'id': 1,
                'text': 'Quelle balise HTML est utilisée pour créer un lien hypertexte ?',
                'type': 'multiple_choice',
                'difficulty': 'facile',
                'options': ['<link>', '<a>', '<href>', '<url>'],
                'correct_answer': 1,
                'hint': 'Cette balise commence par la première lettre de l\'alphabet.'
            },
            {
                'id': 2,
                'text': 'Comment définit-on un titre de niveau 1 en HTML ?',
                'type': 'multiple_choice',
                'difficulty': 'facile',
                'options': ['<title>', '<h1>', '<header>', '<heading>'],
                'correct_answer': 1,
                'hint': 'H pour Heading, 1 pour le niveau.'
            }
        ],
        'CSS': [
            {
                'id': 1,
                'text': 'Quelle propriété CSS est utilisée pour changer la couleur du texte ?',
                'type': 'multiple_choice',
                'difficulty': 'facile',
                'options': ['text-color', 'font-color', 'color', 'text-style'],
                'correct_answer': 2,
                'hint': 'C\'est le mot anglais le plus simple pour couleur.'
            }
        ],
        'JavaScript ES6+': [
            {
                'id': 1,
                'text': 'Quelle est la différence entre let et var ?',
                'type': 'multiple_choice',
                'difficulty': 'moyen',
                'options': [
                    'Aucune différence',
                    'let a une portée de bloc, var a une portée de fonction',
                    'var est plus moderne que let',
                    'let ne peut pas être redéclaré'
                ],
                'correct_answer': 1,
                'hint': 'Pensez à la portée (scope) des variables.'
            }
        ],
        'React.js': [
            {
                'id': 1,
                'text': 'Qu\'est-ce que JSX ?',
                'type': 'multiple_choice',
                'difficulty': 'moyen',
                'options': [
                    'Un nouveau langage de programmation',
                    'Une extension de syntaxe JavaScript',
                    'Un framework CSS',
                    'Une base de données'
                ],
                'correct_answer': 1,
                'hint': 'JSX = JavaScript eXtension'
            }
        ]
    }
    
    # Retourner les questions correspondant au cours ou des questions génériques
    course_name = course.name
    if course_name in questions_by_tech:
        return questions_by_tech[course_name]
    else:
        # Questions génériques
        return [
            {
                'id': 1,
                'text': f'Quelle est la principale utilisation de {course_name} ?',
                'type': 'multiple_choice',
                'difficulty': 'facile',
                'options': [
                    'Développement web frontend',
                    'Développement web backend',
                    'Développement mobile',
                    'Analyse de données'
                ],
                'correct_answer': 0,
                'hint': 'Consultez la description du cours pour un indice.'
            }
        ]

def generate_exercises(course):
    """Générer des exercices basés sur le cours"""
    
    exercises_by_tech = {
        'JavaScript ES6+': [
            {
                'id': 1,
                'title': 'Variables ES6',
                'description': 'Utilisez let et const pour déclarer des variables.',
                'difficulty': 'Facile',
                'points': 10,
                'starterCode': '// Déclarez une variable constante \'PI\' avec la valeur 3.14159\n// Déclarez une variable \'rayon\' avec let et assignez-lui 5\n\n',
                'expectedOutput': 'PI: 3.14159\nRayon: 5',
                'hints': [
                    'Utilisez const pour les valeurs qui ne changent pas',
                    'Utilisez let pour les variables qui peuvent changer',
                    'N\'oubliez pas console.log pour afficher les valeurs'
                ]
            }
        ],
        'React.js': [
            {
                'id': 1,
                'title': 'Premier Composant',
                'description': 'Créez un composant React qui affiche un message de bienvenue.',
                'difficulty': 'Facile',
                'points': 15,
                'starterCode': '// Créez un composant fonctionnel Welcome qui affiche "Bienvenue sur mon site!"\n\n',
                'expectedOutput': 'Bienvenue sur mon site!',
                'hints': [
                    'Utilisez function ou const avec une arrow function',
                    'Retournez du JSX',
                    'N\'oubliez pas les parenthèses pour le JSX multilignes'
                ]
            }
        ]
    }
    
    course_name = course.name
    if course_name in exercises_by_tech:
        return exercises_by_tech[course_name]
    else:
        # Exercices génériques
        return [
            {
                'id': 1,
                'title': f'Introduction à {course_name}',
                'description': f'Créez votre premier exemple avec {course_name}.',
                'difficulty': 'Facile',
                'points': 10,
                'starterCode': f'// Votre code {course_name} ici\n\n',
                'expectedOutput': 'Hello World!',
                'hints': [
                    'Commencez simple',
                    'Consultez la documentation',
                    'Testez étape par étape'
                ]
            }
        ]

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
