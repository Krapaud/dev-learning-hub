// Navigation mobile
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        
        // Fermer le menu quand on clique sur un lien
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
    }
    
    // Gestion des messages flash
    setupFlashMessages();
    
    // Effets d'animation au scroll
    setupScrollAnimations();
    
    // Effets de hover pour les boutons
    setupButtonEffects();
    
    // Console easter egg
    setupConsoleEasterEgg();
    
    // Raccourcis clavier
    setupKeyboardShortcuts();
});

// Gestion des messages flash
function setupFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-hide après 5 secondes
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 300);
        }, 5000);
        
        // Animation d'apparition
        alert.style.opacity = '0';
        alert.style.transform = 'translateX(100%)';
        setTimeout(() => {
            alert.style.opacity = '1';
            alert.style.transform = 'translateX(0)';
        }, 100);
    });
}

// Animations au scroll
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observer les cartes et éléments
    const elements = document.querySelectorAll('.card, .stats-card, .form-container');
    elements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Effets sur les boutons
function setupButtonEffects() {
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 0 20px rgba(0, 255, 65, 0.4)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '';
        });
        
        button.addEventListener('click', function(e) {
            // Effet ripple
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Easter egg dans la console
function setupConsoleEasterEgg() {
    console.log(`
    ╔══════════════════════════════════════╗
    ║          🚀 GeekSite v1.0            ║
    ║                                      ║
    ║  Bienvenue dans la matrice, hacker!  ║
    ║                                      ║
    ║  Commandes disponibles:              ║
    ║  • konami() - Active le code Konami  ║
    ║  • matrix() - Toggle Matrix rain     ║
    ║  • glitch() - Effet glitch global    ║
    ║  • hack() - Mode hacker              ║
    ║                                      ║
    ║  Stack: Python/Flask + HTML/CSS/JS  ║
    ╚══════════════════════════════════════╝
    `);
    
    // Commandes de la console
    window.konami = function() {
        document.body.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            document.body.style.transform = '';
        }, 1000);
        console.log('🎮 Code Konami activé!');
    };
    
    window.matrix = function() {
        const canvas = document.getElementById('matrix-canvas');
        if (canvas) {
            canvas.style.opacity = canvas.style.opacity === '0' ? '0.1' : '0';
            console.log('🔧 Matrix rain toggled');
        }
    };
    
    window.glitch = function() {
        const elements = document.querySelectorAll('h1, h2, h3, .card-title');
        elements.forEach(el => {
            glitchEffect(el);
        });
        console.log('⚡ Effet glitch activé!');
    };
    
    window.hack = function() {
        document.body.classList.toggle('hacker-mode');
        console.log('💻 Mode hacker toggled');
    };
}

// Raccourcis clavier
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl + Shift + D = Dashboard
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
            e.preventDefault();
            const dashboardLink = document.querySelector('a[href*="dashboard"]');
            if (dashboardLink) {
                dashboardLink.click();
            }
        }
        
        // Ctrl + Shift + A = Admin (si disponible)
        if (e.ctrlKey && e.shiftKey && e.key === 'A') {
            e.preventDefault();
            const adminLink = document.querySelector('a[href*="admin"]');
            if (adminLink) {
                adminLink.click();
            }
        }
        
        // Ctrl + Shift + L = Logout
        if (e.ctrlKey && e.shiftKey && e.key === 'L') {
            e.preventDefault();
            const logoutLink = document.querySelector('a[href*="logout"]');
            if (logoutLink) {
                logoutLink.click();
            }
        }
        
        // Echap = Fermer les modales/menus
        if (e.key === 'Escape') {
            const navMenu = document.getElementById('nav-menu');
            const navToggle = document.getElementById('nav-toggle');
            if (navMenu && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        }
    });
}

// Effet de dactylographie pour les titres
function typewriterEffect(element, text, speed = 50) {
    element.innerHTML = '';
    let i = 0;
    
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else {
            // Ajouter un curseur clignotant
            const cursor = document.createElement('span');
            cursor.textContent = '|';
            cursor.style.animation = 'blink 1s infinite';
            element.appendChild(cursor);
        }
    }
    
    type();
}

// Validation de formulaire en temps réel
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateInput(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('invalid')) {
                    validateInput(this);
                }
            });
        });
    });
}

function validateInput(input) {
    const isValid = input.checkValidity();
    
    if (isValid) {
        input.classList.remove('invalid');
        input.classList.add('valid');
    } else {
        input.classList.add('invalid');
        input.classList.remove('valid');
    }
    
    return isValid;
}

// Effet parallax léger
function setupParallax() {
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const rate = scrolled * -0.5;
        
        const canvas = document.getElementById('matrix-canvas');
        if (canvas) {
            canvas.style.transform = `translateY(${rate}px)`;
        }
    });
}

// Initialisation de tous les effets
document.addEventListener('DOMContentLoaded', function() {
    setupFormValidation();
    setupParallax();
    
    // Animation des compteurs
    const counters = document.querySelectorAll('.stats-number');
    counters.forEach(counter => {
        animateCounter(counter);
    });
});

// Animation des compteurs
function animateCounter(element) {
    const target = parseInt(element.textContent);
    if (isNaN(target)) return;
    
    const increment = target / 50;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 50);
}

// CSS pour l'effet ripple
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(0, 255, 65, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .hacker-mode {
        filter: hue-rotate(120deg) contrast(1.2);
    }
    
    .hacker-mode .nav-brand a {
        animation: glow 1s ease-in-out infinite alternate;
    }
`;

document.head.appendChild(style);
