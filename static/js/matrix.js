// Effet Matrix Rain en arrière-plan
class MatrixRain {
    constructor() {
        this.canvas = document.getElementById('matrix-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン';
        this.fontSize = 14;
        this.columns = 0;
        this.drops = [];
        
        this.init();
        this.animate();
    }
    
    init() {
        // Ajuster la taille du canvas
        this.resize();
        window.addEventListener('resize', () => this.resize());
        
        // Initialiser les colonnes
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        this.drops = new Array(this.columns).fill(1);
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        this.drops = new Array(this.columns).fill(1);
    }
    
    draw() {
        // Fond semi-transparent pour l'effet de traînée
        this.ctx.fillStyle = 'rgba(10, 10, 10, 0.04)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Style du texte
        this.ctx.fillStyle = '#00ff41';
        this.ctx.font = `${this.fontSize}px monospace`;
        
        // Dessiner les caractères qui tombent
        for (let i = 0; i < this.drops.length; i++) {
            const char = this.characters[Math.floor(Math.random() * this.characters.length)];
            const x = i * this.fontSize;
            const y = this.drops[i] * this.fontSize;
            
            this.ctx.fillText(char, x, y);
            
            // Réinitialiser la goutte si elle atteint le bas ou de manière aléatoire
            if (y > this.canvas.height && Math.random() > 0.975) {
                this.drops[i] = 0;
            }
            
            this.drops[i]++;
        }
    }
    
    animate() {
        this.draw();
        setTimeout(() => this.animate(), 35);
    }
}

// Initialiser l'effet Matrix quand la page est chargée
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('matrix-canvas')) {
        new MatrixRain();
    }
});

// Animation de particules pour un effet supplémentaire
class ParticleSystem {
    constructor() {
        this.particles = [];
        this.maxParticles = 50;
        this.init();
    }
    
    init() {
        for (let i = 0; i < this.maxParticles; i++) {
            this.particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                life: Math.random()
            });
        }
        this.animate();
    }
    
    animate() {
        // Animation des particules (optionnelle)
        requestAnimationFrame(() => this.animate());
    }
}

// Effet de typing pour les titres
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

// Effet de glitch pour les éléments spéciaux
function glitchEffect(element) {
    const originalText = element.textContent;
    const glitchChars = '!<>-_\\/[]{}—=+*^?#________';
    
    let iterations = 0;
    const maxIterations = 10;
    
    const interval = setInterval(() => {
        element.textContent = originalText
            .split('')
            .map((char, index) => {
                if (index < iterations) {
                    return originalText[index];
                }
                return glitchChars[Math.floor(Math.random() * glitchChars.length)];
            })
            .join('');
        
        iterations += 1/3;
        
        if (iterations >= maxIterations) {
            clearInterval(interval);
            element.textContent = originalText;
        }
    }, 30);
}

// Fonction pour créer des effets de hover avancés
function addHoverEffects() {
    const cards = document.querySelectorAll('.card, .stats-card');
    
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
            this.style.transition = 'all 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}
