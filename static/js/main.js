// JavaScript principal pour Dev Learning Hub

document.addEventListener('DOMContentLoaded', function() {
    initMatrixEffect();
    initFlashMessages();
    initAnimations();
});

// Effet Matrix en arrière-plan
function initMatrixEffect() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Redimensionner le canvas
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Caractères Matrix
    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
    const matrixArray = matrix.split("");
    
    const fontSize = 14;
    const columns = Math.floor(canvas.width / fontSize);
    
    // Tableau pour chaque colonne
    const drops = [];
    for (let x = 0; x < columns; x++) {
        drops[x] = 1;
    }
    
    function draw() {
        // Fond semi-transparent pour l'effet de traînée
        ctx.fillStyle = 'rgba(13, 17, 23, 0.04)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff88';
        ctx.font = fontSize + 'px JetBrains Mono, monospace';
        
        // Dessiner les caractères qui tombent
        for (let i = 0; i < drops.length; i++) {
            const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            // Réinitialiser la colonne aléatoirement
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            
            drops[i]++;
        }
    }
    
    setInterval(draw, 35);
}

// Gestion des messages flash
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        const closeBtn = message.querySelector('.close-flash');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                message.style.animation = 'slideOutRight 0.3s ease forwards';
                setTimeout(() => {
                    message.remove();
                }, 300);
            });
        }
        
        // Auto-fermeture après 5 secondes
        setTimeout(() => {
            if (message.parentNode) {
                message.style.animation = 'slideOutRight 0.3s ease forwards';
                setTimeout(() => {
                    message.remove();
                }, 300);
            }
        }, 5000);
    });
}

// Animations au scroll et au chargement
function initAnimations() {
    // Observer pour les animations au scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    // Observer les éléments animables
    const animatableElements = document.querySelectorAll('.course-card, .feature-card, .stat-card, .trophy-card, .lesson-item');
    animatableElements.forEach(el => {
        observer.observe(el);
    });
}

// Fonctions utilitaires pour les interactions

// Animation de typing pour les titres
function typeWriter(element, text, speed = 100) {
    let i = 0;
    element.innerHTML = '';
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Effet de particules pour les célébrations
function createParticles(container, count = 50) {
    for (let i = 0; i < count; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00ff88;
            border-radius: 50%;
            pointer-events: none;
            animation: particleFloat ${Math.random() * 3 + 2}s ease-out forwards;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        
        container.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 5000);
    }
}

// Effet de glow au survol des boutons
document.addEventListener('mouseover', function(e) {
    if (e.target.classList.contains('btn-primary')) {
        e.target.style.boxShadow = '0 0 30px rgba(0, 255, 136, 0.4)';
    } else if (e.target.classList.contains('btn-secondary')) {
        e.target.style.boxShadow = '0 0 20px rgba(0, 212, 255, 0.3)';
    }
});

document.addEventListener('mouseout', function(e) {
    if (e.target.classList.contains('btn')) {
        e.target.style.boxShadow = '';
    }
});

// Fonction pour animer les compteurs
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(start + (target - start) * easeOutCubic(progress));
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Fonction d'easing
function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

// Gestion du scroll fluide pour les ancres
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Effet de saisie pour les inputs
document.querySelectorAll('input[type="text"], input[type="password"]').forEach(input => {
    input.addEventListener('input', function() {
        if (this.value.length > 0) {
            this.classList.add('has-content');
        } else {
            this.classList.remove('has-content');
        }
    });
});

// Détection du thème système (pour de futures améliorations)
function detectSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    }
    return 'light';
}

// Fonction de copie dans le presse-papiers
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Copié dans le presse-papiers !', 'success');
        });
    } else {
        // Fallback pour les navigateurs plus anciens
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        showNotification('Copié dans le presse-papiers !', 'success');
    }
}

// Système de notifications personnalisé
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
        <button class="close-notification">&times;</button>
    `;
    
    // Styles pour la notification
    notification.style.cssText = `
        position: fixed;
        top: 120px;
        right: 2rem;
        background: var(--bg-secondary);
        border: 1px solid var(--accent-primary);
        border-radius: 8px;
        padding: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        box-shadow: var(--shadow-primary);
        z-index: 1001;
        animation: slideInRight 0.3s ease;
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    // Bouton de fermeture
    const closeBtn = notification.querySelector('.close-notification');
    closeBtn.addEventListener('click', () => {
        removeNotification(notification);
    });
    
    // Auto-fermeture
    setTimeout(() => {
        removeNotification(notification);
    }, duration);
}

function removeNotification(notification) {
    notification.style.animation = 'slideOutRight 0.3s ease forwards';
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 300);
}

// Gestion des erreurs JavaScript
window.addEventListener('error', function(e) {
    console.error('Erreur JavaScript:', e.error);
    // En mode développement seulement
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        showNotification('Une erreur JavaScript s\'est produite. Consultez la console.', 'error');
    }
});

// Préchargement des images importantes
function preloadImages() {
    const imageUrls = [
        // Ajouter ici les URLs des images importantes à précharger
    ];
    
    imageUrls.forEach(url => {
        const img = new Image();
        img.src = url;
    });
}

// Initialiser le préchargement au chargement de la page
window.addEventListener('load', preloadImages);

// Fonction pour détecter si l'utilisateur est sur mobile
function isMobile() {
    return window.innerWidth <= 768;
}

// Ajustements pour mobile
if (isMobile()) {
    // Désactiver l'effet Matrix sur mobile pour les performances
    const matrixCanvas = document.getElementById('matrix-canvas');
    if (matrixCanvas) {
        matrixCanvas.style.display = 'none';
    }
}

// Fonction pour générer des couleurs aléatoirement (pour les futurs effets)
function getRandomColor() {
    const colors = ['#00ff88', '#00d4ff', '#ff6b35', '#ffd93d', '#a8e6cf'];
    return colors[Math.floor(Math.random() * colors.length)];
}

// Animation CSS supplémentaire pour les particules
const particleStyle = document.createElement('style');
particleStyle.textContent = `
    @keyframes particleFloat {
        0% {
            transform: translateY(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(-100px) rotate(360deg);
            opacity: 0;
        }
    }
    
    @keyframes slideOutRight {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification {
        color: var(--text-primary);
    }
    
    .notification-success {
        border-color: var(--accent-primary);
    }
    
    .notification-error {
        border-color: var(--accent-tertiary);
    }
    
    .notification-info {
        border-color: var(--accent-secondary);
    }
    
    .close-notification {
        background: none;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        font-size: 1.2rem;
        margin-left: auto;
    }
    
    .close-notification:hover {
        color: var(--text-primary);
    }
`;

document.head.appendChild(particleStyle);

// Export des fonctions pour utilisation dans d'autres scripts
window.DevLearningHub = {
    typeWriter,
    createParticles,
    animateCounter,
    copyToClipboard,
    showNotification,
    isMobile,
    getRandomColor
};
