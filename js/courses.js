// Système de cours complet
class CourseSystem {
    constructor() {
        this.courses = this.initializeCourses();
        this.currentCourse = null;
        this.currentLesson = null;
    }

    initializeCourses() {
        return {
            html: {
                id: 'html',
                title: 'HTML5',
                icon: 'fab fa-html5',
                color: '#e34c26',
                difficulty: 'debutant',
                description: 'Apprenez les bases du langage de balisage pour créer des pages web',
                duration: '15 leçons',
                students: '1,234',
                lessons: [
                    {
                        id: 1,
                        title: 'Introduction au HTML',
                        content: `
                            <h3>Qu'est-ce que le HTML ?</h3>
                            <p>HTML (HyperText Markup Language) est le langage de balisage standard pour créer des pages web. Il décrit la structure d'une page web à l'aide d'éléments.</p>
                            
                            <h3>Structure de base d'un document HTML</h3>
                            <pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="fr"&gt;
&lt;head&gt;
    &lt;meta charset="UTF-8"&gt;
    &lt;title&gt;Ma première page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;h1&gt;Bonjour le monde !&lt;/h1&gt;
    &lt;p&gt;Ceci est ma première page HTML.&lt;/p&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>
                            
                            <h3>Éléments HTML essentiels</h3>
                            <ul>
                                <li><code>&lt;!DOCTYPE html&gt;</code> : Déclare le type de document</li>
                                <li><code>&lt;html&gt;</code> : Élément racine</li>
                                <li><code>&lt;head&gt;</code> : Métadonnées de la page</li>
                                <li><code>&lt;body&gt;</code> : Contenu visible de la page</li>
                            </ul>
                        `
                    },
                    {
                        id: 2,
                        title: 'Les balises de titre',
                        content: `
                            <h3>Hiérarchie des titres</h3>
                            <p>HTML propose 6 niveaux de titres, de h1 à h6 :</p>
                            
                            <pre><code>&lt;h1&gt;Titre principal&lt;/h1&gt;
&lt;h2&gt;Sous-titre&lt;/h2&gt;
&lt;h3&gt;Sous-sous-titre&lt;/h3&gt;
&lt;h4&gt;Titre de niveau 4&lt;/h4&gt;
&lt;h5&gt;Titre de niveau 5&lt;/h5&gt;
&lt;h6&gt;Titre de niveau 6&lt;/h6&gt;</code></pre>
                            
                            <h3>Bonnes pratiques</h3>
                            <ul>
                                <li>Utilisez un seul h1 par page</li>
                                <li>Respectez la hiérarchie (h1 → h2 → h3...)</li>
                                <li>Les titres sont importants pour le SEO</li>
                            </ul>
                        `
                    },
                    {
                        id: 3,
                        title: 'Les paragraphes et le texte',
                        content: `
                            <h3>Balise paragraphe</h3>
                            <p>La balise <code>&lt;p&gt;</code> définit un paragraphe :</p>
                            
                            <pre><code>&lt;p&gt;Ceci est un paragraphe.&lt;/p&gt;
&lt;p&gt;Ceci est un autre paragraphe.&lt;/p&gt;</code></pre>
                            
                            <h3>Formatage du texte</h3>
                            <pre><code>&lt;strong&gt;Texte important&lt;/strong&gt;
&lt;em&gt;Texte en emphase&lt;/em&gt;
&lt;mark&gt;Texte surligné&lt;/mark&gt;
&lt;small&gt;Petit texte&lt;/small&gt;
&lt;del&gt;Texte supprimé&lt;/del&gt;
&lt;ins&gt;Texte inséré&lt;/ins&gt;</code></pre>
                            
                            <h3>Saut de ligne</h3>
                            <p>Utilisez <code>&lt;br&gt;</code> pour un saut de ligne simple.</p>
                        `
                    }
                ]
            },
            css: {
                id: 'css',
                title: 'CSS3',
                icon: 'fab fa-css3-alt',
                color: '#1572b6',
                difficulty: 'debutant',
                description: 'Maîtrisez les feuilles de style pour donner vie à vos pages web',
                duration: '20 leçons',
                students: '987',
                lessons: [
                    {
                        id: 1,
                        title: 'Introduction au CSS',
                        content: `
                            <h3>Qu'est-ce que le CSS ?</h3>
                            <p>CSS (Cascading Style Sheets) est un langage de feuilles de style utilisé pour décrire la présentation d'un document HTML.</p>
                            
                            <h3>Syntaxe de base</h3>
                            <pre><code>sélecteur {
    propriété: valeur;
    propriété: valeur;
}</code></pre>
                            
                            <h3>Exemple</h3>
                            <pre><code>h1 {
    color: blue;
    font-size: 24px;
    text-align: center;
}</code></pre>
                            
                            <h3>Trois façons d'ajouter du CSS</h3>
                            <ul>
                                <li><strong>Inline :</strong> <code>&lt;p style="color: red;"&gt;</code></li>
                                <li><strong>Interne :</strong> Dans une balise <code>&lt;style&gt;</code></li>
                                <li><strong>Externe :</strong> Fichier .css séparé</li>
                            </ul>
                        `
                    },
                    {
                        id: 2,
                        title: 'Les sélecteurs CSS',
                        content: `
                            <h3>Types de sélecteurs</h3>
                            
                            <h4>Sélecteur d'élément</h4>
                            <pre><code>p {
    color: black;
}</code></pre>
                            
                            <h4>Sélecteur de classe</h4>
                            <pre><code>.ma-classe {
    background-color: yellow;
}</code></pre>
                            
                            <h4>Sélecteur d'ID</h4>
                            <pre><code>#mon-id {
    font-weight: bold;
}</code></pre>
                            
                            <h4>Sélecteurs combinés</h4>
                            <pre><code>/* Descendant */
div p { color: blue; }

/* Enfant direct */
div > p { margin: 10px; }

/* Frère adjacent */
h1 + p { font-style: italic; }</code></pre>
                        `
                    }
                ]
            },
            c: {
                id: 'c',
                title: 'Langage C',
                icon: 'fas fa-code',
                color: '#659ad2',
                difficulty: 'intermediaire',
                description: 'Découvrez la programmation système avec le langage C',
                duration: '25 leçons',
                students: '756',
                lessons: [
                    {
                        id: 1,
                        title: 'Introduction au langage C',
                        content: `
                            <h3>Qu'est-ce que le langage C ?</h3>
                            <p>Le C est un langage de programmation impératif et généraliste, développé en 1972. Il est la base de nombreux langages modernes.</p>
                            
                            <h3>Votre premier programme</h3>
                            <pre><code>#include &lt;stdio.h&gt;

int main() {
    printf("Hello, World!\\n");
    return 0;
}</code></pre>
                            
                            <h3>Structure d'un programme C</h3>
                            <ul>
                                <li><code>#include</code> : Inclusion de bibliothèques</li>
                                <li><code>int main()</code> : Fonction principale</li>
                                <li><code>printf()</code> : Affichage à l'écran</li>
                                <li><code>return 0</code> : Fin du programme</li>
                            </ul>
                            
                            <h3>Compilation</h3>
                            <pre><code>gcc programme.c -o programme
./programme</code></pre>
                        `
                    },
                    {
                        id: 2,
                        title: 'Variables et types de données',
                        content: `
                            <h3>Types de données de base</h3>
                            <pre><code>int age = 25;           // Entier
float prix = 19.99;     // Nombre décimal
char lettre = 'A';      // Caractère
double pi = 3.14159;    // Double précision</code></pre>
                            
                            <h3>Déclaration et initialisation</h3>
                            <pre><code>// Déclaration
int nombre;

// Initialisation
nombre = 42;

// Déclaration + Initialisation
int autre_nombre = 100;</code></pre>
                            
                            <h3>Constantes</h3>
                            <pre><code>#define PI 3.14159
const int MAX_SIZE = 100;</code></pre>
                        `
                    }
                ]
            },
            python: {
                id: 'python',
                title: 'Python',
                icon: 'fab fa-python',
                color: '#3776ab',
                difficulty: 'debutant',
                description: 'Apprenez Python, le langage idéal pour débuter en programmation',
                duration: '30 leçons',
                students: '2,145',
                lessons: [
                    {
                        id: 1,
                        title: 'Introduction à Python',
                        content: `
                            <h3>Qu'est-ce que Python ?</h3>
                            <p>Python est un langage de programmation de haut niveau, interprété et polyvalent. Il est réputé pour sa simplicité et sa lisibilité.</p>
                            
                            <h3>Votre premier programme</h3>
                            <pre><code>print("Hello, World!")</code></pre>
                            
                            <h3>Avantages de Python</h3>
                            <ul>
                                <li>Syntaxe simple et claire</li>
                                <li>Grande communauté</li>
                                <li>Nombreuses bibliothèques</li>
                                <li>Multiplateforme</li>
                            </ul>
                            
                            <h3>Installation</h3>
                            <p>Téléchargez Python depuis <a href="https://python.org" target="_blank">python.org</a></p>
                            
                            <h3>REPL Python</h3>
                            <p>Vous pouvez tester du code directement dans l'interpréteur Python en tapant <code>python</code> dans votre terminal.</p>
                        `
                    },
                    {
                        id: 2,
                        title: 'Variables et types de données',
                        content: `
                            <h3>Variables en Python</h3>
                            <p>En Python, pas besoin de déclarer le type d'une variable :</p>
                            
                            <pre><code># Nombres
age = 25
prix = 19.99

# Chaînes de caractères
nom = "Alice"
message = 'Bonjour'

# Booléens
est_majeur = True
est_mineur = False</code></pre>
                            
                            <h3>Types de données</h3>
                            <pre><code># Vérifier le type
print(type(age))        # &lt;class 'int'&gt;
print(type(prix))       # &lt;class 'float'&gt;
print(type(nom))        # &lt;class 'str'&gt;
print(type(est_majeur)) # &lt;class 'bool'&gt;</code></pre>
                            
                            <h3>Conversion de types</h3>
                            <pre><code>age_str = "25"
age_int = int(age_str)

prix_str = str(19.99)
prix_float = float("19.99")</code></pre>
                        `
                    },
                    {
                        id: 3,
                        title: 'Les chaînes de caractères',
                        content: `
                            <h3>Création de chaînes</h3>
                            <pre><code>nom = "Python"
message = 'Apprentissage'
multiligne = """
Ceci est une chaîne
sur plusieurs lignes
"""</code></pre>
                            
                            <h3>Opérations sur les chaînes</h3>
                            <pre><code># Concaténation
salutation = "Bonjour " + nom

# Répétition
tirets = "-" * 20

# Longueur
longueur = len(nom)

# Méthodes utiles
nom_majuscule = nom.upper()
nom_minuscule = nom.lower()
mots = message.split(' ')</code></pre>
                            
                            <h3>Formatage de chaînes</h3>
                            <pre><code># f-strings (Python 3.6+)
age = 25
message = f"J'ai {age} ans"

# Format classique
message = "J'ai {} ans".format(age)</code></pre>
                        `
                    }
                ]
            }
        };
    }

