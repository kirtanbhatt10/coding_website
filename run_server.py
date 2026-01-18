#!/usr/bin/env python3
"""
Startup script for the Coding Competition Platform
"""
import uvicorn
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

if __name__ == "__main__":
    print("=" * 50)
    print("Coding Competition Platform")
    print("=" * 50)
    print("\nStarting server on http://localhost:8000")
    print("\nAccess the application at:")
    print("  - Landing Page: http://localhost:8000/")
    print("  - Admin Panel: http://localhost:8000/admin")
    print("  - Hall of Fame: http://localhost:8000/hall-of-fame")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
