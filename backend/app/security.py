import secrets
import time
from typing import Dict, Set
from collections import defaultdict

class SecurityManager:
    """Manages security features like rate limiting and tab switching detection"""
    
    def __init__(self):
        self.submission_rates: Dict[str, list] = defaultdict(list)
        self.session_timestamps: Dict[str, float] = {}
        self.max_submissions_per_minute = 10
        self.tab_switch_detections: Dict[str, int] = defaultdict(int)
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID"""
        return secrets.token_urlsafe(32)
    
    def check_rate_limit(self, session_id: str) -> bool:
        """Check if user has exceeded submission rate limit"""
        now = time.time()
        # Remove submissions older than 1 minute
        self.submission_rates[session_id] = [
            ts for ts in self.submission_rates[session_id]
            if now - ts < 60
        ]
        
        if len(self.submission_rates[session_id]) >= self.max_submissions_per_minute:
            return False
        
        self.submission_rates[session_id].append(now)
        return True
    
    def record_tab_switch(self, session_id: str):
        """Record a tab switch detection"""
        self.tab_switch_detections[session_id] += 1
    
    def get_tab_switch_count(self, session_id: str) -> int:
        """Get number of tab switches detected"""
        return self.tab_switch_detections.get(session_id, 0)
    
    def reset_session(self, session_id: str):
        """Reset security tracking for a session"""
        if session_id in self.submission_rates:
            del self.submission_rates[session_id]
        if session_id in self.tab_switch_detections:
            del self.tab_switch_detections[session_id]

security_manager = SecurityManager()
