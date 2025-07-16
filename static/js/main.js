// Dev Learning Hub - JavaScript principal

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des animations et effets
    initMatrixBackground();
    initScrollAnimations();
    initFormValidations();
    initTooltips();
    
    console.log('🚀 Dev Learning Hub chargé avec succès!');
});

// Animation Matrix en arrière-plan
function initMatrixBackground() {
    const matrixBg = document.querySelector('.matrix-bg');
    if (!matrixBg) return;

    // Créer un canvas pour l'effet Matrix
    const canvas = document.createElement('canvas');
    canvas.style.position = 'absolute';
    canvas.style.top = '0';
    canvas.style.left = '0';
    canvas.style.width = '100%';
    canvas.style.height = '100%';
    canvas.style.pointerEvents = 'none';
    canvas.style.opacity = '0.1';
    
    matrixBg.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Caractères Matrix
    const matrixChars = '01';
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    const drops = [];
    
    // Initialiser les gouttes
    for (let i = 0; i < columns; i++) {
        drops[i] = 1;
    }
    
    function drawMatrix() {
        ctx.fillStyle = 'rgba(13, 17, 23, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff88';
        ctx.font = fontSize + 'px JetBrains Mono';
        
        for (let i = 0; i < drops.length; i++) {
            const text = matrixChars[Math.floor(Math.random() * matrixChars.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(drawMatrix, 100);
}

// Animations au scroll
function initScrollAnimations() {
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
    
    // Observer les éléments avec animation
    const animatedElements = document.querySelectorAll('.course-card, .feature-card, .stat-card, .lesson-card, .trophy-card');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        observer.observe(el);
    });
}

// Validation des formulaires
function initFormValidations() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', validateInput);
            input.addEventListener('input', clearValidationError);
        });
        
        form.addEventListener('submit', handleFormSubmit);
    });
}

function validateInput(e) {
    const input = e.target;
    const value = input.value.trim();
    
    // Supprimer les messages d'erreur existants
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
    
    let isValid = true;
    let errorMessage = '';
    
    // Validation selon le type d'input
    switch (input.type) {
        case 'text':
            if (input.name === 'username') {
                if (value.length < 3) {
                    isValid = false;
                    errorMessage = 'Le nom d\'utilisateur doit contenir au moins 3 caractères';
                } else if (!/^[a-zA-Z0-9_]+$/.test(value)) {
                    isValid = false;
                    errorMessage = 'Le nom d\'utilisateur ne peut contenir que des lettres, chiffres et underscores';
                }
            }
            break;
            
        case 'password':
            if (value.length < 6) {
                isValid = false;
                errorMessage = 'Le mot de passe doit contenir au moins 6 caractères';
            }
            break;
    }
    
    // Afficher l'erreur si nécessaire
    if (!isValid) {
        showInputError(input, errorMessage);
    } else {
        input.classList.remove('error');
        input.classList.add('valid');
    }
    
    return isValid;
}

function showInputError(input, message) {
    input.classList.add('error');
    input.classList.remove('valid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    errorDiv.style.color = '#ef4444';
    errorDiv.style.fontSize = '0.8rem';
    errorDiv.style.marginTop = '0.25rem';
    
    input.parentNode.appendChild(errorDiv);
}

function clearValidationError(e) {
    const input = e.target;
    const errorMessage = input.parentNode.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
    input.classList.remove('error');
}

function handleFormSubmit(e) {
    const form = e.target;
    const inputs = form.querySelectorAll('input[required]');
    let isFormValid = true;
    
    inputs.forEach(input => {
        if (!validateInput({ target: input })) {
            isFormValid = false;
        }
    });
    
    // Validation spéciale pour la confirmation de mot de passe
    const password = form.querySelector('input[name="password"]');
    const confirmPassword = form.querySelector('input[name="confirm_password"]');
    
    if (password && confirmPassword) {
        if (password.value !== confirmPassword.value) {
            showInputError(confirmPassword, 'Les mots de passe ne correspondent pas');
            isFormValid = false;
        }
    }
    
    if (!isFormValid) {
        e.preventDefault();
        showNotification('Veuillez corriger les erreurs dans le formulaire', 'error');
    }
}

// Tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const element = e.target;
    const tooltipText = element.getAttribute('data-tooltip');
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.position = 'absolute';
    tooltip.style.background = '#1c2128';
    tooltip.style.color = '#f0f6fc';
    tooltip.style.padding = '0.5rem 1rem';
    tooltip.style.borderRadius = '6px';
    tooltip.style.fontSize = '0.8rem';
    tooltip.style.zIndex = '9999';
    tooltip.style.pointerEvents = 'none';
    tooltip.style.border = '1px solid #30363d';
    tooltip.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.4)';
    
    document.body.appendChild(tooltip);
    
    const rect = element.getBoundingClientRect();
    const tooltipRect = tooltip.getBoundingClientRect();
    
    tooltip.style.left = (rect.left + rect.width / 2 - tooltipRect.width / 2) + 'px';
    tooltip.style.top = (rect.top - tooltipRect.height - 10) + 'px';
    
    element._tooltip = tooltip;
}

