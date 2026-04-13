(function() {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
})();

function toggleTheme() {
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    updateToggleIcon();
}

function updateToggleIcon() {
    const btn = document.querySelector('.theme-toggle');
    if (!btn) return;
    btn.innerHTML = '🌙 Dark Locked';
    btn.setAttribute('disabled', 'disabled');
}

document.addEventListener('DOMContentLoaded', updateToggleIcon);
