// FlavorFinder Enhanced UI - Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize page loader
    initPageLoader();
    
    // Initialize animations on scroll
    initScrollAnimations();
    
    // Initialize back to top button
    initBackToTop();
    
    // Initialize tooltips and popovers
    initTooltips();
    
    // Initialize responsive navigation
    initResponsiveNav();
    
    // Initialize form validations
    initFormValidations();
    
    // Initialize custom alerts
    initCustomAlerts();
    
    // Initialize smooth scrolling
    initSmoothScroll();
});

// Page loader functionality
function initPageLoader() {
    const loader = document.querySelector('.page-loader');
    if (!loader) return;
    
    // Hide loader after page load
    window.addEventListener('load', function() {
        setTimeout(function() {
            loader.classList.add('loaded');
        }, 500);
    });
}

// Animations on scroll
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                // Optional: stop observing after animation
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize tooltips and popovers
function initTooltips() {
    // Using Bootstrap's built-in tooltip and popover functionality
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Responsive navigation
function initResponsiveNav() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Change navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentLocation || currentLocation.includes(href) && href !== '/') {
            link.classList.add('active');
        }
    });
}

// Form validations
function initFormValidations() {
    const forms = document.querySelectorAll('.needs-validation');
    
    if (forms.length === 0) return;
    
    Array.from(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Custom alerts
function initCustomAlerts() {
    // Find all dismissible alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(function(alert) {
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });
}

// Smooth scroll to anchors
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (!target) return;
            
            window.scrollTo({
                top: target.offsetTop - 80, // Offset for fixed navbar
                behavior: 'smooth'
            });
        });
    });
}

// Create custom toast notification
function showToast(title, message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set toast color based on type
    let bgColor = '#4ECDC4';
    switch(type) {
        case 'success':
            bgColor = '#6BFF98';
            break;
        case 'danger':
        case 'error':
            bgColor = '#FF6B6B';
            break;
        case 'warning':
            bgColor = '#FFD166';
            break;
    }
    
    // Create toast content
    toast.innerHTML = `
        <div class="toast-header" style="background-color: ${bgColor}">
            <strong class="me-auto">${title}</strong>
            <small>Just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    // Add toast to container
    toastContainer.appendChild(toast);
    
    // Remove toast after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 5000);
    
    // Add click event to close button
    const closeBtn = toast.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    });
}

// Favorite recipe functionality
function initFavoriteButtons() {
    const favButtons = document.querySelectorAll('.favorite-btn');
    
    favButtons.forEach(button => {
        button.addEventListener('click', function() {
            const mealId = this.getAttribute('data-meal-id');
            const mealName = this.getAttribute('data-meal-name');
            const action = this.classList.contains('active') ? 'remove' : 'add';
            
            // Toggle active class immediately for better UX
            this.classList.toggle('active');
            
            // Update button text
            if (this.classList.contains('active')) {
                this.innerHTML = '<i class="fas fa-heart"></i> Remove from Favorites';
                showToast('Success', `${mealName} added to favorites!`, 'success');
            } else {
                this.innerHTML = '<i class="far fa-heart"></i> Add to Favorites';
                showToast('Success', `${mealName} removed from favorites!`, 'success');
            }
            
            // Handle the API call to add/remove favorite
            handleFavoriteAction(mealId, action);
        });
    });
}

// Handle favorite action
function handleFavoriteAction(mealId, action) {
    // Get CSRF token
    const csrfToken = getCookie('csrftoken');
    
    fetch(`/meal/${mealId}/favorite/${action}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Favorite action successful:', data);
    })
    .catch(error => {
        console.error('Error handling favorite action:', error);
        showToast('Error', 'Could not update favorites. Please try again.', 'danger');
    });
}

// Helper function to get cookies (for CSRF token)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Recipe image gallery
function initRecipeGallery() {
    const galleryItems = document.querySelectorAll('.recipe-gallery-item');
    if (galleryItems.length === 0) return;
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imageUrl = this.getAttribute('data-full-img');
            const caption = this.getAttribute('data-caption');
            
            // Create modal for full-size image
            const modal = document.createElement('div');
            modal.className = 'modal fade';
            modal.id = 'imageModal';
            modal.setAttribute('tabindex', '-1');
            modal.setAttribute('aria-hidden', 'true');
            
            modal.innerHTML = `
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${caption}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${imageUrl}" class="img-fluid" alt="${caption}">
                        </div>
                    </div>
                </div>
            `;
            
            document.body.appendChild(modal);
            
            // Initialize and show the modal
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
            
            // Remove modal from DOM when hidden
            modal.addEventListener('hidden.bs.modal', function() {
                document.body.removeChild(modal);
            });
        });
    });
}

