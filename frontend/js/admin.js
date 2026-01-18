// Admin panel functionality
let currentEvent = null;
let selectedLogoFile = null;

// Define createNewEvent on window IMMEDIATELY at the top - SIMPLE VERSION
if (typeof window !== 'undefined') {
    window.createNewEvent = function() {
        console.error('createNewEvent called before full implementation loaded');
    };
    console.log('✅ createNewEvent placeholder registered at top');
}

async function loadCurrentEvent() {
    try {
        const response = await fetch('/api/admin/event/active');
        if (response.ok) {
            const event = await response.json();
            currentEvent = event;
            
            if (event) {
                document.getElementById('event-status').innerHTML = `
                    <strong>${event.name}</strong> ${event.is_active ? '(Active)' : '(Inactive)'}
                    ${event.join_code ? `<br><strong>Join Code:</strong> <span style="font-size: 1.2rem; color: #6366f1; font-weight: bold;">${event.join_code}</span>` : ''}
                `;
                document.getElementById('start-btn').disabled = event.is_active;
                document.getElementById('stop-btn').disabled = !event.is_active;
                
                if (event.logo_path) {
                    const logo = document.getElementById('navbar-logo');
                    if (logo) {
                        logo.src = event.logo_path;
                        logo.style.display = 'block';
                    }
                }
            } else {
                document.getElementById('event-status').textContent = 'No event created';
                document.getElementById('start-btn').disabled = true;
                document.getElementById('stop-btn').disabled = true;
            }
        } else {
            document.getElementById('event-status').textContent = 'No event created';
            document.getElementById('start-btn').disabled = true;
            document.getElementById('stop-btn').disabled = true;
        }
    } catch (error) {
        console.error('Error loading current event:', error);
        document.getElementById('event-status').textContent = 'Error loading event';
    }
}

// Define function directly on window - NO IIFE, NO WRAPPERS, DIRECT ASSIGNMENT
window.createNewEvent = async function(clickEvent) {
    // Prevent default if it's a click event
    if (clickEvent && clickEvent.preventDefault) {
        clickEvent.preventDefault();
    }
    
    const eventNameInput = document.getElementById('event-name');
    const adminPasswordInput = document.getElementById('admin-password');
    
    if (!eventNameInput) {
        alert('❌ Event name input not found!');
        return;
    }
    
    const eventName = eventNameInput.value.trim();
    const adminPassword = adminPasswordInput ? (adminPasswordInput.value.trim() || 'kjk_codedthisinonenight') : 'kjk_codedthisinonenight';
    
    if (!eventName) {
        alert('⚠️ Please enter an event name');
        eventNameInput.focus();
        return;
    }
    
    // Disable button to prevent double submission
    const createBtn = clickEvent && clickEvent.target ? clickEvent.target : document.getElementById('create-event-btn');
    const originalText = createBtn ? createBtn.textContent : 'Create Event';
    if (createBtn) {
        createBtn.disabled = true;
        createBtn.textContent = 'Creating...';
    }
    
    try {
        console.log('🚀 Creating event:', { name: eventName, hasPassword: !!adminPassword });
        
        const response = await fetch('/api/admin/event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                name: eventName,
                admin_password: adminPassword
            })
        });
        
        console.log('📡 Response status:', response.status);
        
        if (response.ok) {
            const event = await response.json();
            console.log('✅ Event created:', event);
            currentEvent = event;
            
            // Store password for this session
            sessionStorage.setItem('admin_password', adminPassword);
            
            const joinCodeMsg = event.join_code ? `\n\n🔑 Join Code: ${event.join_code}\n\nShare this code with participants!` : '';
            alert('✅ Event created successfully!' + joinCodeMsg);
            
            // Clear form
            eventNameInput.value = '';
            if (adminPasswordInput) {
                adminPasswordInput.value = adminPassword;
            }
            
            // Reload event list
            await loadCurrentEvent();
        } else {
            const errorText = await response.text();
            console.error('❌ Error response:', response.status, errorText);
            let errorMsg = 'Unknown error';
            try {
                const error = JSON.parse(errorText);
                errorMsg = error.detail || error.message || errorText;
            } catch (e) {
                errorMsg = errorText || `Failed to create event (Status: ${response.status})`;
            }
            
            // Check if it's a database schema error
            if (errorMsg.includes('no such column') || errorMsg.includes('join_code') || errorMsg.includes('admin_password')) {
                errorMsg += '\n\n⚠️ Database needs migration!\n\nPlease:\n1. Stop the server (Ctrl+C)\n2. Delete backend/competition.db\n3. Restart the server\n\nThe database will be recreated with the correct schema.';
            }
            
            alert('❌ Error creating event:\n\n' + errorMsg);
            console.error('Full error details:', errorMsg);
        }
    } catch (error) {
        console.error('❌ Create event exception:', error);
        alert('❌ Error creating event:\n\n' + error.message + '\n\nCheck browser console (F12) for details.');
    } finally {
        // Re-enable button
        if (createBtn) {
            createBtn.disabled = false;
            createBtn.textContent = originalText;
        }
    }
};

