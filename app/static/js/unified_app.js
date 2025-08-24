/**
 * Unified Crime Hotspot Application JavaScript Framework
 * Consistent functionality and state management across all pages
 */

class CrimeHotspotApp {
    constructor() {
        this.currentUser = null;
        this.currentPage = null;
        this.notifications = [];
        this.eventListeners = new Map();
        this.components = new Map();
        this.apiCache = new Map();
        
        this.init();
    }
    
    init() {
        console.log('🚀 Initializing Crime Hotspot Application...');
        
        // Initialize core functionality
        this.detectCurrentPage();
        this.initializeNavigation();
        this.initializeNotifications();
        this.initializeTheme();
        this.initializeAuth();
        this.initializeGlobalEventListeners();
        
        // Initialize page-specific functionality
        this.initializePageSpecific();
        
        console.log('✅ Crime Hotspot Application initialized successfully');
    }
    
    detectCurrentPage() {
        const path = window.location.pathname;
        
        if (path === '/' || path === '/index') {
            this.currentPage = 'home';
        } else if (path.includes('/auth/login')) {
            this.currentPage = 'login';
        } else if (path.includes('/auth/signup')) {
            this.currentPage = 'signup';
        } else if (path.includes('/advanced-map')) {
            this.currentPage = 'advanced-map';
        } else if (path.includes('/pattern-analysis')) {
            this.currentPage = 'pattern-analysis';
        } else if (path.includes('/ai-predictions')) {
            this.currentPage = 'ai-dashboard';
        } else if (path.includes('/map')) {
            this.currentPage = 'basic-map';
        } else {
            this.currentPage = 'unknown';
        }
        
        console.log(`📍 Current page detected: ${this.currentPage}`);
        document.body.setAttribute('data-page', this.currentPage);
    }
    
