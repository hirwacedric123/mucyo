// Initialize Lucide icons
lucide.createIcons();

// DOM elements
const navbar = document.getElementById('navbar');
const navDesktop = document.querySelector('.nav-desktop');
const navMobile = document.querySelector('.nav-mobile');
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mobileMenu = document.getElementById('mobileMenu');

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    
    if (scrollTop > 50) {
        navDesktop?.classList.add('scrolled');
        navMobile?.classList.add('scrolled');
    } else {
        navDesktop?.classList.remove('scrolled');
        navMobile?.classList.remove('scrolled');
    }
});

// Mobile menu toggle
if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        mobileMenu.classList.toggle('active');
        
        // Immediate icon toggle
        if (mobileMenu.classList.contains('active')) {
            mobileMenuBtn.innerHTML = '<i data-lucide="x"></i>';
        } else {
            mobileMenuBtn.innerHTML = '<i data-lucide="menu"></i>';
        }
        lucide.createIcons();
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.mobile-nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (mobileMenu) {
            mobileMenu.classList.remove('active');
            if (mobileMenuBtn) {
                mobileMenuBtn.innerHTML = '<i data-lucide="menu"></i>';
                lucide.createIcons();
            }
        }
    });
});

// Close mobile menu when clicking outside
document.addEventListener('click', (e) => {
    if (mobileMenu && mobileMenuBtn && 
        !mobileMenu.contains(e.target) && 
        !mobileMenuBtn.contains(e.target) && 
        mobileMenu.classList.contains('active')) {
        mobileMenu.classList.remove('active');
        mobileMenuBtn.innerHTML = '<i data-lucide="menu"></i>';
        lucide.createIcons();
    }
});

// Smooth scrolling for navigation links
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

// File input styling and validation
const fileInput = document.getElementById('file');
if (fileInput) {
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Check file size (16MB = 16 * 1024 * 1024 bytes)
            const maxSize = 16 * 1024 * 1024;
            if (file.size > maxSize) {
                alert('File size exceeds 16MB limit. Please choose a smaller file.');
                this.value = '';
                return;
            }
            
            // Check file type
            const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!allowedTypes.includes(file.type)) {
                alert('Invalid file type. Please upload a PDF or DOCX file.');
                this.value = '';
                return;
            }
        }
    });
}

// Language selection validation
const sourceLanguageSelect = document.getElementById('source_language');
const targetLanguageSelect = document.getElementById('target_language');

function validateLanguageSelection() {
    if (sourceLanguageSelect && targetLanguageSelect) {
        const sourceValue = sourceLanguageSelect.value;
        const targetValue = targetLanguageSelect.value;
        
        if (sourceValue && targetValue && sourceValue === targetValue) {
            // Show error styling
            sourceLanguageSelect.style.borderColor = '#dc2626';
            targetLanguageSelect.style.borderColor = '#dc2626';
            return false;
        } else {
            // Reset styling
            sourceLanguageSelect.style.borderColor = '';
            targetLanguageSelect.style.borderColor = '';
            return true;
        }
    }
    return true;
}

if (sourceLanguageSelect) {
    sourceLanguageSelect.addEventListener('change', validateLanguageSelection);
}

if (targetLanguageSelect) {
    targetLanguageSelect.addEventListener('change', validateLanguageSelection);
}

// Continue button functionality
const continueBtn = document.getElementById('continueBtn');
const translationFormContainer = document.getElementById('translationFormContainer');

if (continueBtn && translationFormContainer) {
    continueBtn.addEventListener('click', function() {
        this.style.display = 'none';
        translationFormContainer.style.display = 'block';
        translationFormContainer.scrollIntoView({ behavior: 'smooth' });
    });
}

// Form submission with loading state and validation
const translationForm = document.querySelector('.translation-form');
if (translationForm) {
    translationForm.addEventListener('submit', function(e) {
        // Validate language selection
        if (!validateLanguageSelection()) {
            e.preventDefault();
            alert('Source and target languages cannot be the same. Please select different languages.');
            return;
        }
        
        const submitButton = this.querySelector('button[type="submit"]');
        if (submitButton) {
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<div class="loading-spinner"></div> Translating...';
            submitButton.disabled = true;
            
            // Re-enable if form submission fails (shouldn't happen, but just in case)
            setTimeout(() => {
                if (submitButton.disabled) {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                    lucide.createIcons();
                }
            }, 30000); // 30 second timeout
        }
    });
}

// Auto-hide flash messages after 5 seconds
setTimeout(() => {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        msg.style.transition = 'opacity 0.5s ease-out';
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 500);
    });
}, 5000);

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide icons
    lucide.createIcons();
    
    console.log('Student Translator MVP loaded successfully!');
});

