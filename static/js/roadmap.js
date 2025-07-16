// Roadmap Interactive Effects
document.addEventListener('DOMContentLoaded', function() {
    // Parallax effect for roadmap background - DISABLED
    function createParallaxEffect() {
        // Effet parallax désactivé pour une expérience plus statique
        return;
    }

    // Animate course nodes on scroll - DISABLED
    function animateOnScroll() {
        // Animation désactivée - les éléments sont maintenant visibles par défaut
        const courseNodes = document.querySelectorAll('.course-node');
        courseNodes.forEach(node => {
            // Rendre tous les éléments visibles immédiatement
            const children = node.querySelectorAll('.course-icon, .course-content h3, .course-content p, .course-meta, .course-progress-mini, .course-action');
            children.forEach(child => {
                child.style.opacity = '1';
                child.style.transform = 'translateY(0) scale(1)';
                child.style.transition = 'all 0.3s ease';
            });
        });
    }

    // Add floating particles effect
    function createFloatingParticles() {
        const particlesContainer = document.createElement('div');
        particlesContainer.className = 'floating-particles';
        particlesContainer.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            overflow: hidden;
        `;

        // Create particles
        for (let i = 0; i < 20; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 4 + 2}px;
                height: ${Math.random() * 4 + 2}px;
                background: rgba(0, 255, 136, ${Math.random() * 0.3 + 0.1});
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: float-particle ${Math.random() * 10 + 5}s infinite linear;
            `;
            particlesContainer.appendChild(particle);
        }

        document.body.appendChild(particlesContainer);
    }

    // Enhance course node interactions
    function enhanceInteractions() {
        const courseNodes = document.querySelectorAll('.course-node');
        
        courseNodes.forEach(node => {
            // Add ripple effect on click with smoother animation
            node.addEventListener('click', function(e) {
                const ripple = document.createElement('div');
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                ripple.style.cssText = `
                    position: absolute;
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                    background: rgba(0, 255, 136, 0.6);
                    left: ${x - 10}px;
                    top: ${y - 10}px;
                    animation: ripple 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
                    pointer-events: none;
                    z-index: 10;
                `;
                
                this.style.position = 'relative';
                this.appendChild(ripple);
                
                setTimeout(() => {
                    ripple.remove();
                }, 800);
            });

            // Add enhanced glow effect on hover
            node.addEventListener('mouseenter', function() {
                this.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                this.style.boxShadow = `
                    0 25px 80px rgba(0, 0, 0, 0.5),
                    0 0 50px rgba(0, 255, 136, 0.4),
                    0 0 100px rgba(0, 255, 136, 0.2)
                `;
                this.style.transform = 'translateY(-12px) scale(1.03)';
            });

            node.addEventListener('mouseleave', function() {
                this.style.transition = 'all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)';
                this.style.transform = 'translateY(0) scale(1)';
                
                // Reset to original shadow based on course status
                if (this.closest('.roadmap-course.completed')) {
                    this.style.boxShadow = '0 12px 40px rgba(0, 255, 136, 0.3), 0 0 30px rgba(0, 255, 136, 0.2)';
                } else if (this.closest('.roadmap-course.in-progress')) {
                    this.style.boxShadow = '0 12px 40px rgba(251, 191, 36, 0.25), 0 0 25px rgba(251, 191, 36, 0.15)';
                } else if (this.closest('.roadmap-course.available')) {
                    this.style.boxShadow = '0 12px 40px rgba(0, 212, 255, 0.25), 0 0 25px rgba(0, 212, 255, 0.15)';
                } else {
                    this.style.boxShadow = '0 6px 20px rgba(0, 0, 0, 0.15)';
                }
            });
        });
    }

    // Add progress bar animations - DISABLED
    function animateProgressBars() {
        // Animation des barres de progression désactivée
        const progressBars = document.querySelectorAll('.progress-fill-mini');
        progressBars.forEach(bar => {
            // Les barres de progression gardent leur largeur initiale sans animation
            const currentWidth = bar.style.width;
            bar.style.transition = 'all 0.3s ease';
        });
    }

    // Initialize all effects
    createParallaxEffect();
    animateOnScroll();
    createFloatingParticles();
    enhanceInteractions();
    animateProgressBars();
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes float-particle {
        0% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-100vh) rotate(360deg);
            opacity: 0;
        }
    }

    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        50% {
            opacity: 0.6;
        }
        100% {
            transform: scale(6);
            opacity: 0;
        }
    }

    .course-node.animate-in {
        animation: node-enter 1.2s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }

    @keyframes node-enter {
        0% {
            opacity: 0;
            transform: translateY(50px) scale(0.9);
            filter: blur(3px);
        }
        50% {
            opacity: 0.7;
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
            filter: blur(0);
        }
    }

    .course-icon {
        transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }

    .course-node:hover .course-icon {
        transform: scale(1.15) rotate(8deg);
        filter: drop-shadow(0 0 15px rgba(0, 255, 136, 0.6));
    }
`;
document.head.appendChild(style);
