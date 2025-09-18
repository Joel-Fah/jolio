// Preload critical resources
(function () {
    const criticalResources = [
        '/static/unfold/fonts/inter/Inter-Regular.woff2',
        '/static/unfold/fonts/inter/Inter-SemiBold.woff2',
        '/static/unfold/fonts/material-symbols/Material-Symbols-Outlined.woff2'
    ];

    criticalResources.forEach(resource => {
        const link = document.createElement('link');
        link.rel = 'preload';
        link.href = resource;
        link.as = 'font';
        link.type = 'font/woff2';
        link.crossOrigin = 'anonymous';
        document.head.appendChild(link);
    });
})();