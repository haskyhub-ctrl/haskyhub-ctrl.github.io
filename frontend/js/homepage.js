// homepage.js
document.addEventListener('DOMContentLoaded', () => {
    // 1. Intersection Observer for Fade-In-Up Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -50px 0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const delay = el.getAttribute('data-delay');
                if (delay) {
                    setTimeout(() => {
                        el.classList.add('visible');
                    }, parseInt(delay));
                } else {
                    el.classList.add('visible');
                }
                observer.unobserve(el);
            }
        });
    }, observerOptions);

    document.querySelectorAll('.fade-in-up, .slide-up').forEach(el => {
        observer.observe(el);
    });

    // 2. Count-Up Animation
    const statsObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const counters = entry.target.querySelectorAll('.count-up');
                counters.forEach(counter => {
                    const targetText = counter.getAttribute('data-target');
                    if (!targetText) return;
                    
                    const target = parseFloat(targetText.replace(/,/g, ''));
                    const duration = 2000; // ms
                    const increment = target / (duration / 16); // 60fps
                    let current = 0;

                    const updateCounter = () => {
                        current += increment;
                        if (current < target) {
                            counter.innerText = Math.ceil(current).toLocaleString('vi-VN');
                            requestAnimationFrame(updateCounter);
                        } else {
                            counter.innerText = target.toLocaleString('vi-VN');
                        }
                    };

                    updateCounter();
                });
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const statsSection = document.getElementById('stats');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
    const heroContent = document.querySelector('.hp-hero-content');
    if (heroContent) {
        statsObserver.observe(heroContent);
    }
});
