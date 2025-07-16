#!/usr/bin/env python3
"""
Script pour ajouter les nouveaux cours et fonctionnalités au Dev Learning Hub
"""

from app import app, db, Course, Lesson
from datetime import datetime

def add_new_courses():
    """Ajouter les nouveaux cours à la base de données"""
    
    with app.app_context():
        # Nouveaux cours modernes
        new_courses = [
            {
                'name': 'JavaScript ES6+',
                'description': 'Développement web moderne avec les dernières fonctionnalités JavaScript',
                'icon': 'fab fa-js-square',
                'color': '#f7df1e'
            },
            {
                'name': 'React.js',
                'description': 'Bibliothèque d\'interface utilisateur pour créer des applications web interactives',
                'icon': 'fab fa-react',
                'color': '#61dafb'
            },
            {
                'name': 'Node.js',
                'description': 'JavaScript côté serveur pour créer des applications backend performantes',
                'icon': 'fab fa-node-js',
                'color': '#68a063'
            },
            {
                'name': 'SQL/Bases de données',
                'description': 'Gestion et manipulation des données avec SQL et bases de données',
                'icon': 'fas fa-database',
                'color': '#336791'
            },
            {
                'name': 'Git/GitHub',
                'description': 'Contrôle de version et collaboration avec Git et GitHub',
                'icon': 'fab fa-git-alt',
                'color': '#f05032'
            },
            {
                'name': 'Docker',
                'description': 'Conteneurisation d\'applications pour un déploiement simplifié',
                'icon': 'fab fa-docker',
                'color': '#2496ed'
            },
            {
                'name': 'TypeScript',
                'description': 'JavaScript typé pour des applications plus robustes et maintenables',
                'icon': 'fas fa-code',
                'color': '#3178c6'
            },
            {
                'name': 'Vue.js',
                'description': 'Framework JavaScript progressif pour construire des interfaces utilisateur',
                'icon': 'fab fa-vuejs',
                'color': '#4fc08d'
            },
            {
                'name': 'Angular',
                'description': 'Framework web complet pour développer des applications modernes',
                'icon': 'fab fa-angular',
                'color': '#dd0031'
            },
            {
                'name': 'PHP/Laravel',
                'description': 'Développement web backend avec PHP et le framework Laravel',
                'icon': 'fab fa-php',
                'color': '#777bb4'
            }
        ]
        
        courses_added = 0
        
        for course_data in new_courses:
            # Vérifier si le cours existe déjà
            existing_course = Course.query.filter_by(name=course_data['name']).first()
            if not existing_course:
                course = Course(
                    name=course_data['name'],
                    description=course_data['description'],
                    icon=course_data['icon'],
                    color=course_data['color']
                )
                db.session.add(course)
                courses_added += 1
                print(f"✅ Cours ajouté: {course_data['name']}")
            else:
                print(f"ℹ️  Cours déjà existant: {course_data['name']}")
        
        if courses_added > 0:
            db.session.commit()
            print(f"\n🎉 {courses_added} nouveaux cours ajoutés avec succès!")
        else:
            print("\n📚 Tous les cours sont déjà présents dans la base de données.")

def add_sample_lessons_for_new_courses():
    """Ajouter des leçons d'exemple pour les nouveaux cours"""
    
    with app.app_context():
        # Définir des leçons pour chaque nouveau cours
        course_lessons = {
            'JavaScript ES6+': [
                {'title': 'Variables et portée (let, const)', 'content': 'Découvrez les nouvelles façons de déclarer des variables en ES6...', 'order': 1},
                {'title': 'Fonctions fléchées', 'content': 'Les arrow functions simplifient l\'écriture des fonctions...', 'order': 2},
                {'title': 'Destructuring et Spread', 'content': 'Techniques modernes pour manipuler les objets et tableaux...', 'order': 3},
                {'title': 'Modules ES6', 'content': 'Import/Export pour organiser votre code...', 'order': 4},
                {'title': 'Promises et Async/Await', 'content': 'Gérer l\'asynchrone de manière élégante...', 'order': 5}
            ],
            'React.js': [
                {'title': 'Introduction à React', 'content': 'Concepts fondamentaux et création du premier composant...', 'order': 1},
                {'title': 'JSX et rendu conditionnel', 'content': 'Syntaxe JSX et techniques de rendu dynamique...', 'order': 2},
                {'title': 'State et Props', 'content': 'Gestion de l\'état et communication entre composants...', 'order': 3},
                {'title': 'Hooks (useState, useEffect)', 'content': 'Hooks React pour la gestion d\'état moderne...', 'order': 4},
                {'title': 'Gestion des événements', 'content': 'Interactivité et gestion des événements utilisateur...', 'order': 5}
            ],
            'Node.js': [
                {'title': 'Introduction à Node.js', 'content': 'Comprendre l\'environnement d\'exécution JavaScript côté serveur...', 'order': 1},
                {'title': 'Modules et NPM', 'content': 'Système de modules et gestionnaire de paquets...', 'order': 2},
                {'title': 'Serveur HTTP basique', 'content': 'Créer votre premier serveur web avec Node.js...', 'order': 3},
                {'title': 'Express.js Framework', 'content': 'Framework web minimaliste pour Node.js...', 'order': 4},
                {'title': 'APIs REST', 'content': 'Créer des APIs RESTful avec Express...', 'order': 5}
            ],
            'Git/GitHub': [
                {'title': 'Concepts de base Git', 'content': 'Repository, commits, branches - les fondamentaux...', 'order': 1},
                {'title': 'Commandes essentielles', 'content': 'add, commit, push, pull, merge...', 'order': 2},
                {'title': 'Gestion des branches', 'content': 'Créer, fusionner et gérer les branches...', 'order': 3},
                {'title': 'GitHub et collaboration', 'content': 'Pull requests, issues, et travail en équipe...', 'order': 4},
                {'title': 'Bonnes pratiques', 'content': 'Workflow Git et conventions de commit...', 'order': 5}
            ]
        }
        
        lessons_added = 0
        
        for course_name, lessons in course_lessons.items():
            course = Course.query.filter_by(name=course_name).first()
            if course:
                for lesson_data in lessons:
                    # Vérifier si la leçon existe déjà
                    existing_lesson = Lesson.query.filter_by(
                        title=lesson_data['title'], 
                        course_id=course.id
                    ).first()
                    
                    if not existing_lesson:
                        lesson = Lesson(
                            title=lesson_data['title'],
                            content=lesson_data['content'],
                            order=lesson_data['order'],
                            course_id=course.id
                        )
                        db.session.add(lesson)
                        lessons_added += 1
                        print(f"📝 Leçon ajoutée: {lesson_data['title']} ({course_name})")
        
        if lessons_added > 0:
            db.session.commit()
            print(f"\n🎓 {lessons_added} nouvelles leçons ajoutées!")

if __name__ == '__main__':
    print("🚀 Ajout des nouveaux cours et fonctionnalités...")
    print("=" * 60)
    
    # Ajouter les cours
    add_new_courses()
    
    print("\n" + "=" * 60)
    print("📚 Ajout des leçons d'exemple...")
    
    # Ajouter des leçons d'exemple
    add_sample_lessons_for_new_courses()
    
    print("\n" + "=" * 60)
    print("✨ Processus terminé! Vos nouveaux cours sont maintenant disponibles.")