// Log immediately after assignment - DIRECT EXECUTION
console.log('✅ createNewEvent FULL implementation assigned to window');
console.log('✅ Verification:', typeof window.createNewEvent === 'function');
console.log('✅ Function name:', window.createNewEvent ? window.createNewEvent.name : 'N/A');

function previewLogo(input) {
    if (input.files && input.files[0]) {
        selectedLogoFile = input.files[0];
        const reader = new FileReader();
        
        reader.onload = (e) => {
            const preview = document.getElementById('preview-logo');
            preview.src = e.target.result;
            preview.style.display = 'block';
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

async function uploadLogo() {
    if (!currentEvent) {
        alert('Please create an event first');
        return;
    }
    
    if (!selectedLogoFile) {
        alert('Please select a logo file first');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', selectedLogoFile);
    
    try {
        const response = await fetch(`/api/admin/upload-logo/${currentEvent.id}`, {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            alert('Logo uploaded successfully!');
            loadCurrentEvent();
        } else {
            const error = await response.json();
            alert('Error uploading logo: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error uploading logo: ' + error.message);
    }
}

async function startContest() {
    if (!currentEvent) {
        alert('Please create an event first');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/event/${currentEvent.id}/start`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Contest started!');
            loadCurrentEvent();
        } else {
            const error = await response.json();
            alert('Error starting contest: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error starting contest: ' + error.message);
    }
}

async function stopContest() {
    if (!currentEvent) {
        alert('Please create an event first');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/event/${currentEvent.id}/stop`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Contest stopped!');
            loadCurrentEvent();
        } else {
            const error = await response.json();
            alert('Error stopping contest: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error stopping contest: ' + error.message);
    }
}

async function resetContest() {
    if (!currentEvent) {
        alert('Please create an event first');
        return;
    }
    
    if (!confirm('Are you sure you want to reset the contest? This will delete all submissions and leaderboard data.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/event/${currentEvent.id}/reset`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Contest reset!');
            loadCurrentEvent();
        } else {
            const error = await response.json();
            alert('Error resetting contest: ' + (error.detail || 'Unknown error'));
        }
    } catch (error) {
        alert('Error resetting contest: ' + error.message);
    }
}

async function exportLeaderboard() {
    if (!currentEvent) {
        alert('Please create an event first');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/export/leaderboard/${currentEvent.id}`);
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `leaderboard_${currentEvent.id}.csv`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showAlert('Leaderboard exported successfully!', 'success');
        } else {
            const error = await response.json();
            showAlert('Error exporting leaderboard: ' + (error.detail || 'Unknown error'), 'error');
        }
    } catch (error) {
        showAlert('Error exporting leaderboard: ' + error.message, 'error');
    }
}

async function exportHallOfFame() {
    try {
        const response = await fetch('/api/admin/export/hall-of-fame');
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'hall_of_fame.csv';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showAlert('Hall of Fame exported successfully!', 'success');
        } else {
            const error = await response.json();
            showAlert('Error exporting Hall of Fame: ' + (error.detail || 'Unknown error'), 'error');
        }
    } catch (error) {
        showAlert('Error exporting Hall of Fame: ' + error.message, 'error');
    }
}

// Final verification - function should already be on window (defined above)
if (typeof window !== 'undefined' && typeof window.createNewEvent === 'function') {
    console.log('✅ Final verification: createNewEvent is available on window');
} else {
    console.error('❌ CRITICAL: createNewEvent not available on window at end of file!');
}
