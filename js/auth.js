// Système d'authentification
class AuthSystem {
    constructor() {
        this.users = JSON.parse(localStorage.getItem('users')) || [];
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Formulaire de connexion
        const loginForm = document.getElementById('loginForm');
        if (loginForm) {
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleLogin();
            });
        }

        // Formulaire d'inscription
        const registerForm = document.getElementById('registerForm');
        if (registerForm) {
            registerForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleRegister();
            });
        }

        // Bouton de déconnexion
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                this.handleLogout();
            });
        }
    }

    handleLogin() {
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        if (!email || !password) {
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        const user = this.users.find(u => u.email === email && u.password === password);
        
        if (user) {
            this.loginUser(user);
            document.getElementById('loginModal').style.display = 'none';
            showNotification(`Bienvenue ${user.username} !`, 'success');
        } else {
            showNotification('Email ou mot de passe incorrect', 'error');
        }
    }

    handleRegister() {
        const username = document.getElementById('registerUsername').value;
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        // Validation
        if (!username || !email || !password || !confirmPassword) {
            showNotification('Veuillez remplir tous les champs', 'error');
            return;
        }

        if (password !== confirmPassword) {
            showNotification('Les mots de passe ne correspondent pas', 'error');
            return;
        }

        if (password.length < 6) {
            showNotification('Le mot de passe doit contenir au moins 6 caractères', 'error');
            return;
        }

        if (this.users.find(u => u.email === email)) {
            showNotification('Cet email est déjà utilisé', 'error');
            return;
        }

        if (this.users.find(u => u.username === username)) {
            showNotification('Ce nom d\'utilisateur est déjà pris', 'error');
            return;
        }

        // Créer le nouvel utilisateur
        const newUser = {
            id: generateId(),
            username: username,
            email: email,
            password: password, // Note: En production, il faudrait hasher le mot de passe
            joinDate: new Date().toISOString(),
            progress: this.initializeUserProgress(),
            achievements: [],
            stats: {
                totalLessonsCompleted: 0,
                totalTimeSpent: 0,
                streak: 0,
                lastActivity: null
            }
        };

        this.users.push(newUser);
        this.saveUsers();
        this.loginUser(newUser);
        
        document.getElementById('registerModal').style.display = 'none';
        showNotification(`Compte créé avec succès ! Bienvenue ${username} !`, 'success');
    }

    loginUser(user) {
        currentUser = user;
        isLoggedIn = true;
        localStorage.setItem('currentUser', JSON.stringify(user));
        updateUIForLoggedInUser();
    }

    handleLogout() {
        currentUser = null;
        isLoggedIn = false;
        localStorage.removeItem('currentUser');
        
        // Réinitialiser l'interface
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const userMenu = document.getElementById('userMenu');
        
        loginBtn.style.display = 'inline-block';
        registerBtn.style.display = 'inline-block';
        userMenu.style.display = 'none';
        
        // Masquer les sections nécessitant une connexion
        this.hideAuthRequiredSections();
        
        showNotification('Vous avez été déconnecté', 'success');
    }

    hideAuthRequiredSections() {
        const progressContent = document.getElementById('progressContent');
        const achievementsContent = document.getElementById('achievementsContent');
        
        if (progressContent) {
            progressContent.innerHTML = `
                <div class="login-required">
                    <i class="fas fa-lock"></i>
                    <p>Connectez-vous pour voir votre progression</p>
                </div>
            `;
        }
        
        if (achievementsContent) {
            achievementsContent.innerHTML = `
                <div class="login-required">
                    <i class="fas fa-lock"></i>
                    <p>Connectez-vous pour voir vos succès</p>
                </div>
            `;
        }
    }

    initializeUserProgress() {
        const courses = ['html', 'css', 'c', 'python'];
        const progress = {};
        
        courses.forEach(course => {
            progress[course] = {
                completed: 0,
                total: this.getCourseTotalLessons(course),
                currentLesson: 1,
                timeSpent: 0,
                lastAccessed: null
            };
        });
        
        return progress;
    }

    getCourseTotalLessons(courseId) {
        const courseLessons = {
            'html': 15,
            'css': 20,
            'c': 25,
            'python': 30
        };
        return courseLessons[courseId] || 10;
    }

    saveUsers() {
        localStorage.setItem('users', JSON.stringify(this.users));
    }

    updateUserProgress(courseId, lessonId, timeSpent = 0) {
        if (!isLoggedIn || !currentUser) return;

        if (!currentUser.progress[courseId]) {
            currentUser.progress[courseId] = {
                completed: 0,
                total: this.getCourseTotalLessons(courseId),
                currentLesson: 1,
                timeSpent: 0,
                lastAccessed: null
            };
        }

        const courseProgress = currentUser.progress[courseId];
        
        // Mettre à jour la progression
        if (lessonId > courseProgress.currentLesson) {
            courseProgress.completed = lessonId - 1;
            courseProgress.currentLesson = lessonId;
        }
        
        courseProgress.timeSpent += timeSpent;
        courseProgress.lastAccessed = new Date().toISOString();
        
        // Mettre à jour les stats globales
        currentUser.stats.totalLessonsCompleted = Object.values(currentUser.progress)
            .reduce((total, course) => total + course.completed, 0);
        currentUser.stats.totalTimeSpent += timeSpent;
        currentUser.stats.lastActivity = new Date().toISOString();
        
        // Sauvegarder
        this.saveUserData();
        
        // Vérifier les succès
        this.checkAchievements();
        
        // Mettre à jour l'interface
        loadUserProgress();
    }

    saveUserData() {
        // Mettre à jour dans la liste des utilisateurs
        const userIndex = this.users.findIndex(u => u.id === currentUser.id);
        if (userIndex !== -1) {
            this.users[userIndex] = currentUser;
            this.saveUsers();
        }
        
        // Sauvegarder l'utilisateur actuel
        localStorage.setItem('currentUser', JSON.stringify(currentUser));
    }

    checkAchievements() {
        if (!isLoggedIn || !currentUser) return;

        const achievements = [
            {
                id: 'first_lesson',
                title: 'Premier pas',
                description: 'Terminer votre première leçon',
                icon: 'fa-star',
                condition: () => currentUser.stats.totalLessonsCompleted >= 1
            },
            {
                id: 'html_beginner',
                title: 'Apprenti HTML',
                description: 'Terminer 5 leçons HTML',
                icon: 'fa-code',
                condition: () => currentUser.progress.html && currentUser.progress.html.completed >= 5
            },
            {
                id: 'css_beginner',
                title: 'Styliste CSS',
                description: 'Terminer 5 leçons CSS',
                icon: 'fa-paint-brush',
                condition: () => currentUser.progress.css && currentUser.progress.css.completed >= 5
            },
            {
                id: 'dedicated_learner',
                title: 'Apprenant dévoué',
                description: 'Passer 5 heures à apprendre',
                icon: 'fa-clock',
                condition: () => currentUser.stats.totalTimeSpent >= 5 * 60 * 60 // 5 heures en secondes
            },
            {
                id: 'course_master',
                title: 'Maître du cours',
                description: 'Terminer un cours complet',
                icon: 'fa-trophy',
                condition: () => {
                    return Object.values(currentUser.progress).some(course => 
                        course.completed >= course.total
                    );
                }
            },
            {
                id: 'polyglot',
                title: 'Polyglotte',
                description: 'Commencer l\'apprentissage de 3 langages',
                icon: 'fa-globe',
                condition: () => {
                    return Object.values(currentUser.progress).filter(course => 
                        course.completed > 0
                    ).length >= 3;
                }
            }
        ];

        let newAchievements = [];
        
        achievements.forEach(achievement => {
            const alreadyUnlocked = currentUser.achievements.some(a => a.id === achievement.id);
            
            if (!alreadyUnlocked && achievement.condition()) {
                currentUser.achievements.push({
                    ...achievement,
                    unlockedAt: new Date().toISOString()
                });
                newAchievements.push(achievement);
            }
        });

        if (newAchievements.length > 0) {
            this.saveUserData();
            
            // Afficher les notifications pour les nouveaux succès
            newAchievements.forEach(achievement => {
                setTimeout(() => {
                    showNotification(`🏆 Succès débloqué: ${achievement.title}!`, 'success');
                }, 500);
            });
            
            // Mettre à jour l'affichage des succès
            loadUserAchievements();
        }
    }

    // Méthode pour réinitialiser les données (utile pour le développement)
    resetUserData() {
        if (confirm('Êtes-vous sûr de vouloir réinitialiser toutes vos données ?')) {
            localStorage.removeItem('users');
            localStorage.removeItem('currentUser');
            this.users = [];
            this.handleLogout();
            showNotification('Données réinitialisées', 'success');
        }
    }
}

// Initialiser le système d'authentification
const authSystem = new AuthSystem();

// Fonction globale pour mettre à jour la progression (utilisée par le système de cours)
function updateProgress(courseId, lessonId, timeSpent = 0) {
    authSystem.updateUserProgress(courseId, lessonId, timeSpent);
}
