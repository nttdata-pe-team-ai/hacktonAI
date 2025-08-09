// ProfeAI JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Add form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc2626';
                    
                    // Remove error styling when user starts typing
                    field.addEventListener('input', function() {
                        this.style.borderColor = '';
                    }, { once: true });
                }
            });

            if (!isValid) {
                e.preventDefault();
                showMessage('Please fill in all required fields', 'error');
            }
        });
    });

    // Add loading states to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (this.form && this.form.checkValidity()) {
                const originalText = this.textContent;
                this.textContent = 'Loading...';
                this.disabled = true;

                // Re-enable button after 10 seconds as fallback
                setTimeout(() => {
                    this.textContent = originalText;
                    this.disabled = false;
                }, 10000);
            }
        });
    });

    // Add progress animation
    const progressBars = document.querySelectorAll('.progress-fill');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = width;
        }, 500);
    });

    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.welcome-card, .registration-form, .progress-card, .actions-card, .lessons-card, .getting-started-card, .lesson-content');
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Enhanced feedback button interactions
    const feedbackButtons = document.querySelectorAll('.btn-feedback');
    feedbackButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add click effect
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);

            // Show confirmation message
            const feedbackType = this.querySelector('input[name="feedback_type"]').value;
            let message = '';
            
            switch(feedbackType) {
                case 'clear':
                    message = 'Thanks! Glad this was helpful! 😊';
                    break;
                case 'confused':
                    message = 'I\'ll generate a clearer explanation for you! 🔄';
                    break;
                case 'frustrated':
                    message = 'Let me try a different approach! 💪';
                    break;
            }
            
            if (message) {
                showMessage(message, 'info');
            }
        });
    });

    // Add hover effects to lesson items
    const lessonItems = document.querySelectorAll('.lesson-item');
    lessonItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // ESC key to go back
        if (e.key === 'Escape') {
            const backLink = document.querySelector('.back-link');
            if (backLink) {
                window.location.href = backLink.href;
            }
        }

        // Enter key on buttons
        if (e.key === 'Enter' && e.target.classList.contains('btn-primary')) {
            e.target.click();
        }
    });

    // Add copy-to-clipboard functionality for code blocks
    const codeBlocks = document.querySelectorAll('pre');
    codeBlocks.forEach(block => {
        const button = document.createElement('button');
        button.textContent = 'Copy';
        button.className = 'copy-btn';
        button.style.cssText = `
            position: absolute;
            top: 0.5rem;
            right: 0.5rem;
            background: var(--primary-color);
            color: white;
            border: none;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            cursor: pointer;
            opacity: 0.7;
            transition: opacity 0.2s;
        `;

        block.style.position = 'relative';
        block.appendChild(button);

        button.addEventListener('click', async function() {
            try {
                await navigator.clipboard.writeText(block.textContent.replace('Copy', '').trim());
                this.textContent = 'Copied!';
                setTimeout(() => {
                    this.textContent = 'Copy';
                }, 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
                showMessage('Failed to copy to clipboard', 'error');
            }
        });

        button.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
        });

        button.addEventListener('mouseleave', function() {
            this.style.opacity = '0.7';
        });
    });
});

// Utility function to show messages
function showMessage(text, type = 'info') {
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem;
        border-radius: 0.5rem;
        font-weight: 500;
        z-index: 1000;
        min-width: 200px;
        max-width: 400px;
        box-shadow: var(--shadow-lg);
        animation: slideIn 0.3s ease;
    `;

    // Set colors based on type
    switch(type) {
        case 'success':
            message.style.background = '#dcfce7';
            message.style.border = '1px solid #16a34a';
            message.style.color = '#15803d';
            break;
        case 'error':
            message.style.background = '#fef2f2';
            message.style.border = '1px solid #dc2626';
            message.style.color = '#dc2626';
            break;
        case 'info':
        default:
            message.style.background = '#dbeafe';
            message.style.border = '1px solid #2563eb';
            message.style.color = '#1d4ed8';
            break;
    }

    document.body.appendChild(message);

    // Auto-remove after 4 seconds
    setTimeout(() => {
        message.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(message);
        }, 300);
    }, 4000);
}

// Add slide animations
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