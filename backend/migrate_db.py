"""
Database migration script to add new columns to Event table
Run this if you get errors about missing columns
"""
import sqlite3
import os
import sys

# Get the backend directory
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BACKEND_DIR, "competition.db")

def migrate_database():
    """Add new columns to Event table if they don't exist"""
    if not os.path.exists(DB_PATH):
        print("Database doesn't exist yet. It will be created on first run.")
        return
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if events table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        if not cursor.fetchone():
            print("Events table doesn't exist. It will be created on server startup.")
            conn.close()
            return
        
        # Check if columns exist
        cursor.execute("PRAGMA table_info(events)")
        columns = [row[1] for row in cursor.fetchall()]
        
        changes_made = False
        
        # Add join_code column if it doesn't exist
        if 'join_code' not in columns:
            print("Adding join_code column...")
            cursor.execute("ALTER TABLE events ADD COLUMN join_code VARCHAR")
            changes_made = True
        
        # Add admin_password column if it doesn't exist
        if 'admin_password' not in columns:
            print("Adding admin_password column...")
            cursor.execute("ALTER TABLE events ADD COLUMN admin_password VARCHAR")
            changes_made = True
        
        if changes_made:
            conn.commit()
            print("✅ Database migration completed successfully!")
        else:
            print("✅ Database is already up to date.")
            
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Running database migration...")
    migrate_database()