// Meal planner interactive functions
function initMealPlanner() {
    const mealPlanForm = document.getElementById('meal-plan-form');
    if (!mealPlanForm) return;
    
    // Update calorie estimation based on selected options
    const dietSelect = document.getElementById('diet');
    const mealsSelect = document.getElementById('meals');
    const calorieEstimate = document.getElementById('calorie-estimate');
    
    function updateCalorieEstimate() {
        if (!calorieEstimate) return;
        
        const diet = dietSelect.value;
        const meals = parseInt(mealsSelect.value);
        
        // Basic estimation algorithm
        let baseCalories = 2000;
        
        if (diet === 'low-carb' || diet === 'keto') {
            baseCalories -= 200;
        } else if (diet === 'high-protein') {
            baseCalories += 300;
        }
        
        // Adjust for number of meals
        const calorieAdjustment = ((meals - 3) * 200);
        const estimatedCalories = baseCalories + calorieAdjustment;
        
        calorieEstimate.textContent = estimatedCalories;
    }
    
    // Update on change
    if (dietSelect && mealsSelect) {
        dietSelect.addEventListener('change', updateCalorieEstimate);
        mealsSelect.addEventListener('change', updateCalorieEstimate);
        
        // Initial calculation
        updateCalorieEstimate();
    }
    
    // Handle drag and drop meal reordering
    const mealCards = document.querySelectorAll('.meal-card');
    if (mealCards.length > 0) {
        // Initialize drag and drop functionality
        // This would require a library like SortableJS in a real implementation
    }
}

// Initialize search form with autocomplete
function initSearchAutocomplete() {
    const searchInput = document.getElementById('ingredient-search');
    if (!searchInput) return;
    
    // Common ingredients for autocomplete
    const commonIngredients = [
        'Chicken', 'Beef', 'Pork', 'Fish', 'Salmon', 'Tuna',
        'Rice', 'Pasta', 'Potatoes', 'Sweet Potatoes',
        'Tomatoes', 'Onions', 'Garlic', 'Bell Peppers',
        'Broccoli', 'Spinach', 'Kale', 'Lettuce',
        'Cheese', 'Milk', 'Yogurt', 'Butter',
        'Eggs', 'Bread', 'Flour', 'Sugar',
        'Olive Oil', 'Vegetable Oil', 'Soy Sauce', 'Hot Sauce'
    ];
    
    // Basic autocomplete implementation
    // In a real app, you'd use a more robust library like Typeahead.js or equivalent
    searchInput.addEventListener('input', function() {
        const value = this.value.toLowerCase();
        if (value.length < 2) return;
        
        const matchedIngredients = commonIngredients.filter(ingredient => 
            ingredient.toLowerCase().includes(value)
        ).slice(0, 5);
        
        // Clear any existing suggestions
        let suggestionBox = document.getElementById('search-suggestions');
        if (!suggestionBox) {
            suggestionBox = document.createElement('div');
            suggestionBox.id = 'search-suggestions';
            suggestionBox.className = 'search-suggestions';
            searchInput.parentNode.appendChild(suggestionBox);
        } else {
            suggestionBox.innerHTML = '';
        }
        
        // Add new suggestions
        if (matchedIngredients.length > 0) {
            matchedIngredients.forEach(ingredient => {
                const suggestion = document.createElement('div');
                suggestion.className = 'suggestion-item';
                suggestion.textContent = ingredient;
                suggestion.addEventListener('click', function() {
                    searchInput.value = ingredient;
                    suggestionBox.innerHTML = '';
                });
                suggestionBox.appendChild(suggestion);
            });
        }
    });
    
    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target !== searchInput) {
            const suggestionBox = document.getElementById('search-suggestions');
            if (suggestionBox) {
                suggestionBox.innerHTML = '';
            }
        }
    });
}

// Add this function to handle recipe filtering
function initRecipeFilters() {
    const filterForm = document.getElementById('recipe-filters');
    if (!filterForm) return;
    
    const filterInputs = filterForm.querySelectorAll('input, select');
    const recipeCards = document.querySelectorAll('.recipe-card');
    
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            applyFilters();
        });
    });
    
    function applyFilters() {
        // Get filter values
        const category = document.getElementById('filter-category')?.value || 'all';
        const maxTime = parseInt(document.getElementById('filter-time')?.value || '0');
        
        recipeCards.forEach(card => {
            let showCard = true;
            
            // Check category
            if (category !== 'all') {
                const cardCategory = card.getAttribute('data-category');
                if (cardCategory !== category) {
                    showCard = false;
                }
            }
            
            // Check cooking time
            if (maxTime > 0) {
                const cardTime = parseInt(card.getAttribute('data-cooking-time') || '0');
                if (cardTime > maxTime) {
                    showCard = false;
                }
            }
            
            // Show or hide card
            card.style.display = showCard ? 'flex' : 'none';
        });
    }
}

// Initialize page-specific features
function initPageSpecificFeatures() {
    // Check which page we're on based on URL or body class
    const path = window.location.pathname;
    
    if (path === '/' || path === '/home/') {
        // Home page specific initializations
        initSearchAutocomplete();
    } else if (path.includes('/meal/')) {
        // Recipe detail page
        initRecipeGallery();
        initFavoriteButtons();
    } else if (path.includes('/search/')) {
        // Search results page
        initRecipeFilters();
    } else if (path.includes('/meal-planner/')) {
        // Meal planner page
        initMealPlanner();
    }
}

