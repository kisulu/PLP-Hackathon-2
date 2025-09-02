// Global variables for study mode
let currentFlashcards = [];
let studyMode = false;

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="notification-close">&times;</button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Flashcard generation and display
function displayGeneratedFlashcards(flashcards) {
    const container = document.getElementById('flashcards-container');
    const grid = document.getElementById('flashcards-grid');
    
    if (!container || !grid) return;
    
    grid.innerHTML = '';
    currentFlashcards = flashcards;
    
    flashcards.forEach((card, index) => {
        const cardElement = createFlashcardPreview(card, index);
        grid.appendChild(cardElement);
    });
    
    container.style.display = 'block';
    container.scrollIntoView({ behavior: 'smooth' });
    
    // Update stats
    updateStudyStats(flashcards.length, 0, 0);
}

function createFlashcardPreview(card, index) {
    const cardDiv = document.createElement('div');
    cardDiv.className = 'flashcard-preview';
    cardDiv.innerHTML = `
        <div class="card-preview-header">
            <h4>${card.title}</h4>
            <span class="difficulty-badge difficulty-${card.difficulty}">${card.difficulty}</span>
        </div>
        <div class="card-preview-content">
            <p class="question-preview">${card.question}</p>
            <button class="reveal-btn" onclick="togglePreviewAnswer(this, ${index})">
                Reveal Answer
            </button>
            <div class="answer-preview" style="display: none;">
                <p>${card.answer}</p>
            </div>
        </div>
        <div class="card-preview-actions">
            <button class="study-single-btn" onclick="studySingleCard(${index})">
                🎯 Study This Card
            </button>
        </div>
    `;
    return cardDiv;
}

function togglePreviewAnswer(button, index) {
    const answerDiv = button.nextElementSibling;
    const isHidden = answerDiv.style.display === 'none';
    
    if (isHidden) {
        answerDiv.style.display = 'block';
        button.textContent = 'Hide Answer';
        button.classList.add('active');
        
        // Add smooth reveal animation
        answerDiv.style.opacity = '0';
        answerDiv.style.transform = 'translateY(-10px)';
        
        setTimeout(() => {
            answerDiv.style.transition = 'all 0.3s ease';
            answerDiv.style.opacity = '1';
            answerDiv.style.transform = 'translateY(0)';
        }, 10);
    } else {
        answerDiv.style.display = 'none';
        button.textContent = 'Reveal Answer';
        button.classList.remove('active');
    }
}

function studySingleCard(index) {
    if (currentFlashcards[index]) {
        startStudyMode([currentFlashcards[index]]);
    }
}

function startStudyMode(flashcards) {
    if (!flashcards || flashcards.length === 0) return;
    
    // Store flashcards in sessionStorage for study mode
    sessionStorage.setItem('studyFlashcards', JSON.stringify(flashcards));
    
    // Redirect to study mode
    window.location.href = '/flashcards/study/all';
}

function updateStudyStats(total, studied, correct) {
    const totalElement = document.getElementById('total-cards');
    const studiedElement = document.getElementById('studied-cards');
    const correctElement = document.getElementById('correct-answers');
    
    if (totalElement) totalElement.textContent = total;
    if (studiedElement) studiedElement.textContent = studied;
    if (correctElement) correctElement.textContent = correct;
    
    const statsContainer = document.getElementById('study-stats');
    if (statsContainer && total > 0) {
        statsContainer.style.display = 'flex';
    }
}

// Enhanced flashcard interactions
function enhanceFlashcardInteractions() {
    // Add keyboard shortcuts for study mode
    document.addEventListener('keydown', function(e) {
        if (!studyMode) return;
        
        switch(e.key) {
            case ' ':
                e.preventDefault();
                const flipButton = document.querySelector('.flashcard-3d');
                if (flipButton) flipButton.click();
                break;
            case 'ArrowLeft':
                e.preventDefault();
                const prevBtn = document.getElementById('prev-card');
                if (prevBtn && !prevBtn.disabled) prevBtn.click();
                break;
            case 'ArrowRight':
                e.preventDefault();
                const nextBtn = document.getElementById('next-card');
                if (nextBtn && !nextBtn.disabled) nextBtn.click();
                break;
            case '1':
                e.preventDefault();
                const incorrectBtn = document.getElementById('incorrect-btn');
                if (incorrectBtn && incorrectBtn.style.display !== 'none') incorrectBtn.click();
                break;
            case '2':
                e.preventDefault();
                const correctBtn = document.getElementById('correct-btn');
                if (correctBtn && correctBtn.style.display !== 'none') correctBtn.click();
                break;
        }
    });
}