    renderCourses() {
        const coursesGrid = document.getElementById('coursesGrid');
        if (!coursesGrid) return;

        coursesGrid.innerHTML = '';

        Object.values(this.courses).forEach(course => {
            const courseCard = this.createCourseCard(course);
            coursesGrid.appendChild(courseCard);
        });
    }

    createCourseCard(course) {
        const card = document.createElement('div');
        card.className = 'course-card';
        card.dataset.difficulty = course.difficulty;
        card.dataset.courseId = course.id;

        card.innerHTML = `
            <div class="course-header">
                <i class="${course.icon} course-icon" style="color: ${course.color}"></i>
                <h3 class="course-title">${course.title}</h3>
            </div>
            <div class="course-difficulty difficulty-${course.difficulty}">
                ${course.difficulty}
            </div>
            <p class="course-description">${course.description}</p>
            <div class="course-stats">
                <span><i class="fas fa-clock"></i> ${course.duration}</span>
                <span><i class="fas fa-users"></i> ${course.students} étudiants</span>
            </div>
        `;

        card.addEventListener('click', () => {
            this.openCourse(course.id);
        });

        return card;
    }

    openCourse(courseId) {
        this.currentCourse = this.courses[courseId];
        if (!this.currentCourse) return;

        this.currentLesson = 1;
        this.showCourseModal();
    }

