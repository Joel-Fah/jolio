document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("page-transition");

    // On page load, start with overlay fully visible, then animate out
    overlay.classList.add("transition-in");
    overlay.classList.remove("transition-out");
    overlay.style.setProperty("--x", "100vw");
    overlay.style.setProperty("--y", "100vh");

    requestAnimationFrame(() => {
        overlay.classList.remove("transition-in");
        overlay.classList.add("transition-out");
    });

    document.querySelectorAll("a").forEach(anchor => {
        anchor.addEventListener("click", (e) => {
            const href = anchor.getAttribute("href");
            if (!href || href.startsWith("#") || href.startsWith("javascript:")) return;

            e.preventDefault();

            // Set origin to click position
            overlay.style.setProperty("--x", `${e.clientX}px`);
            overlay.style.setProperty("--y", `${e.clientY}px`);

            overlay.classList.remove("transition-out");
            overlay.classList.add("transition-in");

            setTimeout(() => {
                window.location.href = href;
            }, 1500);
        });
    });
});