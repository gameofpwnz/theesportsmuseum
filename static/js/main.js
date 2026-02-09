// Esports Museum - Main JavaScript

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.style.display = mobileMenu.style.display === 'block' ? 'none' : 'block';
        mobileMenuBtn.classList.toggle('active');
    });
}

// Global Search
const globalSearch = document.getElementById('globalSearch');
const searchResults = document.getElementById('searchResults');
let searchTimeout;

if (globalSearch) {
    globalSearch.addEventListener('input', (e) => {
        const query = e.target.value.trim();
        
        clearTimeout(searchTimeout);
        
        if (query.length < 2) {
            searchResults.classList.remove('active');
            return;
        }
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, 300);
    });
    
    // Close search results when clicking outside
    document.addEventListener('click', (e) => {
        if (!globalSearch.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.remove('active');
        }
    });
}

// Load search index
let searchIndex = [];

fetch('/static/search-index.json')
    .then(response => response.json())
    .then(data => {
        searchIndex = data;
    })
    .catch(error => console.error('Failed to load search index:', error));

async function performSearch(query) {
    try {
        const queryLower = query.toLowerCase();
        
        // Simple client-side search
        const results = searchIndex.filter(record => {
            return (
                record.title?.toLowerCase().includes(queryLower) ||
                record.description?.toLowerCase().includes(queryLower) ||
                record.steward?.toLowerCase().includes(queryLower) ||
                record.team?.toLowerCase().includes(queryLower) ||
                record.player?.toLowerCase().includes(queryLower) ||
                record.id?.toLowerCase().includes(queryLower) ||
                record.esport?.toLowerCase().includes(queryLower)
            );
        }).slice(0, 10); // Limit to 10 results
        
        if (results.length === 0) {
            searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: var(--color-text-tertiary);">No results found</div>';
            searchResults.classList.add('active');
            return;
        }
        
        searchResults.innerHTML = results.map(record => `
            <a href="${record.url}" class="search-result-item">
                ${record.primary_image 
                    ? `<img src="${record.primary_image}" alt="${record.title}">`
                    : '<div style="width: 60px; height: 60px; background: var(--color-bg-tertiary); border-radius: 4px;"></div>'
                }
                <div style="flex: 1;">
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">${record.title}</div>
                    <div style="font-size: 0.75rem; color: var(--color-text-tertiary);">
                        ${record.id} • ${record.esport.toUpperCase()}
                    </div>
                </div>
            </a>
        `).join('');
        
        searchResults.classList.add('active');
    } catch (error) {
        console.error('Search error:', error);
    }
}

// Smooth Scroll for Internal Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy Loading Images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// Back to Top Button (if implemented)
const backToTopBtn = document.getElementById('backToTop');
if (backToTopBtn) {
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 500) {
            backToTopBtn.style.opacity = '1';
            backToTopBtn.style.visibility = 'visible';
        } else {
            backToTopBtn.style.opacity = '0';
            backToTopBtn.style.visibility = 'hidden';
        }
    });
    
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Analytics - Record View Tracking
function trackRecordView(recordId) {
    // Could send to analytics service
    console.log('Record viewed:', recordId);
}

// Share Functionality
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Link copied to clipboard!');
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('Link copied to clipboard!');
    }
}

function showNotification(message) {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: var(--color-accent);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize
console.log('Esports Museum initialized');
