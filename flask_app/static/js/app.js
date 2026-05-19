// Main Application JS - Theme, Navigation, Utilities
document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    animateCounters();
});

function initTheme() {
    const toggle = document.getElementById("theme-toggle");
    if (!toggle) return;

    // Restore theme from localStorage
    const savedTheme = localStorage.getItem("theme") || "dark";
    applyTheme(savedTheme);

    // Toggle theme on click
    toggle.addEventListener("click", () => {
        const isLightMode = document.body.classList.contains("light-mode");
        const newTheme = isLightMode ? "dark" : "light";
        applyTheme(newTheme);
        localStorage.setItem("theme", newTheme);
    });
}

function applyTheme(theme) {
    const toggle = document.getElementById("theme-toggle");
    const htmlElement = document.documentElement;
    
    if (theme === "light") {
        document.body.classList.add("light-mode");
        htmlElement.setAttribute("data-theme", "light");
        htmlElement.style.colorScheme = "light";
        if (toggle) {
            toggle.textContent = "🌙";
            toggle.title = "Switch to Dark Mode";
        }
    } else {
        document.body.classList.remove("light-mode");
        htmlElement.setAttribute("data-theme", "dark");
        htmlElement.style.colorScheme = "dark";
        if (toggle) {
            toggle.textContent = "🌞";
            toggle.title = "Switch to Light Mode";
        }
    }
}

function animateCounters() {
    // Animated counters
    document.querySelectorAll(".counter").forEach(el => {
        const target = parseInt(el.innerText);
        if (!isNaN(target)) {
            animateCounter(el, target);
        }
    });
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 60;
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.innerText = target;
            clearInterval(timer);
        } else {
            element.innerText = Math.floor(current);
        }
    }, 16);
}