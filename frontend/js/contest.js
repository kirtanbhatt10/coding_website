// Contest page functionality
let currentQuestion = null;
let questions = [];
let questionStartTime = null;
let timerInterval = null;
let timeLimit = null;
let ws = null;

async function initContest() {
    const sessionId = localStorage.getItem('session_id');
    if (!sessionId) {
        window.location.href = '/';
        return;
    }

    // Load event details
    await loadEventDetails();
    
    // Connect WebSocket for real-time updates
    connectWebSocket();
    
    // Load questions
    await loadQuestions();
    
    // Load user progress
    await loadUserProgress();
    
    // Load mini leaderboard
    loadMiniLeaderboard();
    setInterval(loadMiniLeaderboard, 5000);
    
    // Security: Detect tab switching
    setupTabSwitchDetection();
    
    // Disable copy-paste
    disableCopyPaste();
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
    const wsUrl = `${protocol}//${window.location.host}/ws/contest?session_id=${sessionId || ''}`;
    
    ws = new WebSocket(wsUrl);
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'contest_ended') {
            alert('Contest has ended! Redirecting to leaderboard...');
            window.location.href = '/leaderboard';
        }
    };
}

async function loadQuestions() {
    try {
        const sessionId = localStorage.getItem('session_id');
        if (!sessionId) {
            showAlert('Session not found. Please join the event again.', 'error');
            setTimeout(() => window.location.href = '/', 2000);
            return;
        }
        
        const response = await fetch(`/api/questions/?session_id=${sessionId}`);
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Questions API error:', response.status, errorText);
            throw new Error(`Failed to load questions: ${response.status}`);
        }
        questions = await response.json();
        
        console.log('Loaded questions:', questions.length);
        
        if (questions.length > 0) {
            loadQuestion(questions[0]);
        } else {
            showAlert('No questions available. Please contact admin.', 'error');
            document.getElementById('question-title').textContent = 'No Questions Available';
            document.getElementById('question-description').textContent = 'Please wait for questions to be added or contact the administrator.';
        }
    } catch (error) {
        console.error('Error loading questions:', error);
        showAlert('Error loading questions: ' + error.message, 'error');
        document.getElementById('question-title').textContent = 'Error Loading Questions';
        document.getElementById('question-description').textContent = error.message;
    }
}

function loadQuestion(question) {
    currentQuestion = question;
    questionStartTime = Date.now();
    
    // Update UI
    document.getElementById('question-title').textContent = question.title;
    document.getElementById('question-description').textContent = question.description;
    
    const levelBadge = document.getElementById('question-level');
    levelBadge.textContent = `Level ${question.level}`;
    levelBadge.className = `question-level level-${question.level}`;
    
    // Set starter code - ALWAYS clear it first, then only set if it exists and is not empty
    const codeEditor = document.getElementById('code-editor');
    codeEditor.value = ''; // Always clear first
    
    // Only set starter code if it exists, is not null, and is not empty after trimming
    if (question.starter_code != null && question.starter_code !== undefined && question.starter_code.trim() !== '') {
        codeEditor.value = question.starter_code;
    }
    
    // Setup timer if time limit exists
    timeLimit = question.time_limit;
    if (timeLimit) {
        startTimer(timeLimit);
    } else {
        document.getElementById('timer').textContent = 'No time limit';
        document.getElementById('timer').className = 'timer';
    }
    
    // Clear output
    document.getElementById('output-panel').innerHTML = '<div>Output will appear here...</div>';
    document.getElementById('test-results').innerHTML = '';
}

function startTimer(seconds) {
    let remaining = seconds;
    const timerEl = document.getElementById('timer');
    
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    timerEl.textContent = formatTime(remaining);
    timerEl.className = 'timer';
    
    timerInterval = setInterval(() => {
        remaining--;
        timerEl.textContent = formatTime(remaining);
        
        if (remaining <= 10) {
            timerEl.className = 'timer danger';
        } else if (remaining <= 30) {
            timerEl.className = 'timer warning';
        }
        
        if (remaining <= 0) {
            clearInterval(timerInterval);
            autoSubmit();
        }
    }, 1000);
}

