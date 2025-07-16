from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev_learning_hub.db'

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configuration SQLAlchemy
engine = create_engine('sqlite:///dev_learning_hub.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Modèles de base de données
class User(UserMixin, Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password_hash = Column(String(120), nullable=False)
    total_points = Column(Integer, default=0)
    level = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    progress = relationship("UserProgress", back_populates="user")
    trophies = relationship("UserTrophy", back_populates="user")

class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(10))
    color = Column(String(7))
    difficulty = Column(String(20))
    
    # Relations
    lessons = relationship("Lesson", back_populates="course")

class Lesson(Base):
    __tablename__ = 'lessons'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    order = Column(Integer, nullable=False)
    points_reward = Column(Integer, default=10)
    
    # Relations
    course = relationship("Course", back_populates="lessons")

class UserProgress(Base):
    __tablename__ = 'user_progress'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="progress")

class Trophy(Base):
    __tablename__ = 'trophies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    icon = Column(String(10))
    requirement_type = Column(String(50))  # points, courses_completed, lessons_completed
    requirement_value = Column(Integer)
    rarity = Column(String(20))  # bronze, silver, gold, platinum

class UserTrophy(Base):
    __tablename__ = 'user_trophies'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trophy_id = Column(Integer, ForeignKey('trophies.id'), nullable=False)
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="trophies")
    trophy = relationship("Trophy")

@login_manager.user_loader
def load_user(user_id):
    return session.get(User, int(user_id))