    showCourseModal() {
        const modal = document.getElementById('courseModal');
        const content = document.getElementById('courseContent');
        
        if (!modal || !content) return;

        const lesson = this.currentCourse.lessons.find(l => l.id === this.currentLesson);
        if (!lesson) return;

        content.innerHTML = this.renderLesson(lesson);
        modal.style.display = 'block';

        // Démarrer le suivi du temps
        this.startLessonTimer();
    }

    renderLesson(lesson) {
        const totalLessons = this.currentCourse.lessons.length;
        const progressPercent = (this.currentLesson / totalLessons) * 100;

        return `
            <div class="course-header">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <i class="${this.currentCourse.icon}" style="color: ${this.currentCourse.color}; margin-right: 1rem; font-size: 2rem;"></i>
                    <div>
                        <h2>${this.currentCourse.title}</h2>
                        <p style="color: var(--text-secondary); margin: 0;">Leçon ${this.currentLesson} sur ${totalLessons}</p>
                    </div>
                </div>
                <div class="progress-bar" style="margin-bottom: 2rem;">
                    <div class="progress-fill" style="width: ${progressPercent}%"></div>
                </div>
            </div>
            
            <div class="lesson-content">
                <h2>${lesson.title}</h2>
                <div class="course-content">
                    ${lesson.content}
                </div>
            </div>
            
            <div class="course-navigation">
                <button class="btn-secondary" onclick="courseSystem.previousLesson()" 
                        ${this.currentLesson <= 1 ? 'disabled' : ''}>
                    <i class="fas fa-chevron-left"></i> Précédent
                </button>
                
                <button class="btn-primary" onclick="courseSystem.nextLesson()">
                    ${this.currentLesson < totalLessons ? 'Suivant' : 'Terminer'}
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        `;
    }