async function runCode() {
    if (!currentQuestion) {
        showAlert('No question loaded. Please wait...', 'error');
        return;
    }
    
    const code = document.getElementById('code-editor').value;
    if (!code.trim()) {
        showAlert('Please write some code before running', 'error');
        return;
    }
    
    const outputPanel = document.getElementById('output-panel');
    const testResults = document.getElementById('test-results');
    
    outputPanel.innerHTML = '<div style="color: #6366f1;">⏳ Running code...</div>';
    testResults.innerHTML = '';
    
    try {
        const sessionId = localStorage.getItem('session_id');
        const response = await fetch(`/api/submissions/run?session_id=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_id: currentQuestion.id,
                code: code
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to run code');
        }
        
        const result = await response.json();
        
        // Display output - show actual program outputs
        let outputHtml = '';
        if (result.error_message) {
            outputHtml = `<div style="color: #ef4444; padding: 10px; background: rgba(239, 68, 68, 0.1); border-radius: 5px; margin-bottom: 10px;">
                <strong>❌ Error:</strong> ${result.error_message}
            </div>`;
        } else if (result.status === 'correct') {
            outputHtml = `<div style="color: #10b981; padding: 10px; background: rgba(16, 185, 129, 0.1); border-radius: 5px; margin-bottom: 10px;">
                <strong>✅ Code executed successfully!</strong>
            </div>`;
        } else if (result.status === 'incorrect') {
            outputHtml = `<div style="color: #f59e0b; padding: 10px; background: rgba(245, 158, 11, 0.1); border-radius: 5px; margin-bottom: 10px;">
                <strong>⚠️ Code executed but output doesn't match expected results</strong>
            </div>`;
        } else {
            outputHtml = `<div style="color: #6366f1; padding: 10px; background: rgba(99, 102, 241, 0.1); border-radius: 5px; margin-bottom: 10px;">
                <strong>ℹ️ Code executed (Status: ${result.status})</strong>
            </div>`;
        }
        
        // Show execution time if available
        if (result.execution_time !== undefined) {
            outputHtml += `<div style="color: var(--text-light-secondary); font-size: 0.9rem; margin-top: 5px;">
                Execution time: ${result.execution_time.toFixed(3)}s
            </div>`;
        }
        
        outputPanel.innerHTML = outputHtml;
        
        // Display test results with detailed output
        if (result.results && result.results.length > 0) {
            let testHtml = '<h3 style="margin-top: 20px; margin-bottom: 15px;">📋 Test Results:</h3>';
            
            result.results.forEach((test, idx) => {
                const isPass = test.status === 'correct';
                const statusIcon = isPass ? '✅' : '❌';
                const statusText = isPass ? 'Passed' : 'Failed';
                const bgColor = isPass ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)';
                const borderColor = isPass ? 'rgba(16, 185, 129, 0.3)' : 'rgba(239, 68, 68, 0.3)';
                
                testHtml += `
                    <div style="padding: 15px; margin-bottom: 10px; background: ${bgColor}; border-left: 4px solid ${borderColor}; border-radius: 5px;">
                        <div style="font-weight: bold; margin-bottom: 8px;">
                            ${statusIcon} <strong>Test Case ${test.test_case}:</strong> ${statusText}
                        </div>
                        ${test.output !== undefined && test.output !== null ? `
                            <div style="margin-top: 5px;">
                                <strong>Your Output:</strong> 
                                <code style="background: rgba(0,0,0,0.1); padding: 2px 6px; border-radius: 3px; font-family: monospace;">${escapeHtml(String(test.output))}</code>
                            </div>
                        ` : ''}
                        ${test.expected !== undefined && test.expected !== null ? `
                            <div style="margin-top: 5px;">
                                <strong>Expected:</strong> 
                                <code style="background: rgba(0,0,0,0.1); padding: 2px 6px; border-radius: 3px; font-family: monospace;">${escapeHtml(String(test.expected))}</code>
                            </div>
                        ` : ''}
                        ${test.error ? `
                            <div style="margin-top: 5px; color: #ef4444;">
                                <strong>Error:</strong> ${escapeHtml(String(test.error))}
                            </div>
                        ` : ''}
                    </div>
                `;
            });
            
            testResults.innerHTML = testHtml;
        } else if (result.error_message) {
            testResults.innerHTML = '';
        } else {
            testResults.innerHTML = '<div style="color: var(--text-light-secondary); padding: 10px;">No test results available</div>';
        }
    } catch (error) {
        outputPanel.innerHTML = `<div style="color: #ef4444; padding: 10px; background: rgba(239, 68, 68, 0.1); border-radius: 5px;">
            <strong>❌ Error:</strong> ${escapeHtml(error.message)}
        </div>`;
        testResults.innerHTML = '';
        console.error('Run code error:', error);
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function submitCode() {
    if (!currentQuestion) return;
    
    const code = document.getElementById('code-editor').value;
    const timerText = document.getElementById('timer').textContent;
    let timeTaken = 0;
    
    if (timeLimit && timerText !== 'No time limit') {
        const [mins, secs] = timerText.split(':').map(Number);
        const remaining = mins * 60 + secs;
        timeTaken = timeLimit - remaining;
    }
    
    if (!code.trim()) {
        showAlert('Please write some code before submitting', 'error');
        return;
    }
    
    try {
        const sessionId = localStorage.getItem('session_id');
        const response = await fetch(`/api/submissions/submit?session_id=${sessionId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_id: currentQuestion.id,
                code: code,
                time_taken: timeTaken
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit code');
        }
        
        const result = await response.json();
        
        if (result.status === 'correct') {
            // Show success message with points info
            let successMsg = '✅ Correct! Question solved!';
            if (result.points_earned !== undefined) {
                successMsg += `\n\nPoints: ${result.points_earned.toFixed(1)}`;
                if (result.base_points !== undefined) {
                    successMsg += ` (Base: ${result.base_points}`;
                    if (result.speed_bonus && result.speed_bonus > 0) {
                        successMsg += ` + Speed Bonus: ${result.speed_bonus.toFixed(1)}`;
                        if (result.speed_rank) {
                            const rankEmoji = result.speed_rank === 1 ? '🥇' : result.speed_rank === 2 ? '🥈' : '🥉';
                            successMsg += ` - ${rankEmoji} ${result.speed_rank === 1 ? '1st' : result.speed_rank === 2 ? '2nd' : '3rd'} fastest!`;
                        }
                    }
                    successMsg += ')';
                }
            }
            showAlert(successMsg, 'success');
            
            // Update progress
            await loadUserProgress();
            
            // Load next question
            const currentIndex = questions.findIndex(q => q.id === currentQuestion.id);
            if (currentIndex < questions.length - 1) {
                setTimeout(() => {
                    loadQuestion(questions[currentIndex + 1]);
                }, 2000);
            } else {
                showAlert('Congratulations! You completed all questions!', 'success');
            }
        } else {
            showAlert('Incorrect solution. Please try again.', 'error');
            const outputPanel = document.getElementById('output-panel');
            if (result.error_message) {
                outputPanel.innerHTML = `<div style="color: #ef4444;">${result.error_message}</div>`;
            }
        }
    } catch (error) {
        showAlert('Submission failed: ' + error.message, 'error');
    }
}

function autoSubmit() {
    if (!currentQuestion) return;
    
    showAlert('Time limit reached! Auto-submitting...', 'warning');
    submitCode();
}

async function loadUserProgress() {
    try {
        const sessionId = localStorage.getItem('session_id');
        const response = await fetch(`/api/auth/me/${sessionId}`);
        if (!response.ok) {
            throw new Error('Failed to load user progress');
        }
        const user = await response.json();
        
        document.getElementById('user-score').textContent = user.score.toFixed(1);
        
        // Calculate progress for each level
        const level1Questions = questions.filter(q => q.level === 1);
        const level2Questions = questions.filter(q => q.level === 2);
        const level3Questions = questions.filter(q => q.level === 3);
        
        // This would need to be fetched from submissions API
        // For now, we'll use a placeholder
        updateProgressBar('level1', 0, level1Questions.length);
        updateProgressBar('level2', 0, level2Questions.length);
        updateProgressBar('level3', 0, level3Questions.length);
    } catch (error) {
        console.error('Error loading user progress:', error);
    }
}

function updateProgressBar(level, solved, total) {
    const percentage = total > 0 ? (solved / total) * 100 : 0;
    const progressEl = document.getElementById(`${level}-progress`);
    const barEl = document.getElementById(`${level}-bar`);
    if (progressEl) progressEl.textContent = `${solved}/${total}`;
    if (barEl) barEl.style.width = `${percentage}%`;
}

async function loadMiniLeaderboard() {
    try {
        const response = await fetch('/api/leaderboard/');
        if (response.ok) {
            const leaderboard = await response.json();
            const top5 = leaderboard.slice(0, 5);
            
            const container = document.getElementById('mini-leaderboard');
            if (top5.length === 0) {
                container.innerHTML = '<p>No entries yet</p>';
                return;
            }
            
            container.innerHTML = top5.map((entry, idx) => `
                <div style="padding: 10px; margin-bottom: 10px; background: rgba(99, 102, 241, 0.1); border-radius: 5px;">
                    <strong>${entry.rank}.</strong> ${entry.user_name} - ${entry.score.toFixed(1)} pts
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading mini leaderboard:', error);
    }
}

function setupTabSwitchDetection() {
    let hidden = false;
    let switchCount = 0;
    
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            hidden = true;
            switchCount++;
            
            if (switchCount > 3) {
                alert('Warning: Multiple tab switches detected. This may result in disqualification.');
            }
        } else {
            hidden = false;
        }
    });
    
    window.addEventListener('blur', () => {
        if (switchCount > 5) {
            alert('Excessive tab switching detected. You may be disqualified.');
        }
    });
}

function disableCopyPaste() {
    const editor = document.getElementById('code-editor');
    if (!editor) return;
    
    editor.addEventListener('copy', (e) => {
        e.preventDefault();
        showAlert('Copying is disabled during the contest', 'warning');
    });
    
    editor.addEventListener('paste', (e) => {
        e.preventDefault();
        showAlert('Pasting is disabled during the contest', 'warning');
    });
    
    // Disable right-click context menu
    editor.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    });
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initContest);
} else {
    initContest();
}
