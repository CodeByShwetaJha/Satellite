class HertZApp {
    constructor() {
        this.basePath = this.getBasePath();
        this.currentPage = 'home';
        this.loadingScreen = document.getElementById('loading-screen');
        
        this.init();
    }
    
    getBasePath() {
        const path = window.location.pathname;
        return path.substring(0, path.lastIndexOf("/") + 1);
    }
    
    async init() {
        console.log('🚀 Initializing HertZ Labs Application...');
        
        try {
            // Show loading screen
            this.showLoading();
            
            // Load components
            await Promise.all([
                this.loadComponent('header', 'header.html'),
                this.loadComponent('footer', 'footer.html')
            ]);
            
            // Initialize navigation
            this.initNavigation();
            
            // Load home page by default
            await this.loadPage('pages/home.html');
            
            // Initialize animations
            this.initAnimations();
            
            // Hide loading screen
            setTimeout(() => this.hideLoading(), 1000);
            
            console.log('✅ HertZ Labs Application Initialized Successfully!');
            
        } catch (error) {
            console.error('❌ Application initialization failed:', error);
            this.hideLoading();
        }
    }
    
    showLoading() {
        if (this.loadingScreen) {
            this.loadingScreen.classList.remove('hidden');
        }
    }
    
    hideLoading() {
        if (this.loadingScreen) {
            this.loadingScreen.classList.add('hidden');
            setTimeout(() => {
                this.loadingScreen.style.display = 'none';
            }, 500);
        }
    }
    
    async loadComponent(elementId, componentPath) {
        try {
            const response = await fetch(this.basePath + componentPath);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const html = await response.text();
            const element = document.getElementById(elementId);
            
            if (element) {
                element.innerHTML = html;
                console.log(`✅ Component loaded: ${componentPath}`);
            }
            
        } catch (error) {
            console.warn(`⚠️ Component not found: ${componentPath}`);
        }
    }
    
    async loadPage(pagePath) {
        try {
            console.log(`🔄 Loading page: ${pagePath}`);
            
            const response = await fetch(this.basePath + pagePath);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            
            const html = await response.text();
            const mainContent = document.getElementById('main-content');
            
            if (mainContent) {
                // Fade out current content
                mainContent.style.opacity = '0';
                
                setTimeout(() => {
                    mainContent.innerHTML = html;
                    this.executeScripts(mainContent);
                    
                    // Fade in new content
                    mainContent.style.opacity = '1';
                    
                    // Trigger animations
                    this.triggerAnimations();
                    
                    console.log(`✅ Page loaded: ${pagePath}`);
                }, 150);
            }
            
        } catch (error) {
            console.error(`❌ Failed to load page: ${pagePath}`, error);
            this.showErrorPage();
        }
    }
    
    executeScripts(container) {
        const scripts = container.querySelectorAll('script');
        scripts.forEach(oldScript => {
            const newScript = document.createElement('script');
            
            if (oldScript.src) {
                newScript.src = oldScript.src;
            } else {
                newScript.textContent = oldScript.textContent;
            }
            
            oldScript.remove();
            container.appendChild(newScript);
        });
    }
    
    initNavigation() {
        document.addEventListener('click', (event) => {
            const link = event.target.closest('[data-page]');
            if (link) {
                event.preventDefault();
                const page = link.getAttribute('data-page');
                this.navigateToPage(page);
            }
        });
        
        // Handle browser back/forward
        window.addEventListener('popstate', (event) => {
            if (event.state && event.state.page) {
                this.loadPage(`pages/${event.state.page}.html`);
            }
        });
    }
    
    navigateToPage(page) {
        if (page === this.currentPage) return;
        
        this.currentPage = page;
        
        // Update browser history
        window.history.pushState(
            { page: page },
            '',
            `#${page.replace('/', '-')}`
        );
        
        // Load the page
        this.loadPage(`pages/${page}.html`);
        
        // Close mobile menu if open
        this.closeMobileMenu();
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    closeMobileMenu() {
        const navbarNav = document.querySelector('.navbar-nav');
        if (navbarNav) {
            navbarNav.classList.remove('active');
        }
    }
    
    initAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        this.observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
    }
    
    triggerAnimations() {
        // Re-observe elements for animations
        const animatedElements = document.querySelectorAll('.animate-on-scroll');
        animatedElements.forEach(element => {
            element.classList.remove('visible');
            this.observer.observe(element);
        });
    }
    
    showErrorPage() {
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.innerHTML = `
                <div class="error-page">
                    <h2>🚀 Houston, we have a problem!</h2>
                    <p>The page you're looking for seems to be lost in space.</p>
                    <button class="btn btn-primary" onclick="app.navigateToPage('home')">
                        Return to Base
                    </button>
                </div>
                <style>
                .error-page {
                    text-align: center;
                    padding: 100px 20px;
                    min-height: 60vh;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }
                .error-page h2 {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                    color: #4a90e2;
                }
                .error-page p {
                    font-size: 1.2rem;
                    color: rgba(255, 255, 255, 0.8);
                    margin-bottom: 2rem;
                }
                </style>
            `;
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    window.app = new HertZApp();
});

// Make navigation function globally available
window.loadContent = (page) => {
    if (window.app) {
        window.app.loadPage(`pages/${page}.html`);
    }
};