    nextLesson() {
        const totalLessons = this.currentCourse.lessons.length;
        
        // Enregistrer la progression
        if (isLoggedIn) {
            const timeSpent = this.getLessonTime();
            updateProgress(this.currentCourse.id, this.currentLesson, timeSpent);
        }

        if (this.currentLesson < totalLessons) {
            this.currentLesson++;
            this.showCourseModal();
        } else {
            // Cours terminé
            showNotification(`Félicitations ! Vous avez terminé le cours ${this.currentCourse.title} !`, 'success');
            document.getElementById('courseModal').style.display = 'none';
            
            if (isLoggedIn) {
                loadUserProgress();
            }
        }
    }

    previousLesson() {
        if (this.currentLesson > 1) {
            this.currentLesson--;
            this.showCourseModal();
        }
    }

    startLessonTimer() {
        this.lessonStartTime = Date.now();
    }

    getLessonTime() {
        if (!this.lessonStartTime) return 0;
        return Math.floor((Date.now() - this.lessonStartTime) / 1000); // en secondes
    }

    getCourseProgress(courseId) {
        if (!isLoggedIn || !currentUser || !currentUser.progress[courseId]) {
            return { completed: 0, total: this.courses[courseId].lessons.length };
        }
        return currentUser.progress[courseId];
    }
}

// Initialiser le système de cours
const courseSystem = new CourseSystem();

// Fonction globale pour charger les cours
function loadCourses() {
    courseSystem.renderCourses();
}
