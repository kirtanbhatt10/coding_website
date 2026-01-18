// Hall of Fame page functionality
let currentEventId = null;

async function initHallOfFame() {
    await loadEventDetails();
    await loadHallOfFame();
}

async function loadEventDetails() {
    try {
        const response = await fetch('/api/admin/event/active');
        if (response.ok) {
            const event = await response.json();
            if (event) {
                if (event.logo_path) {
                    const logo = document.getElementById('navbar-logo');
                    if (logo) {
                        logo.src = event.logo_path;
                        logo.style.display = 'block';
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error loading event details:', error);
    }
}

async function loadHallOfFame() {
    try {
        const response = await fetch('/api/hall-of-fame/');
        if (response.ok) {
            const entries = await response.json();
            renderHallOfFame(entries);
        } else {
            throw new Error('Failed to load Hall of Fame');
        }
    } catch (error) {
        console.error('Error loading Hall of Fame:', error);
        const container = document.getElementById('hall-of-fame-grid');
        if (container) {
            container.innerHTML = `
                <div style="text-align: center; grid-column: 1 / -1; padding: 40px;">
                    Error loading Hall of Fame. Please refresh the page.
                </div>
            `;
        }
    }
}

function renderHallOfFame(entries) {
    const container = document.getElementById('hall-of-fame-grid');
    if (!container) return;
    
    if (entries.length === 0) {
        container.innerHTML = `
            <div style="text-align: center; grid-column: 1 / -1; padding: 40px;">
                <h2>No Hall of Fame entries yet</h2>
                <p>Be the first to win a competition!</p>
            </div>
        `;
        return;
    }
    
    // Group by event
    const events = {};
    entries.forEach(entry => {
        if (!events[entry.event_name]) {
            events[entry.event_name] = [];
        }
        events[entry.event_name].push(entry);
    });
    
    let html = '';
    Object.keys(events).forEach(eventName => {
        const eventEntries = events[eventName].sort((a, b) => a.rank - b.rank);
        
        html += `<div style="grid-column: 1 / -1; margin-top: 30px; margin-bottom: 20px;">
            <h2 style="color: var(--primary-color);">${eventName}</h2>
            <p style="opacity: 0.7;">${eventEntries[0].event_date}</p>
        </div>`;
        
        eventEntries.forEach((entry, index) => {
            const isTop3 = entry.rank <= 3;
            const delay = index * 0.1;
            
            html += `
                <div class="hof-card ${isTop3 ? 'top-3' : ''} ${isTop3 ? `rank-${entry.rank}` : ''}" 
                     style="animation-delay: ${delay}s;">
                    <div class="hof-rank">#${entry.rank}</div>
                    <div class="hof-name">${entry.winner_name}</div>
                    <div class="hof-event">${entry.college_year} Year</div>
                    <div class="hof-details">
                        <div><strong>Score:</strong> ${entry.score.toFixed(1)}</div>
                        <div><strong>Questions Solved:</strong> ${entry.questions_solved}</div>
                        <div><strong>Total Time:</strong> ${formatTime(entry.total_time)}</div>
                    </div>
                </div>
            `;
        });
    });
    
    container.innerHTML = html;
    
    // Add confetti for top entries
    const topEntries = entries.filter(e => e.rank <= 3);
    if (topEntries.length > 0) {
        setTimeout(() => {
            createConfetti();
        }, 500);
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHallOfFame);
} else {
    initHallOfFame();
}