// Library search functionality
function filterFlashcards() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.library-card');
    let visibleCount = 0;
    
    cards.forEach(card => {
        const title = card.dataset.title || '';
        const question = card.dataset.question || '';
        const answer = card.dataset.answer || '';
        
        const isVisible = title.includes(searchTerm) || 
                         question.includes(searchTerm) || 
                         answer.includes(searchTerm);
        
        if (isVisible) {
            card.style.display = 'block';
            visibleCount++;
        } else {
            card.style.display = 'none';
        }
    });
    
    // Update search results count
    const resultsInfo = document.querySelector('.search-results-info');
    if (resultsInfo) {
        resultsInfo.textContent = `Showing ${visibleCount} of ${cards.length} flashcards`;
    }
}

// Delete flashcard with confirmation
async function deleteFlashcard(cardId) {
    if (!confirm('Are you sure you want to delete this flashcard? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/flashcards/delete/${cardId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Flashcard deleted successfully', 'success');
            // Remove the card from DOM
            const cardElement = document.querySelector(`[data-card-id="${cardId}"]`);
            if (cardElement) {
                cardElement.style.transition = 'all 0.3s ease';
                cardElement.style.opacity = '0';
                cardElement.style.transform = 'scale(0.8)';
                setTimeout(() => cardElement.remove(), 300);
            }
        } else {
            showNotification(data.error || 'Failed to delete flashcard', 'error');
        }
    } catch (error) {
        showNotification('Network error. Please try again.', 'error');
    }
}

// Enhanced study mode features
function initializeStudyMode() {
    studyMode = true;
    enhanceFlashcardInteractions();
    
    // Add study mode indicators
    document.body.classList.add('study-mode');
    
    // Show keyboard shortcuts help
    showKeyboardShortcuts();
}

function showKeyboardShortcuts() {
    const helpDiv = document.createElement('div');
    helpDiv.className = 'keyboard-shortcuts-help';
    helpDiv.innerHTML = `
        <div class="shortcuts-content">
            <h4>⌨️ Keyboard Shortcuts</h4>
            <div class="shortcuts-list">
                <div class="shortcut-item">
                    <kbd>Space</kbd>
                    <span>Flip card</span>
                </div>
                <div class="shortcut-item">
                    <kbd>←</kbd>
                    <span>Previous card</span>
                </div>
                <div class="shortcut-item">
                    <kbd>→</kbd>
                    <span>Next card</span>
                </div>
                <div class="shortcut-item">
                    <kbd>1</kbd>
                    <span>Mark incorrect</span>
                </div>
                <div class="shortcut-item">
                    <kbd>2</kbd>
                    <span>Mark correct</span>
                </div>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="close-shortcuts">
                Got it!
            </button>
        </div>
    `;
    
    document.body.appendChild(helpDiv);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (helpDiv.parentElement) {
            helpDiv.remove();
        }
    }, 10000);
}

// Progress tracking
function trackStudyProgress(cardId, isCorrect, timeSpent) {
    // Send progress data to backend
    fetch('/flashcards/track_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            flashcard_id: cardId,
            is_correct: isCorrect,
            time_spent: timeSpent
        })
    }).catch(error => {
        console.error('Failed to track progress:', error);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're in study mode
    if (window.location.pathname.includes('/study')) {
        initializeStudyMode();
    }
    
    // Add smooth scrolling to all anchor links
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
    
    // Add loading states to all forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.style.opacity = '0.7';
                submitBtn.style.pointerEvents = 'none';
            }
        });
    });
});

// Export functions for global use
window.displayGeneratedFlashcards = displayGeneratedFlashcards;
window.startStudyMode = startStudyMode;
window.deleteFlashcard = deleteFlashcard;
window.filterFlashcards = filterFlashcards;
window.showNotification = showNotification;