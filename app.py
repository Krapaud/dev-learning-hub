from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

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

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
