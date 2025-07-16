// Système de progression et succès
function loadUserProgress() {
    if (!isLoggedIn || !currentUser) {
        return;
    }

    const progressContent = document.getElementById('progressContent');
    if (!progressContent) return;

    const totalStats = calculateTotalStats();
    
    progressContent.innerHTML = `
        <div class="progress-overview">
            <div class="progress-card">
                <h3><i class="fas fa-book"></i> Leçons terminées</h3>
                <div class="stat-number">${totalStats.totalCompleted}</div>
                <div class="stat-label">sur ${totalStats.totalLessons} leçons</div>
            </div>
            
            <div class="progress-card">
                <h3><i class="fas fa-clock"></i> Temps d'apprentissage</h3>
                <div class="stat-number">${formatTime(currentUser.stats.totalTimeSpent)}</div>
                <div class="stat-label">temps total</div>
            </div>
            
            <div class="progress-card">
                <h3><i class="fas fa-fire"></i> Série actuelle</h3>
                <div class="stat-number">${currentUser.stats.streak || 0}</div>
                <div class="stat-label">jours consécutifs</div>
            </div>
            
            <div class="progress-card">
                <h3><i class="fas fa-trophy"></i> Succès</h3>
                <div class="stat-number">${currentUser.achievements.length}</div>
                <div class="stat-label">débloqués</div>
            </div>
        </div>
        
        <div class="courses-progress">
            <h3>Progression par cours</h3>
            <div class="courses-progress-grid">
                ${renderCoursesProgress()}
            </div>
        </div>
        
        <div class="recent-activity">
            <h3>Activité récente</h3>
            <div class="activity-list">
                ${renderRecentActivity()}
            </div>
        </div>
    `;
}

function calculateTotalStats() {
    if (!currentUser || !currentUser.progress) {
        return { totalCompleted: 0, totalLessons: 0 };
    }

    let totalCompleted = 0;
    let totalLessons = 0;

    Object.values(currentUser.progress).forEach(courseProgress => {
        totalCompleted += courseProgress.completed;
        totalLessons += courseProgress.total;
    });

    return { totalCompleted, totalLessons };
}

function renderCoursesProgress() {
    if (!currentUser || !currentUser.progress) return '';

    return Object.entries(currentUser.progress).map(([courseId, progress]) => {
        const course = courseSystem.courses[courseId];
        if (!course) return '';

        const percentage = Math.round((progress.completed / progress.total) * 100);
        const isCompleted = progress.completed >= progress.total;

        return `
            <div class="course-progress-item ${isCompleted ? 'completed' : ''}">
                <div class="course-progress-header">
                    <div class="course-info">
                        <i class="${course.icon}" style="color: ${course.color}"></i>
                        <span class="course-name">${course.title}</span>
                    </div>
                    <span class="progress-percentage">${percentage}%</span>
                </div>
                
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${percentage}%"></div>
                </div>
                
                <div class="progress-details">
                    <span>${progress.completed}/${progress.total} leçons</span>
                    <span>${formatTime(progress.timeSpent)}</span>
                    ${progress.lastAccessed ? `<span>Dernière fois: ${formatDate(progress.lastAccessed)}</span>` : ''}
                </div>
                
                ${isCompleted ? '<div class="completion-badge"><i class="fas fa-check-circle"></i> Terminé</div>' : ''}
            </div>
        `;
    }).join('');
}