    initializeNavigation() {
        // Add active state to current navigation item
        const navLinks = document.querySelectorAll('.unified-nav-link, .nav-link');
        const currentPath = window.location.pathname;
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href) && href !== '/') {
                link.classList.add('active');
            }
        });
        
        // Initialize dropdown menus
        this.initializeDropdowns();
        
        // Initialize mobile navigation
        this.initializeMobileNav();
    }
    
    initializeDropdowns() {
        const dropdownToggles = document.querySelectorAll('[data-bs-toggle="dropdown"]');
        
        dropdownToggles.forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.preventDefault();
                const dropdown = toggle.nextElementSibling;
                if (dropdown && dropdown.classList.contains('dropdown-menu')) {
                    dropdown.classList.toggle('show');
                }
            });
        });
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    }
    
    initializeMobileNav() {
        const navToggle = document.querySelector('.navbar-toggler');
        const navCollapse = document.querySelector('.navbar-collapse');
        
        if (navToggle && navCollapse) {
            navToggle.addEventListener('click', () => {
                navCollapse.classList.toggle('show');
            });
        }
    }
    
    initializeNotifications() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('unified-notifications')) {
            const container = document.createElement('div');
            container.id = 'unified-notifications';
            container.className = 'unified-notifications-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
                pointer-events: none;
            `;
            document.body.appendChild(container);
        }
    }
    
    showNotification(message, type = 'info', duration = 5000) {
        const container = document.getElementById('unified-notifications');
        if (!container) return;
        
        const notification = document.createElement('div');
        const id = 'notification-' + Date.now();
        notification.id = id;
        notification.className = `unified-alert unified-alert-${type} fade-in`;
        notification.style.cssText = `
            margin-bottom: 10px;
            pointer-events: auto;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease-out;
        `;
        
        const icon = this.getNotificationIcon(type);
        notification.innerHTML = `
            <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                <i class="fas ${icon}" style="margin-top: 2px;"></i>
                <div style="flex: 1;">
                    <div>${message}</div>
                </div>
                <button onclick="crimeApp.dismissNotification('${id}')" 
                        style="background: none; border: none; color: inherit; cursor: pointer; padding: 0; margin-left: 0.5rem;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        container.appendChild(notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        });
        
        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                this.dismissNotification(id);
            }, duration);
        }
        
        this.notifications.push({ id, element: notification, type, message });
    }
    
    dismissNotification(id) {
        const notification = document.getElementById(id);
        if (notification) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
            
            this.notifications = this.notifications.filter(n => n.id !== id);
        }
    }
    
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            warning: 'fa-exclamation-triangle',
            danger: 'fa-exclamation-circle',
            info: 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }
    
    initializeTheme() {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('crime-app-theme') || 'light';
        this.setTheme(savedTheme);
        
        // Add theme toggle functionality
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                this.setTheme(newTheme);
            });
        }
    }
    
    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('crime-app-theme', theme);
        
        // Update theme toggle icon
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const icon = themeToggle.querySelector('i');
            if (icon) {
                icon.className = theme === 'light' ? 'fas fa-moon' : 'fas fa-sun';
            }
        }
    }
    
    initializeAuth() {
        // Check authentication status
        this.checkAuthStatus();
        
        // Initialize login form if present
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            this.initializeLoginForm(loginForm);
        }
        
        // Initialize logout functionality
        const logoutLinks = document.querySelectorAll('[href*="logout"]');
        logoutLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.logout();
            });
        });
    }
    
    checkAuthStatus() {
        // Check if user is logged in based on page content
        const userMenu = document.querySelector('.user-menu');
        const loginLink = document.querySelector('[href*="login"]');
        
        if (userMenu && !loginLink) {
            this.currentUser = { authenticated: true };
        } else {
            this.currentUser = { authenticated: false };
        }
    }
    
    initializeLoginForm(form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            const submitButton = form.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;

            // Show loading state
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Signing in...';

            try {
                // Let the form submit normally after a brief delay
                setTimeout(() => {
                    form.submit();
                }, 500);

            } catch (error) {
                console.error('Login error:', error);
                this.showNotification('Login failed. Please try again.', 'danger');

                // Restore button state
                submitButton.disabled = false;
                submitButton.textContent = originalText;
            }
        });
    }
    
    logout() {
        // Show confirmation
        if (confirm('Are you sure you want to log out?')) {
            window.location.href = '/auth/logout';
        }
    }
    
    initializeGlobalEventListeners() {
        // Handle page transitions
        window.addEventListener('beforeunload', () => {
            this.savePageState();
        });
        
        // Handle resize events
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize();
        }, 250));
        
        // Handle keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
        
        // Handle form validation
        document.addEventListener('submit', (e) => {
            this.handleFormSubmission(e);
        });
    }
    
    handleResize() {
        // Trigger resize events for components
        this.components.forEach((component, name) => {
            if (component.handleResize) {
                component.handleResize();
            }
        });
    }
    
    handleKeyboardShortcuts(e) {
        // Global keyboard shortcuts
        if (e.ctrlKey || e.metaKey) {
            switch (e.key) {
                case 'k':
                    e.preventDefault();
                    this.openSearch();
                    break;
                case '/':
                    e.preventDefault();
                    this.openHelp();
                    break;
            }
        }
        
        // Escape key to close modals/dropdowns
        if (e.key === 'Escape') {
            this.closeAllModals();
        }
    }
    
    handleFormSubmission(e) {
        const form = e.target;
        if (!form.checkValidity()) {
            e.preventDefault();
            this.showFormErrors(form);
        }
    }
    
    showFormErrors(form) {
        const invalidFields = form.querySelectorAll(':invalid');
        if (invalidFields.length > 0) {
            const firstInvalid = invalidFields[0];
            firstInvalid.focus();
            
            const fieldName = firstInvalid.getAttribute('name') || 'field';
            this.showNotification(`Please check the ${fieldName} field.`, 'warning');
        }
    }
    
    initializePageSpecific() {
        switch (this.currentPage) {
            case 'home':
                this.initializeHomePage();
                break;
            case 'advanced-map':
                this.initializeAdvancedMap();
                break;
            case 'pattern-analysis':
                this.initializePatternAnalysis();
                break;
            case 'ai-dashboard':
                this.initializeAIDashboard();
                break;
            case 'basic-map':
                this.initializeBasicMap();
                break;
            case 'login':
                this.initializeLoginPage();
                break;
        }
    }
    
    initializeHomePage() {
        console.log('🏠 Initializing home page...');
        // Add any home page specific functionality
    }
    
    initializeAdvancedMap() {
        console.log('🗺️ Initializing advanced map...');
        // Advanced map will be initialized by its own script
        // This is just for integration
    }
    
    initializePatternAnalysis() {
        console.log('🧠 Initializing pattern analysis...');
        // Pattern analysis will be initialized by its own script
    }
    
    initializeAIDashboard() {
        console.log('📊 Initializing AI dashboard...');
        // AI dashboard will be initialized by its own script
    }
    
    initializeBasicMap() {
        console.log('🗺️ Initializing basic map...');
        // Basic map functionality
    }
    
    initializeLoginPage() {
        console.log('🔐 Initializing login page...');
        // Add login page specific enhancements
    }
    
    // Utility methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    async apiCall(endpoint, options = {}) {
        const cacheKey = `${endpoint}-${JSON.stringify(options)}`;
        
        // Check cache first
        if (this.apiCache.has(cacheKey)) {
            const cached = this.apiCache.get(cacheKey);
            if (Date.now() - cached.timestamp < 300000) { // 5 minutes
                return cached.data;
            }
        }
        
        try {
            const response = await fetch(endpoint, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // Cache the result
            this.apiCache.set(cacheKey, {
                data,
                timestamp: Date.now()
            });
            
            return data;
            
        } catch (error) {
            console.error('API call failed:', error);
            this.showNotification('Failed to load data. Please try again.', 'danger');
            throw error;
        }
    }
    
    savePageState() {
        const state = {
            page: this.currentPage,
            timestamp: Date.now(),
            scrollPosition: window.scrollY
        };
        
        sessionStorage.setItem('crime-app-state', JSON.stringify(state));
    }
    
    restorePageState() {
        const saved = sessionStorage.getItem('crime-app-state');
        if (saved) {
            try {
                const state = JSON.parse(saved);
                if (state.scrollPosition) {
                    window.scrollTo(0, state.scrollPosition);
                }
            } catch (error) {
                console.warn('Failed to restore page state:', error);
            }
        }
    }
    
    openSearch() {
        // Implement global search functionality
        console.log('🔍 Opening search...');
    }
    
    openHelp() {
        // Implement help system
        console.log('❓ Opening help...');
    }
    
    closeAllModals() {
        // Close any open modals or dropdowns
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            menu.classList.remove('show');
        });
        
        document.querySelectorAll('.modal.show').forEach(modal => {
            modal.classList.remove('show');
        });
    }
    
    registerComponent(name, component) {
        this.components.set(name, component);
        console.log(`📦 Registered component: ${name}`);
    }
    
    getComponent(name) {
        return this.components.get(name);
    }
}

// Initialize the global application instance
let crimeApp;

document.addEventListener('DOMContentLoaded', function() {
    crimeApp = new CrimeHotspotApp();
    
    // Make it globally accessible
    window.crimeApp = crimeApp;
    
    // Restore page state after initialization
    setTimeout(() => {
        crimeApp.restorePageState();
    }, 100);
});

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CrimeHotspotApp;
}
