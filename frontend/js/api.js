/**
 * FRAS API Wrapper
 * Handles all API communication with JWT authentication
 */

const API_BASE = `${window.location.origin}/api`;

class FrasAPI {
    constructor() {
        this.token = localStorage.getItem('fras_token');
    }

    setToken(token) {
        this.token = token;
        localStorage.setItem('fras_token', token);
    }

    clearToken() {
        this.token = null;
        localStorage.removeItem('fras_token');
        localStorage.removeItem('fras_user');
    }

    getUser() {
        const u = localStorage.getItem('fras_user');
        return u ? JSON.parse(u) : null;
    }

    setUser(user) {
        localStorage.setItem('fras_user', JSON.stringify(user));
    }

    isLoggedIn() {
        return !!this.token;
    }

    async fetch(endpoint, options = {}) {
        const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        try {
            const response = await fetch(url, {
                ...options,
                headers,
            });

            if (response.status === 401) {
                this.clearToken();
                if (!window.location.pathname.includes('login')) {
                    window.location.href = '/login.html';
                }
                throw new Error('Phiên đăng nhập đã hết hạn');
            }

            const data = await response.json();

            if (!response.ok) {
                let errMessage = 'Lỗi không xác định';
                if (data.detail) {
                    if (Array.isArray(data.detail)) {
                        errMessage = data.detail.map(e => `${e.loc ? e.loc.join('.') : ''}: ${e.msg}`).join(' | ');
                    } else {
                        errMessage = data.detail;
                    }
                }
                throw new Error(errMessage);
            }

            return data;
        } catch (error) {
            if (error.message === 'Failed to fetch') {
                throw new Error('Không thể kết nối đến server');
            }
            throw error;
        }
    }

    async get(endpoint) {
        return this.fetch(endpoint, { method: 'GET' });
    }

    async post(endpoint, body) {
        return this.fetch(endpoint, {
            method: 'POST',
            body: JSON.stringify(body),
        });
    }

    async put(endpoint, body) {
        return this.fetch(endpoint, {
            method: 'PUT',
            body: JSON.stringify(body),
        });
    }

    async delete(endpoint) {
        return this.fetch(endpoint, { method: 'DELETE' });
    }

    // Auth
    async login(email, password) {
        const data = await this.post('/auth/login', { email, password });
        this.setToken(data.access_token);
        this.setUser(data.user);
        return data;
    }

    async register(userData) {
        const data = await this.post('/auth/register', userData);
        this.setToken(data.access_token);
        this.setUser(data.user);
        return data;
    }

    async getMe() {
        const data = await this.get('/auth/me');
        this.setUser(data);
        return data;
    }

    logout() {
        this.clearToken();
        window.location.href = '/login.html';
    }
}

// Global instance
const api = new FrasAPI();

// Toast notification
function showToast(message, type = 'success') {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container';
        document.body.appendChild(container);
    }

    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
    };

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${icons[type] || ''}</span><span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Loading overlay
function showLoading(message = 'Đang xử lý...') {
    let overlay = document.getElementById('loading-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `<div class="loading-spinner"></div><p>${message}</p>`;
        document.body.appendChild(overlay);
    }
    overlay.style.display = 'flex';
    overlay.querySelector('p').textContent = message;
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) overlay.style.display = 'none';
}