function renderRecentActivity() {
    if (!currentUser || !currentUser.progress) {
        return '<p class="no-activity">Aucune activité récente</p>';
    }

    // Créer une liste d'activités récentes basée sur les cours
    const activities = [];
    
    Object.entries(currentUser.progress).forEach(([courseId, progress]) => {
        const course = courseSystem.courses[courseId];
        if (course && progress.lastAccessed) {
            activities.push({
                type: 'lesson',
                course: course,
                progress: progress,
                date: new Date(progress.lastAccessed)
            });
        }
    });

    // Ajouter les succès récents
    if (currentUser.achievements) {
        currentUser.achievements.forEach(achievement => {
            activities.push({
                type: 'achievement',
                achievement: achievement,
                date: new Date(achievement.unlockedAt)
            });
        });
    }

    // Trier par date (plus récent en premier)
    activities.sort((a, b) => b.date - a.date);

    // Prendre les 5 plus récentes
    const recentActivities = activities.slice(0, 5);

    if (recentActivities.length === 0) {
        return '<p class="no-activity">Aucune activité récente</p>';
    }

    return recentActivities.map(activity => {
        if (activity.type === 'lesson') {
            return `
                <div class="activity-item">
                    <div class="activity-icon">
                        <i class="${activity.course.icon}" style="color: ${activity.course.color}"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">Progression en ${activity.course.title}</div>
                        <div class="activity-description">
                            ${activity.progress.completed}/${activity.progress.total} leçons terminées
                        </div>
                        <div class="activity-date">${formatTimeAgo(activity.date)}</div>
                    </div>
                </div>
            `;
        } else if (activity.type === 'achievement') {
            return `
                <div class="activity-item achievement-activity">
                    <div class="activity-icon">
                        <i class="fas ${activity.achievement.icon}" style="color: var(--primary-color)"></i>
                    </div>
                    <div class="activity-content">
                        <div class="activity-title">🏆 Succès débloqué</div>
                        <div class="activity-description">${activity.achievement.title}</div>
                        <div class="activity-date">${formatTimeAgo(activity.date)}</div>
                    </div>
                </div>
            `;
        }
        return '';
    }).join('');
}

