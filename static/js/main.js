// Main JavaScript functionality

// Video speed adjustment
document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('bgVideo');
    if (video) {
        video.playbackRate = 0.25; // Slow down by 75% (25% speed)
    }

    // Initialize events display
    renderEvents('all');
    
    // Set up event listeners
    setupEventListeners();
});

// Setup all event listeners
function setupEventListeners() {
    // Topbar scroll behavior
    window.addEventListener('scroll', handleScroll);
    
    // Category filter buttons
    const filterButtons = document.querySelectorAll('.filter-btn');
    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            // Filter events
            const category = btn.dataset.category;
            renderEvents(category);
        });
    });
    
    // Modal close buttons
    const modalClose = document.getElementById('modalClose');
    const rulesModalClose = document.getElementById('rulesModalClose');
    const eventModal = document.getElementById('eventModal');
    const rulesModal = document.getElementById('rulesModal');
    
    if (modalClose) {
        modalClose.addEventListener('click', () => {
            eventModal.classList.remove('active');
        });
    }
    
    if (rulesModalClose) {
        rulesModalClose.addEventListener('click', () => {
            rulesModal.classList.remove('active');
        });
    }
    
    // Close modals on outside click
    window.addEventListener('click', (e) => {
        if (e.target === eventModal) {
            eventModal.classList.remove('active');
        }
        if (e.target === rulesModal) {
            rulesModal.classList.remove('active');
        }
    });
    
    // Accept rules button
    const acceptRulesBtn = document.getElementById('acceptRulesBtn');
    if (acceptRulesBtn) {
        acceptRulesBtn.addEventListener('click', () => {
            rulesModal.classList.remove('active');
            // Redirect to registration link if stored
            const regLink = sessionStorage.getItem('pendingRegLink');
            if (regLink) {
                window.open(regLink, '_blank');
                sessionStorage.removeItem('pendingRegLink');
            }
        });
    }
}

// Handle scroll for topbar
function handleScroll() {
    const topbar = document.getElementById('topbar');
    if (window.scrollY > 100) {
        topbar.classList.add('scrolled');
    } else {
        topbar.classList.remove('scrolled');
    }
}

// Render events based on category
function renderEvents(category) {
    const eventsGrid = document.getElementById('eventsGrid');
    const events = getEvents(category);
    
    eventsGrid.innerHTML = '';
    
    events.forEach(event => {
        const eventCard = createEventCard(event);
        eventsGrid.appendChild(eventCard);
    });
    
    // Add scroll animation
    setTimeout(() => {
        const cards = document.querySelectorAll('.event-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 50);
        });
    }, 10);
}

// Create event card element
function createEventCard(event) {
    const card = document.createElement('div');
    card.className = `event-card ${event.category}`;
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    
    const feeText = event.fee === 0 ? 'Free' : `₹${event.fee}`;
    const starLabel = event.category.split('-')[0] + '★';
    
    card.innerHTML = `
        <div class="event-card-header">
            <span class="material-symbols-rounded event-icon">${event.icon}</span>
            <span class="event-badge">${starLabel}</span>
        </div>
        <h3 class="event-name">${event.name}</h3>
        <p class="event-description">${event.description}</p>
    `;
    
    card.addEventListener('click', () => showEventDetails(event));
    
    return card;
}

// Show event details in modal
function showEventDetails(event) {
    const modalBody = document.getElementById('modalBody');
    const modal = document.getElementById('eventModal');
    
    const feeText = event.fee === 0 ? 'Free Entry' : `Registration Fee: ₹${event.fee}`;
    
    modalBody.innerHTML = `
        <div class="event-details">
            <div class="event-details-header">
                <span class="material-symbols-rounded event-icon-large">${event.icon}</span>
                <div>
                    <h2>${event.name}</h2>
                    <span class="event-category-badge">${event.category.toUpperCase()}</span>
                </div>
            </div>
            
            <div class="event-details-body">
                <div class="event-fee">
                    <span class="material-symbols-rounded">payments</span>
                    <span>${feeText}</span>
                </div>
                
                <p class="event-full-description">${event.details}</p>
                
                <button class="btn-register" onclick="handleRegistration('${event.regLink}')">
                    <span class="material-symbols-rounded">how_to_reg</span>
                    Register Now
                </button>
                
                <p class="terms-note">
                    <span class="material-symbols-rounded">info</span>
                    By registering, you agree to our terms and conditions
                </p>
            </div>
        </div>
    `;
    
    modal.classList.add('active');
}

// Handle registration button click
function handleRegistration(regLink) {
    // Store the registration link
    sessionStorage.setItem('pendingRegLink', regLink);
    
    // Close event modal
    const eventModal = document.getElementById('eventModal');
    eventModal.classList.remove('active');
    
    // Show rules modal
    setTimeout(() => {
        const rulesModal = document.getElementById('rulesModal');
        rulesModal.classList.add('active');
    }, 300);
}

// Smooth scroll behavior
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

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-section');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});