def init_db():
    """Initialise la base de données avec des données de démonstration"""
    Base.metadata.create_all(engine)
    
    # Vérifier si les données existent déjà
    if session.query(Course).count() > 0:
        return
    
    # Cours
    courses_data = [
        {
            'name': 'Shell/Terminal',
            'description': 'Maîtrisez la ligne de commande et les outils système',
            'icon': '💻',
            'color': '#00ff88',
            'difficulty': 'Débutant'
        },
        {
            'name': 'HTML5',
            'description': 'Créez la structure de vos pages web modernes',
            'icon': '🌐',
            'color': '#ff6b35',
            'difficulty': 'Débutant'
        },
        {
            'name': 'CSS3',
            'description': 'Stylisez et animez vos interfaces utilisateur',
            'icon': '🎨',
            'color': '#4285f4',
            'difficulty': 'Débutant'
        },
        {
            'name': 'Langage C',
            'description': 'Apprenez les fondamentaux de la programmation',
            'icon': '⚡',
            'color': '#a855f7',
            'difficulty': 'Intermédiaire'
        },
        {
            'name': 'Python',
            'description': 'Découvrez le langage polyvalent du développement moderne',
            'icon': '🐍',
            'color': '#fbbf24',
            'difficulty': 'Débutant'
        }
    ]
    
    # Ajouter les cours
    for course_data in courses_data:
        course = Course(**course_data)
        session.add(course)
    
    session.commit()
    
    # Leçons pour chaque cours
    lessons_data = {
        1: [  # Shell/Terminal
            {'title': 'Introduction au Terminal', 'content': 'Découvrez les bases du terminal et de la ligne de commande.', 'order': 1},
            {'title': 'Navigation dans le système', 'content': 'Apprenez à naviguer dans l\'arborescence des fichiers.', 'order': 2},
            {'title': 'Manipulation de fichiers', 'content': 'Créez, copiez, déplacez et supprimez des fichiers.', 'order': 3},
            {'title': 'Permissions et droits', 'content': 'Gérez les permissions des fichiers et dossiers.', 'order': 4},
            {'title': 'Scripts bash avancés', 'content': 'Créez vos premiers scripts automatisés.', 'order': 5},
        ],
        2: [  # HTML5
            {'title': 'Structure HTML de base', 'content': 'Apprenez la structure fondamentale d\'une page HTML.', 'order': 1},
            {'title': 'Balises sémantiques', 'content': 'Utilisez les balises HTML5 pour structurer votre contenu.', 'order': 2},
            {'title': 'Formulaires interactifs', 'content': 'Créez des formulaires avec validation.', 'order': 3},
            {'title': 'Multimédia et accessibilité', 'content': 'Intégrez images, vidéos et améliorez l\'accessibilité.', 'order': 4},
        ],
        3: [  # CSS3
            {'title': 'Sélecteurs et propriétés', 'content': 'Maîtrisez les sélecteurs CSS et leurs propriétés.', 'order': 1},
            {'title': 'Layout et Flexbox', 'content': 'Créez des mises en page avec Flexbox.', 'order': 2},
            {'title': 'CSS Grid', 'content': 'Maîtrisez le système de grille CSS.', 'order': 3},
            {'title': 'Animations et transitions', 'content': 'Ajoutez du mouvement à vos interfaces.', 'order': 4},
            {'title': 'Responsive Design', 'content': 'Adaptez vos designs à tous les écrans.', 'order': 5},
        ],
        4: [  # Langage C
            {'title': 'Syntaxe de base', 'content': 'Découvrez la syntaxe fondamentale du langage C.', 'order': 1},
            {'title': 'Variables et types', 'content': 'Apprenez à déclarer et utiliser les variables.', 'order': 2},
            {'title': 'Structures de contrôle', 'content': 'Maîtrisez les boucles et conditions.', 'order': 3},
            {'title': 'Fonctions', 'content': 'Créez et utilisez des fonctions.', 'order': 4},
            {'title': 'Pointeurs et mémoire', 'content': 'Comprenez la gestion de la mémoire.', 'order': 5},
        ],
        5: [  # Python
            {'title': 'Syntaxe Python', 'content': 'Découvrez la syntaxe claire et élégante de Python.', 'order': 1},
            {'title': 'Structures de données', 'content': 'Maîtrisez les listes, dictionnaires et tuples.', 'order': 2},
            {'title': 'Programmation orientée objet', 'content': 'Créez vos premières classes et objets.', 'order': 3},
            {'title': 'Modules et packages', 'content': 'Organisez votre code avec les modules.', 'order': 4},
            {'title': 'Gestion des erreurs', 'content': 'Gérez les exceptions et erreurs.', 'order': 5},
        ]
    }
    
    for course_id, lessons in lessons_data.items():
        for lesson_data in lessons:
            lesson = Lesson(course_id=course_id, **lesson_data)
            session.add(lesson)
    
    # Trophées
    trophies_data = [
        # Bronze
        {'name': 'Premier Pas', 'description': 'Complétez votre première leçon', 'icon': '🥉', 'requirement_type': 'lessons_completed', 'requirement_value': 1, 'rarity': 'bronze'},
        {'name': 'Étudiant Assidu', 'description': 'Complétez 10 leçons', 'icon': '📚', 'requirement_type': 'lessons_completed', 'requirement_value': 10, 'rarity': 'bronze'},
        # Argent
        {'name': 'Collectionneur de Points', 'description': 'Gagnez 100 points', 'icon': '🥈', 'requirement_type': 'points', 'requirement_value': 100, 'rarity': 'silver'},
        {'name': 'Maître du Code', 'description': 'Complétez votre premier cours', 'icon': '👨‍💻', 'requirement_type': 'courses_completed', 'requirement_value': 1, 'rarity': 'silver'},
        # Or
        {'name': 'Polyglotte', 'description': 'Complétez 3 cours différents', 'icon': '🥇', 'requirement_type': 'courses_completed', 'requirement_value': 3, 'rarity': 'gold'},
        # Platine
        {'name': 'Ninja du Terminal', 'description': 'Maîtrisez le Shell', 'icon': '💎', 'requirement_type': 'specific_course', 'requirement_value': 1, 'rarity': 'platinum'},
        {'name': 'Architecte Web', 'description': 'Terminez HTML + CSS', 'icon': '🏛️', 'requirement_type': 'web_master', 'requirement_value': 2, 'rarity': 'platinum'},
        {'name': 'Programmeur Confirmé', 'description': 'Terminez C + Python', 'icon': '🚀', 'requirement_type': 'programming_master', 'requirement_value': 2, 'rarity': 'platinum'},
    ]
    
    for trophy_data in trophies_data:
        trophy = Trophy(**trophy_data)
        session.add(trophy)
    
    session.commit()

def check_trophies(user):
    """Vérifie et attribue les nouveaux trophées à l'utilisateur"""
    # Récupérer les statistiques de l'utilisateur
    completed_lessons = session.query(UserProgress).filter_by(user_id=user.id, completed=True).count()
    completed_courses = len(get_completed_courses(user.id))
    
    # Récupérer les trophées déjà obtenus
    earned_trophy_ids = [ut.trophy_id for ut in user.trophies]
    
    # Vérifier chaque trophée
    all_trophies = session.query(Trophy).all()
    new_trophies = []
    
    for trophy in all_trophies:
        if trophy.id in earned_trophy_ids:
            continue
            
        earned = False
        
        if trophy.requirement_type == 'lessons_completed' and completed_lessons >= trophy.requirement_value:
            earned = True
        elif trophy.requirement_type == 'points' and user.total_points >= trophy.requirement_value:
            earned = True
        elif trophy.requirement_type == 'courses_completed' and completed_courses >= trophy.requirement_value:
            earned = True
        elif trophy.requirement_type == 'specific_course':
            # Vérifier si le cours spécifique est terminé (Shell = course_id 1)
            if is_course_completed(user.id, trophy.requirement_value):
                earned = True
        elif trophy.requirement_type == 'web_master':
            # HTML (2) + CSS (3)
            if is_course_completed(user.id, 2) and is_course_completed(user.id, 3):
                earned = True
        elif trophy.requirement_type == 'programming_master':
            # C (4) + Python (5)
            if is_course_completed(user.id, 4) and is_course_completed(user.id, 5):
                earned = True
        
        if earned:
            user_trophy = UserTrophy(user_id=user.id, trophy_id=trophy.id)
            session.add(user_trophy)
            new_trophies.append(trophy)
    
    if new_trophies:
        session.commit()
    
    return new_trophies

