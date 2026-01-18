// Leaderboard page functionality
let ws = null;

async function initLeaderboard() {
    await loadEventDetails();
    await loadLeaderboard();
    connectWebSocket();
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
                if (event.name) {
                    document.getElementById('event-name').textContent = event.name;
                }
            }
        }
    } catch (error) {
        console.error('Error loading event details:', error);
    }
}

function connectWebSocket() {
    const sessionId = localStorage.getItem('session_id');
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/leaderboard?session_id=${sessionId || ''}`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'leaderboard_update') {
            loadLeaderboard();
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        setTimeout(connectWebSocket, 3000);
    };
}

async function loadLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard/');
        if (response.ok) {
            const leaderboard = await response.json();
            renderLeaderboard(leaderboard);
        } else {
            throw new Error('Failed to load leaderboard');
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
        const tbody = document.getElementById('leaderboard-body');
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" style="text-align: center; padding: 40px;">
                        Error loading leaderboard. Please refresh the page.
                    </td>
                </tr>
            `;
        }
    }
}

function renderLeaderboard(leaderboard) {
    const tbody = document.getElementById('leaderboard-body');
    if (!tbody) return;
    
    if (leaderboard.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; padding: 40px;">
                    No entries yet. Be the first to solve a question!
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = leaderboard.map((entry, index) => {
        const rankClass = entry.rank <= 3 ? `rank-${entry.rank}` : '';
        const badge = entry.rank <= 3 ? `<span class="rank-badge ${rankClass}">${entry.rank}</span>` : entry.rank;
        
        return `
            <tr style="animation: slideIn 0.3s ease-out; animation-delay: ${index * 0.05}s;">
                <td>${badge}</td>
                <td><strong>${entry.user_name}</strong></td>
                <td>${entry.college_year}</td>
                <td>${entry.score.toFixed(1)}</td>
                <td>${entry.questions_solved}</td>
                <td>${formatTime(entry.total_time)}</td>
            </tr>
        `;
    }).join('');
    
    // Add confetti for top 3
    if (leaderboard.length > 0 && leaderboard[0].rank === 1) {
        createConfetti();
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLeaderboard);
} else {
    initLeaderboard();
}
