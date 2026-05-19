// Theme switching with smooth transition
function initTheme() {
    const btn = document.getElementById("theme-toggle");
    btn.onclick = () => {
        document.body.classList.toggle("light-mode");
        localStorage.setItem("theme", document.body.classList.contains("light-mode") ? "light" : "dark");
    };
}
document.addEventListener("DOMContentLoaded", initTheme);