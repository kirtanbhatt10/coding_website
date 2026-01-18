// Lobby page functionality
let ws = null;
let players = [];

async function initLobby() {
    const sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
        window.location.href = '/';
        return;
    }

    // Load event details
    await loadEventDetails();
    
    // Connect to WebSocket
    connectWebSocket();
    
    // Load players periodically
    loadPlayers();
    setInterval(loadPlayers, 3000);
    
    // Check for contest start
    checkContestStatus();
    setInterval(checkContestStatus, 2000);
}

async function loadEventDetails() {
    try {
        const event = await apiCall('/api/admin/event/active');
        if (event) {
            if (event.logo_path) {
                const logos = document.querySelectorAll('#navbar-logo, #lobby-logo');
                logos.forEach(logo => {
                    logo.src = event.logo_path;
                    logo.style.display = 'block';
                });
            }
            if (event.name) {
                document.getElementById('event-name').textContent = event.name;
            }
        }
    } catch (error) {
        console.error('Error loading event details:', error);
    }
}

function connectWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/lobby`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'contest_started') {
            window.location.href = '/contest';
        }
    };
    
    ws.onerror = (error) => {
        console.error('WebSocket error:', error);
    };
    
    ws.onclose = () => {
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000);
    };
}

async function loadPlayers() {
    // In a real implementation, you'd fetch from an API
    // For now, we'll simulate with stored players
    const sessionId = localStorage.getItem('session_id');
    if (!sessionId) return;
    
    // This would be replaced with actual API call to get all players
    // For demo purposes, we'll show the current user
    const userName = localStorage.getItem('user_name') || 'You';
    players = [{ name: userName, session_id: sessionId }];
    
    renderPlayers();
}

function renderPlayers() {
    const container = document.getElementById('players-list');
    const count = document.getElementById('player-count');
    
    count.textContent = players.length;
    
    container.innerHTML = players.map(player => `
        <div class="player-card">
            <div class="player-name">${player.name}</div>
            <div class="player-year">${player.college_year || 'Participant'}</div>
        </div>
    `).join('');
}

async function checkContestStatus() {
    try {
        const event = await apiCall('/api/admin/event/active');
        if (event && event.is_active) {
            window.location.href = '/contest';
        }
    } catch (error) {
        // Event not active or doesn't exist
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initLobby);
} else {
    initLobby();
}