def get_completed_courses(user_id):
    """Retourne la liste des cours terminés par l'utilisateur"""
    completed_courses = []
    courses = session.query(Course).all()
    
    for course in courses:
        if is_course_completed(user_id, course.id):
            completed_courses.append(course)
    
    return completed_courses

def is_course_completed(user_id, course_id):
    """Vérifie si un cours est terminé"""
    total_lessons = session.query(Lesson).filter_by(course_id=course_id).count()
    completed_lessons = session.query(UserProgress).join(Lesson).filter(
        UserProgress.user_id == user_id,
        UserProgress.completed == True,
        Lesson.course_id == course_id
    ).count()
    
    return total_lessons > 0 and completed_lessons == total_lessons

def calculate_level(points):
    """Calcule le niveau basé sur les points"""
    return min(points // 100 + 1, 50)  # Niveau max 50

# Routes
@app.route('/')
def index():
    courses = session.query(Course).all()
    return render_template('index.html', courses=courses)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Vérifier si l'utilisateur existe déjà
        if session.query(User).filter_by(username=username).first():
            flash('Ce nom d\'utilisateur existe déjà!')
            return redirect(url_for('register'))
        
        # Créer le nouvel utilisateur
        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )
        session.add(user)
        session.commit()
        
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = session.query(User).filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect!')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Statistiques utilisateur
    completed_lessons = session.query(UserProgress).filter_by(user_id=current_user.id, completed=True).count()
    total_lessons = session.query(Lesson).count()
    completed_courses = get_completed_courses(current_user.id)
    
    # Mettre à jour le niveau
    current_user.level = calculate_level(current_user.total_points)
    session.commit()
    
    # Récupérer les cours avec progression
    courses = session.query(Course).all()
    courses_with_progress = []
    
    for course in courses:
        course_lessons = session.query(Lesson).filter_by(course_id=course.id).count()
        course_completed_lessons = session.query(UserProgress).join(Lesson).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.completed == True,
            Lesson.course_id == course.id
        ).count()
        
        progress_percentage = (course_completed_lessons / course_lessons * 100) if course_lessons > 0 else 0
        
        courses_with_progress.append({
            'course': course,
            'progress': progress_percentage,
            'completed_lessons': course_completed_lessons,
            'total_lessons': course_lessons
        })
    
    return render_template('dashboard.html', 
                         courses=courses_with_progress,
                         completed_lessons=completed_lessons,
                         total_lessons=total_lessons,
                         completed_courses=len(completed_courses))

@app.route('/course/<int:course_id>')
@login_required
def course_detail(course_id):
    course = session.get(Course, course_id)
    if not course:
        flash('Cours introuvable!')
        return redirect(url_for('dashboard'))
    
    lessons = session.query(Lesson).filter_by(course_id=course_id).order_by(Lesson.order).all()
    
    # Récupérer la progression de l'utilisateur
    user_progress = {}
    for lesson in lessons:
        progress = session.query(UserProgress).filter_by(
            user_id=current_user.id, 
            lesson_id=lesson.id
        ).first()
        user_progress[lesson.id] = progress.completed if progress else False
    
    return render_template('course_detail.html', 
                         course=course, 
                         lessons=lessons, 
                         user_progress=user_progress)