// Call page-specific initializations
// FlavorFinder Enhanced UI - Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize page loader
    initPageLoader();
    
    // Initialize animations on scroll
    initScrollAnimations();
    
    // Initialize back to top button
    initBackToTop();
    
    // Initialize tooltips and popovers
    initTooltips();
    
    // Initialize responsive navigation
    initResponsiveNav();
    
    // Initialize form validations
    initFormValidations();
    
    // Initialize custom alerts
    initCustomAlerts();
    
    // Initialize smooth scrolling
    initSmoothScroll();
    
    // Initialize scroll indicator
    initScrollIndicator();
    
    // Initialize page-specific features
    initPageSpecificFeatures();
});

// Page loader functionality
function initPageLoader() {
    const loader = document.querySelector('.page-loader');
    if (!loader) return;
    
    // Hide loader after page load
    window.addEventListener('load', function() {
        setTimeout(function() {
            loader.classList.add('loaded');
        }, 500);
    });
}

// Animations on scroll
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if (animatedElements.length === 0) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                // Optional: stop observing after animation
                // observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Back to top button
function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');
    if (!backToTopBtn) return;
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize tooltips and popovers
function initTooltips() {
    // Using Bootstrap's built-in tooltip and popover functionality
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Responsive navigation
function initResponsiveNav() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    // Change navbar background on scroll
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });
    
    // Add active class to current nav item
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(function(link) {
        const href = link.getAttribute('href');
        if (href === currentLocation || currentLocation.includes(href) && href !== '/') {
            link.classList.add('active');
        }
    });
}

// Form validations
function initFormValidations() {
    const forms = document.querySelectorAll('.needs-validation');
    
    if (forms.length === 0) return;
    
    Array.from(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
}

// Custom alerts
function initCustomAlerts() {
    // Find all dismissible alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    
    alerts.forEach(function(alert) {
        // Auto-dismiss after 5 seconds
        setTimeout(function() {
            const closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) {
                closeBtn.click();
            }
        }, 5000);
    });
}

// Smooth scroll to anchors
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (!target) return;
            
            window.scrollTo({
                top: target.offsetTop - 80, // Offset for fixed navbar
                behavior: 'smooth'
            });
        });
    });
}

// Scroll indicator
function initScrollIndicator() {
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (!scrollIndicator) return;
    
    window.addEventListener('scroll', function() {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        scrollIndicator.style.width = scrolled + "%";
    });
}

// Create custom toast notification
function showToast(title, message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set toast color based on type
    let bgColor = '#4ECDC4';
    let iconClass = 'fa-info-circle';
    
    switch(type) {
        case 'success':
            bgColor = '#6BFF98';
            iconClass = 'fa-check-circle';
            break;
        case 'danger':
        case 'error':
            bgColor = '#FF6B6B';
            iconClass = 'fa-exclamation-circle';
            break;
        case 'warning':
            bgColor = '#FFD166';
            iconClass = 'fa-exclamation-triangle';
            break;
    }
    
    // Create toast content
    toast.innerHTML = `
        <div class="toast-header" style="background-color: ${bgColor}">
            <i class="fas ${iconClass} me-2"></i>
            <strong class="me-auto">${title}</strong>
            <small>Just now</small>
            <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    // Add toast to container
    toastContainer.appendChild(toast);
    
    // Remove toast after 5 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    }, 5000);
    
    // Add click event to close button
    const closeBtn = toast.querySelector('.btn-close');
    closeBtn.addEventListener('click', () => {
        toast.classList.remove('show');
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    });
}

// Initialize page-specific features
function initPageSpecificFeatures() {
    // Check which page we're on based on URL or body class
    const path = window.location.pathname;
    
    if (path === '/' || path === '/home/') {
        // Home page specific initializations
        initCategoryCards();
    } else if (path.includes('/meal/')) {
        // Recipe detail page
        initFavoriteButtons();
    } else if (path.includes('/search/')) {
        // Search results page
        initRecipeFilterEffects();
    }
}

// Category cards hover effect
function initCategoryCards() {
    const categoryCards = document.querySelectorAll('.category-card');
    
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// Recipe filter animation effects
function initRecipeFilterEffects() {
    const filterForm = document.getElementById('recipe-filters');
    if (!filterForm) return;
    
    // Add animation when filtering
    const filterInputs = filterForm.querySelectorAll('input, select');
    
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            const recipeCards = document.querySelectorAll('.recipe-card');
            
            recipeCards.forEach(card => {
                // Add a small animation effect
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '0.5';
                
                setTimeout(() => {
                    card.style.opacity = '1';
                }, 300);
            });
        });
    });
}

// Page loader functionality
function initPageLoader() {
    const loader = document.querySelector('.page-loader');
    if (!loader) return;
    
    // Hide loader immediately for debugging
    loader.style.display = 'none';
    
    // Or keep the original with a shorter timeout
    window.addEventListener('load', function() {
        setTimeout(function() {
            loader.classList.add('loaded');
        }, 100); // Reduced from 500ms
    });
}