function hideTooltip(e) {
    const element = e.target;
    if (element._tooltip) {
        element._tooltip.remove();
        delete element._tooltip;
    }
}

// Notifications
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    
    const icon = getNotificationIcon(type);
    notification.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Styles
    notification.style.position = 'fixed';
    notification.style.top = '100px';
    notification.style.right = '2rem';
    notification.style.background = '#1c2128';
    notification.style.border = `1px solid ${getNotificationColor(type)}`;
    notification.style.color = '#f0f6fc';
    notification.style.padding = '1rem';
    notification.style.borderRadius = '8px';
    notification.style.display = 'flex';
    notification.style.alignItems = 'center';
    notification.style.gap = '0.5rem';
    notification.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.4)';
    notification.style.zIndex = '1001';
    notification.style.animation = 'slideIn 0.3s ease';
    notification.style.maxWidth = '400px';
    
    notification.querySelector('button').style.background = 'none';
    notification.querySelector('button').style.border = 'none';
    notification.querySelector('button').style.color = '#8b949e';
    notification.querySelector('button').style.cursor = 'pointer';
    notification.querySelector('button').style.marginLeft = 'auto';
    
    document.body.appendChild(notification);
    
    // Auto-remove
    if (duration > 0) {
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
    }
    
    return notification;
}

function getNotificationIcon(type) {
    const icons = {
        info: 'fas fa-info-circle',
        success: 'fas fa-check-circle',
        warning: 'fas fa-exclamation-triangle',
        error: 'fas fa-times-circle'
    };
    return icons[type] || icons.info;
}

function getNotificationColor(type) {
    const colors = {
        info: '#00d4ff',
        success: '#00ff88',
        warning: '#fbbf24',
        error: '#ef4444'
    };
    return colors[type] || colors.info;
}

// Animations de progression
function animateProgressBar(element, targetWidth, duration = 1000) {
    const startWidth = 0;
    const startTime = performance.now();
    
    function updateProgress(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentWidth = startWidth + (targetWidth - startWidth) * easeOutCubic(progress);
        element.style.width = currentWidth + '%';
        
        if (progress < 1) {
            requestAnimationFrame(updateProgress);
        }
    }
    
    requestAnimationFrame(updateProgress);
}

function easeOutCubic(t) {
    return 1 - Math.pow(1 - t, 3);
}

// Animation du compteur
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
        } else {
            element.textContent = target;
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Recherche et filtrage (pour futures fonctionnalités)
function initSearch() {
    const searchInput = document.querySelector('#search-input');
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', (e) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            performSearch(e.target.value);
        }, 300);
    });
}

function performSearch(query) {
    const searchableElements = document.querySelectorAll('[data-searchable]');
    const normalizedQuery = query.toLowerCase().trim();
    
    searchableElements.forEach(element => {
        const searchText = element.getAttribute('data-searchable').toLowerCase();
        const isVisible = !normalizedQuery || searchText.includes(normalizedQuery);
        
        element.style.display = isVisible ? '' : 'none';
        
        if (isVisible && normalizedQuery) {
            highlightSearchTerms(element, normalizedQuery);
        } else {
            removeHighlights(element);
        }
    });
}

function highlightSearchTerms(element, query) {
    // Implémentation simple du surlignage
    const textNodes = getTextNodes(element);
    textNodes.forEach(node => {
        const parent = node.parentNode;
        const text = node.textContent;
        const regex = new RegExp(`(${query})`, 'gi');
        
        if (regex.test(text)) {
            const highlightedText = text.replace(regex, '<mark>$1</mark>');
            const wrapper = document.createElement('span');
            wrapper.innerHTML = highlightedText;
            parent.replaceChild(wrapper, node);
        }
    });
}

function removeHighlights(element) {
    const marks = element.querySelectorAll('mark');
    marks.forEach(mark => {
        mark.outerHTML = mark.textContent;
    });
}

function getTextNodes(element) {
    const textNodes = [];
    const walker = document.createTreeWalker(
        element,
        NodeFilter.SHOW_TEXT,
        null,
        false
    );
    
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    
    return textNodes;
}

// Utilitaires
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Gestion du thème (pour futures fonctionnalités)
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('preferred-theme', newTheme);
    
    showNotification(`Thème ${newTheme === 'dark' ? 'sombre' : 'clair'} activé`, 'success');
}

function loadSavedTheme() {
    const savedTheme = localStorage.getItem('preferred-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// Initialiser le thème au chargement
loadSavedTheme();

// Gestion des événements globaux
window.addEventListener('online', () => {
    showNotification('Connexion rétablie', 'success');
});

window.addEventListener('offline', () => {
    showNotification('Connexion perdue', 'warning');
});

// Export des fonctions utiles pour d'autres scripts
window.DevLearningHub = {
    showNotification,
    animateProgressBar,
    animateCounter,
    toggleTheme,
    debounce,
    throttle
};