@app.route('/lesson/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        flash('Leçon introuvable!')
        return redirect(url_for('dashboard'))
    
    # Vérifier la progression
    progress = session.query(UserProgress).filter_by(
        user_id=current_user.id, 
        lesson_id=lesson_id
    ).first()
    
    completed = progress.completed if progress else False
    
    return render_template('lesson_detail.html', lesson=lesson, completed=completed)

@app.route('/complete_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    lesson = session.get(Lesson, lesson_id)
    if not lesson:
        return jsonify({'success': False, 'message': 'Leçon introuvable'})
    
    # Vérifier si déjà complétée
    progress = session.query(UserProgress).filter_by(
        user_id=current_user.id, 
        lesson_id=lesson_id
    ).first()
    
    if progress and progress.completed:
        return jsonify({'success': False, 'message': 'Leçon déjà complétée'})
    
    # Marquer comme complétée
    if not progress:
        progress = UserProgress(user_id=current_user.id, lesson_id=lesson_id)
        session.add(progress)
    
    progress.completed = True
    progress.completed_at = datetime.utcnow()
    
    # Ajouter les points
    current_user.total_points += lesson.points_reward
    current_user.level = calculate_level(current_user.total_points)
    
    session.commit()
    
    # Vérifier les nouveaux trophées
    new_trophies = check_trophies(current_user)
    
    return jsonify({
        'success': True, 
        'points_earned': lesson.points_reward,
        'total_points': current_user.total_points,
        'new_level': current_user.level,
        'new_trophies': [{'name': t.name, 'icon': t.icon} for t in new_trophies]
    })

@app.route('/roadmap')
def roadmap():
    if not current_user.is_authenticated:
        # Version publique de la roadmap
        courses = session.query(Course).all()
        return render_template('roadmap.html', courses=courses)
    
    # Version personnalisée pour l'utilisateur connecté
    courses = session.query(Course).all()
    courses_status = {}
    
    # Calculer le statut de chaque cours
    for course in courses:
        course_lessons = session.query(Lesson).filter_by(course_id=course.id).count()
        course_completed_lessons = session.query(UserProgress).join(Lesson).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.completed == True,
            Lesson.course_id == course.id
        ).count()
        
        progress_percentage = (course_completed_lessons / course_lessons * 100) if course_lessons > 0 else 0
        
        courses_status[course.id] = {
            'progress': progress_percentage,
            'completed_lessons': course_completed_lessons,
            'total_lessons': course_lessons,
            'completed': progress_percentage == 100,
            'started': course_completed_lessons > 0
        }
    
    # Calculer les progressions par niveau
    beginner_courses = [1, 2, 3, 5]  # Shell, HTML, CSS, Python
    intermediate_courses = [4]  # C
    
    beginner_progress = sum(courses_status.get(cid, {}).get('progress', 0) for cid in beginner_courses) / len(beginner_courses)
    intermediate_progress = sum(courses_status.get(cid, {}).get('progress', 0) for cid in intermediate_courses) / len(intermediate_courses)
    
    # Vérifier si les niveaux sont complétés
    beginner_completed = all(courses_status.get(cid, {}).get('completed', False) for cid in beginner_courses)
    intermediate_completed = all(courses_status.get(cid, {}).get('completed', False) for cid in intermediate_courses)
    
    # Statistiques utilisateur
    completed_lessons = session.query(UserProgress).filter_by(user_id=current_user.id, completed=True).count()
    total_lessons = session.query(Lesson).count()
    completed_courses = sum(1 for status in courses_status.values() if status.get('completed', False))
    
    user_progress = {
        'completed_courses': completed_courses,
        'total_lessons_completed': completed_lessons,
        'overall_progress': (completed_lessons / total_lessons * 100) if total_lessons > 0 else 0
    }
    
    # Déterminer le prochain cours recommandé
    next_course = None
    if not courses_status.get(1, {}).get('completed', False):
        next_course = session.get(Course, 1)  # Shell
    elif not courses_status.get(2, {}).get('completed', False):
        next_course = session.get(Course, 2)  # HTML
    elif not courses_status.get(3, {}).get('completed', False):
        next_course = session.get(Course, 3)  # CSS
    elif not courses_status.get(5, {}).get('completed', False):
        next_course = session.get(Course, 5)  # Python
    elif beginner_completed and not courses_status.get(4, {}).get('completed', False):
        next_course = session.get(Course, 4)  # C
    
    return render_template('roadmap.html',
                         courses=courses,
                         courses_status=courses_status,
                         user_progress=user_progress,
                         beginner_progress=beginner_progress,
                         intermediate_progress=intermediate_progress,
                         beginner_completed=beginner_completed,
                         intermediate_completed=intermediate_completed,
                         next_course=next_course)

@app.route('/trophies')
@login_required
def trophies():
    # Récupérer tous les trophées
    all_trophies = session.query(Trophy).all()
    
    # Récupérer les trophées de l'utilisateur
    user_trophy_ids = [ut.trophy_id for ut in current_user.trophies]
    
    # Organiser par rareté
    trophies_by_rarity = {
        'bronze': [],
        'silver': [],
        'gold': [],
        'platinum': []
    }
    
    for trophy in all_trophies:
        trophy_data = {
            'trophy': trophy,
            'earned': trophy.id in user_trophy_ids,
            'earned_at': None
        }
        
        if trophy.id in user_trophy_ids:
            user_trophy = next(ut for ut in current_user.trophies if ut.trophy_id == trophy.id)
            trophy_data['earned_at'] = user_trophy.earned_at
        
        trophies_by_rarity[trophy.rarity].append(trophy_data)
    
    total_trophies = len(all_trophies)
    earned_trophies = len(user_trophy_ids)
    
    return render_template('trophies.html', 
                         trophies_by_rarity=trophies_by_rarity,
                         total_trophies=total_trophies,
                         earned_trophies=earned_trophies)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