function loadUserAchievements() {
    if (!isLoggedIn || !currentUser) {
        return;
    }

    const achievementsContent = document.getElementById('achievementsContent');
    if (!achievementsContent) return;

    // Liste de tous les succès possibles
    const allAchievements = [
        {
            id: 'first_lesson',
            title: 'Premier pas',
            description: 'Terminer votre première leçon',
            icon: 'fa-star'
        },
        {
            id: 'html_beginner',
            title: 'Apprenti HTML',
            description: 'Terminer 5 leçons HTML',
            icon: 'fa-code'
        },
        {
            id: 'css_beginner',
            title: 'Styliste CSS',
            description: 'Terminer 5 leçons CSS',
            icon: 'fa-paint-brush'
        },
        {
            id: 'dedicated_learner',
            title: 'Apprenant dévoué',
            description: 'Passer 5 heures à apprendre',
            icon: 'fa-clock'
        },
        {
            id: 'course_master',
            title: 'Maître du cours',
            description: 'Terminer un cours complet',
            icon: 'fa-trophy'
        },
        {
            id: 'polyglot',
            title: 'Polyglotte',
            description: 'Commencer l\'apprentissage de 3 langages',
            icon: 'fa-globe'
        },
        {
            id: 'speed_learner',
            title: 'Apprenant rapide',
            description: 'Terminer 10 leçons en une journée',
            icon: 'fa-rocket'
        },
        {
            id: 'consistent_learner',
            title: 'Régularité',
            description: 'Apprendre 7 jours consécutifs',
            icon: 'fa-calendar-check'
        },
        {
            id: 'night_owl',
            title: 'Oiseau de nuit',
            description: 'Apprendre après minuit',
            icon: 'fa-moon'
        },
        {
            id: 'early_bird',
            title: 'Lève-tôt',
            description: 'Apprendre avant 7h du matin',
            icon: 'fa-sun'
        }
    ];

    const unlockedAchievements = currentUser.achievements || [];
    const unlockedIds = unlockedAchievements.map(a => a.id);

    achievementsContent.innerHTML = `
        <div class="achievements-stats">
            <div class="achievement-progress">
                <h3>Progression des succès</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${(unlockedAchievements.length / allAchievements.length) * 100}%"></div>
                </div>
                <p>${unlockedAchievements.length} sur ${allAchievements.length} succès débloqués</p>
            </div>
        </div>
        
        <div class="achievements-grid">
            ${allAchievements.map(achievement => {
                const isUnlocked = unlockedIds.includes(achievement.id);
                const unlockedData = isUnlocked ? unlockedAchievements.find(a => a.id === achievement.id) : null;
                
                return `
                    <div class="achievement-card ${isUnlocked ? 'unlocked' : 'locked'}">
                        <div class="achievement-icon">
                            <i class="fas ${achievement.icon}"></i>
                        </div>
                        <h4 class="achievement-title">${achievement.title}</h4>
                        <p class="achievement-description">${achievement.description}</p>
                        ${isUnlocked && unlockedData ? 
                            `<div class="achievement-date">Débloqué le ${formatDate(unlockedData.unlockedAt)}</div>` : 
                            '<div class="achievement-locked">🔒 Verrouillé</div>'
                        }
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

// Fonctions utilitaires
function formatTime(seconds) {
    if (seconds < 60) {
        return `${seconds}s`;
    } else if (seconds < 3600) {
        const minutes = Math.floor(seconds / 60);
        return `${minutes}min`;
    } else {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${hours}h ${minutes}min`;
    }
}

function formatTimeAgo(date) {
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) {
        return 'À l\'instant';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `Il y a ${minutes} minute${minutes > 1 ? 's' : ''}`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `Il y a ${hours} heure${hours > 1 ? 's' : ''}`;
    } else {
        const days = Math.floor(diffInSeconds / 86400);
        return `Il y a ${days} jour${days > 1 ? 's' : ''}`;
    }
}

// Système de statistiques avancées
function generateDetailedStats() {
    if (!isLoggedIn || !currentUser) return null;

    const progress = currentUser.progress;
    const stats = {
        totalTime: currentUser.stats.totalTimeSpent,
        totalLessons: currentUser.stats.totalLessonsCompleted,
        averageSessionTime: 0,
        favoriteLanguage: null,
        learningStreak: currentUser.stats.streak || 0,
        coursesStarted: 0,
        coursesCompleted: 0
    };

    // Calculer les statistiques par cours
    Object.entries(progress).forEach(([courseId, courseProgress]) => {
        if (courseProgress.completed > 0) {
            stats.coursesStarted++;
        }
        if (courseProgress.completed >= courseProgress.total) {
            stats.coursesCompleted++;
        }
    });

    // Trouver le langage favori (le plus de temps passé)
    let maxTime = 0;
    Object.entries(progress).forEach(([courseId, courseProgress]) => {
        if (courseProgress.timeSpent > maxTime) {
            maxTime = courseProgress.timeSpent;
            stats.favoriteLanguage = courseSystem.courses[courseId]?.title || courseId;
        }
    });

    // Calculer le temps moyen par session (approximatif)
    if (stats.totalLessons > 0) {
        stats.averageSessionTime = Math.floor(stats.totalTime / stats.totalLessons);
    }

    return stats;
}

// Mise à jour de la série d'apprentissage
function updateLearningStreak() {
    if (!isLoggedIn || !currentUser) return;

    const today = new Date().toDateString();
    const lastActivity = currentUser.stats.lastActivity ? 
        new Date(currentUser.stats.lastActivity).toDateString() : null;

    if (lastActivity !== today) {
        // Nouvelle journée d'activité
        if (lastActivity) {
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (new Date(lastActivity).toDateString() === yesterday.toDateString()) {
                // Activité hier, continuer la série
                currentUser.stats.streak = (currentUser.stats.streak || 0) + 1;
            } else {
                // Pas d'activité hier, redémarrer la série
                currentUser.stats.streak = 1;
            }
        } else {
            // Première activité
            currentUser.stats.streak = 1;
        }
        
        currentUser.stats.lastActivity = new Date().toISOString();
        authSystem.saveUserData();
    }
}
