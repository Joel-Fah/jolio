// Performance utilities
(function () {
    'use strict';

    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Optimize font loading
    if ('fonts' in document) {
        Promise.all([
            document.fonts.load('400 1em Syne'),
            document.fonts.load('600 1em Syne'),
            document.fonts.load('800 1em Syne')
        ]).then(() => {
            document.body.classList.add('fonts-loaded');
        });
    }

    // Service worker for caching (optional)
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .catch(err => console.log('SW registration failed'));
        });
    }
})();