// Format date
function formatDate(dateStr) {
    if (!dateStr) return 'N/A';
    const d = new Date(dateStr);
    return d.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

function formatDateTime(dateStr) {
    if (!dateStr) return 'N/A';
    const d = new Date(dateStr);
    return d.toLocaleDateString('vi-VN', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}

// Risk helpers
function getRiskLabel(level) {
    const lang = localStorage.getItem('fras_lang') || 'vi';
    if (lang === 'en') {
        const labels = { low: 'Low Risk', medium: 'Medium Risk', high: 'High Risk', critical: 'Critical Risk' };
        return labels[level] || level;
    }
    const labels = { low: 'Nguy cơ Thấp', medium: 'Nguy cơ Trung bình', high: 'Nguy cơ Cao', critical: 'Nguy cơ Rất cao' };
    return labels[level] || level;
}

function getRiskBadge(level) {
    return `<span class="badge badge-${level}">${getRiskLabel(level)}</span>`;
}

// Mobile nav toggle
function setupMobileNav() {
    const toggle = document.querySelector('.nav-mobile-toggle');
    const links = document.querySelector('.nav-links');
    if (toggle && links) {
        toggle.addEventListener('click', () => links.classList.toggle('mobile-open'));
    }
}

// =================== THEME TOGGLE ===================
function initTheme() {
    const saved = localStorage.getItem('fras_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('fras_theme', next);
    updateThemeButton();
}

function updateThemeButton() {
    const btn = document.getElementById('theme-toggle-btn');
    if (!btn) return;
    const theme = document.documentElement.getAttribute('data-theme') || 'dark';
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
    btn.title = theme === 'dark' ? 'Light mode' : 'Dark mode';
}

// =================== LANGUAGE TOGGLE ===================
const i18n = {
    vi: {
        dashboard: 'Bảng điều khiển',
        history: 'Lịch sử',
        admin: 'Quản trị',
        home: 'Trang chủ',
        logout: 'Đăng xuất',
        login: 'Đăng nhập',
        loading: 'Đang xử lý...',
        risk_low: 'Nguy cơ Thấp',
        risk_medium: 'Nguy cơ Trung bình',
        risk_high: 'Nguy cơ Cao',
        risk_critical: 'Nguy cơ Rất cao',
    },
    en: {
        dashboard: 'Dashboard',
        history: 'History',
        admin: 'Admin',
        home: 'Home',
        logout: 'Logout',
        login: 'Login',
        loading: 'Processing...',
        risk_low: 'Low Risk',
        risk_medium: 'Medium Risk',
        risk_high: 'High Risk',
        risk_critical: 'Critical Risk',
    }
};

function getLang() {
    return localStorage.getItem('fras_lang') || 'vi';
}

function t(key) {
    const lang = getLang();
    return (i18n[lang] && i18n[lang][key]) || (i18n['vi'][key]) || key;
}

function toggleLanguage() {
    const current = getLang();
    const next = current === 'vi' ? 'en' : 'vi';
    localStorage.setItem('fras_lang', next);
    updateLangButton();
    // Reload page so all content re-renders
    location.reload();
}

function updateLangButton() {
    const btn = document.getElementById('lang-toggle-btn');
    if (!btn) return;
    const lang = getLang();
    btn.textContent = lang === 'vi' ? 'EN' : 'VI';
    btn.title = lang === 'vi' ? 'Switch to English' : 'Chuyển sang Tiếng Việt';
}

// Setup navbar based on auth state
function setupNavbar() {
    // Init theme first
    initTheme();

    const user = api.getUser();
    const navUser = document.querySelector('.nav-user');
    const navLinks = document.querySelector('.nav-links');

    if (user && navLinks) {
        const isAdmin = user.role === 'admin' || user.role === 'superadmin';

        if (!isAdmin) {
            // Normal User Links
            const dashLink = document.createElement('li');
            dashLink.innerHTML = `<a href="/dashboard.html">${t('dashboard')}</a>`;
            const histLink = document.createElement('li');
            histLink.innerHTML = `<a href="/history.html">${t('history')}</a>`;

            if (!navLinks.querySelector('a[href="/dashboard.html"]')) {
                navLinks.insertBefore(dashLink, navLinks.firstChild);
                navLinks.insertBefore(histLink, dashLink.nextSibling);

                const mapLink = document.createElement('li');
                mapLink.innerHTML = `<a href="/map.html">Bản đồ</a>`;
                navLinks.insertBefore(mapLink, histLink.nextSibling);
            }
        } else {
            // Admin Links
            if (!navLinks.querySelector('a[href="/admin/"]')) {
                const adminLink = document.createElement('li');
                adminLink.innerHTML = `<a href="/admin/">Bảng điều khiển Admin</a>`;
                navLinks.insertBefore(adminLink, navLinks.firstChild);
                
                const mapLink = document.createElement('li');
                mapLink.innerHTML = `<a href="/map.html">Bản đồ Rủi ro</a>`;
                navLinks.insertBefore(mapLink, adminLink.nextSibling);
            }
        }
    }

    if (navUser) {
        // Insert controls before user info
        const controls = document.createElement('div');
        controls.className = 'nav-controls';
        controls.innerHTML = `
            <button class="ctrl-btn" id="lang-toggle-btn" onclick="toggleLanguage()" title=""></button>
            <button class="ctrl-btn" id="theme-toggle-btn" onclick="toggleTheme()" title=""></button>
        `;

        if (user) {
            navUser.innerHTML = '';
            // Notification bell
            const notifBell = document.createElement('div');
            notifBell.className = 'notif-bell';
            notifBell.innerHTML = `
                <a href="#" onclick="toggleNotifPanel(event)" title="Thông báo" style="position:relative;font-size:1.3rem;text-decoration:none;">
                    🔔<span class="notif-badge" id="notif-badge" style="display:none;">0</span>
                </a>
                <div class="notif-panel" id="notif-panel" style="display:none;">
                    <div class="notif-panel-header">
                        <span style="font-weight:600;">Thông báo</span>
                        <a href="#" onclick="markAllRead(event)" style="font-size:0.8rem;">Đã đọc tất cả</a>
                    </div>
                    <div class="notif-panel-body" id="notif-panel-body">Đang tải...</div>
                </div>
            `;
            navUser.appendChild(notifBell);
            navUser.appendChild(controls);
            const userSpan = document.createElement('span');
            userSpan.className = 'user-name';
            userSpan.textContent = user.full_name;
            navUser.appendChild(userSpan);
            const logoutBtn = document.createElement('button');
            logoutBtn.className = 'btn btn-sm btn-secondary';
            logoutBtn.textContent = t('logout');
            logoutBtn.onclick = () => api.logout();
            navUser.appendChild(logoutBtn);
            // Start polling notifications
            loadNotifCount();
            setInterval(loadNotifCount, 30000);
        } else {
            navUser.innerHTML = '';
            navUser.appendChild(controls);
            const loginLink = document.createElement('a');
            loginLink.href = '/login.html';
            loginLink.className = 'btn btn-sm btn-primary';
            loginLink.textContent = t('login');
            navUser.appendChild(loginLink);
        }

        updateThemeButton();
        updateLangButton();
    }

    setupMobileNav();
}

// Require auth - redirect if not logged in
function requireAuth() {
    if (!api.isLoggedIn()) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

// DOMContentLoaded helper
function onReady(fn) {
    if (document.readyState !== 'loading') {
        fn();
    } else {
        document.addEventListener('DOMContentLoaded', fn);
    }
}

// Initialize theme on script load (before DOM ready for flash prevention)
initTheme();

// =================== NOTIFICATION SYSTEM ===================
async function loadNotifCount() {
    try {
        const data = await api.get('/notifications/unread-count');
        const badge = document.getElementById('notif-badge');
        if (badge) {
            if (data.count > 0) {
                badge.textContent = data.count > 9 ? '9+' : data.count;
                badge.style.display = 'flex';
            } else {
                badge.style.display = 'none';
            }
        }
    } catch (e) { }
}

function toggleNotifPanel(e) {
    e.preventDefault();
    const panel = document.getElementById('notif-panel');
    if (panel.style.display === 'none') {
        panel.style.display = 'block';
        loadNotifList();
    } else {
        panel.style.display = 'none';
    }
}

async function loadNotifList() {
    try {
        const data = await api.get('/notifications');
        const body = document.getElementById('notif-panel-body');
        if (!data.length) {
            body.innerHTML = '<div style="padding:24px; text-align:center; color:var(--text-muted);">Không có thông báo</div>';
            return;
        }
        body.innerHTML = data.slice(0, 10).map(n => `
            <div class="notif-item ${n.is_read ? '' : 'unread'}" onclick="${n.link ? `window.location.href='${n.link}'` : ''}">
                <div class="notif-title">${n.title}</div>
                <div class="notif-msg">${n.message}</div>
                <div class="notif-time">${formatDate(n.created_at)}</div>
            </div>
        `).join('');
    } catch (e) {
        document.getElementById('notif-panel-body').innerHTML = '<div style="padding:16px; text-align:center; color:var(--text-muted);">Lỗi tải thông báo</div>';
    }
}

async function markAllRead(e) {
    e.preventDefault();
    try {
        await api.put('/notifications/read-all', {});
        loadNotifCount();
        loadNotifList();
    } catch (e) { }
}

// Close notification panel when clicking outside
document.addEventListener('click', function (e) {
    const panel = document.getElementById('notif-panel');
    const bell = document.querySelector('.notif-bell');
    if (panel && bell && !bell.contains(e.target)) {
        panel.style.display = 'none';
    }
});

// ========== Auto-load Global AI Chatbot ==========
(function() {
    const s = document.createElement('script');
    s.src = '/js/chatbot.js?v=' + Date.now();
    s.defer = true;
    document.body ? document.body.appendChild(s) : document.addEventListener('DOMContentLoaded', () => document.body.appendChild(s));
})();
