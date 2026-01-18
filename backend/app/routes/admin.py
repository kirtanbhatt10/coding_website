from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import shutil
from ..database import get_db, init_db
from ..models import Event, Question, User, Leaderboard, HallOfFame, Submission
from ..websocket import manager

router = APIRouter(prefix="/api/admin", tags=["admin"])

# Ensure uploads directory exists
import pathlib
BASE_DIR = pathlib.Path(__file__).parent.parent.parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "logo"
os.makedirs(str(UPLOAD_DIR), exist_ok=True)

class EventCreate(BaseModel):
    name: str
    admin_password: Optional[str] = "kjk_codedthisinonenight"  # Default password
    join_code: Optional[str] = None  # Auto-generate if not provided

class EventResponse(BaseModel):
    id: int
    name: str
    logo_path: Optional[str]
    join_code: Optional[str]
    is_active: bool
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    
    class Config:
        from_attributes = True

class AdminLogin(BaseModel):
    password: str

class JoinEvent(BaseModel):
    join_code: str
    name: str
    college_year: str

@router.post("/event", response_model=EventResponse)
async def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """Create a new event"""
    import secrets
    import hashlib
    
    try:
        # Ensure database has the required columns - do this first
        try:
            from ..database import engine
            import sqlite3
            conn = engine.raw_connection()
            cursor = conn.cursor()
            
            # Check if events table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
            if cursor.fetchone():
                # Check columns
                cursor.execute("PRAGMA table_info(events)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'join_code' not in columns:
                    print("Adding join_code column...")
                    cursor.execute("ALTER TABLE events ADD COLUMN join_code VARCHAR")
                    conn.commit()
                
                if 'admin_password' not in columns:
                    print("Adding admin_password column...")
                    cursor.execute("ALTER TABLE events ADD COLUMN admin_password VARCHAR")
                    conn.commit()
            
            conn.close()
        except Exception as migrate_err:
            print(f"Migration check error: {migrate_err}")
            import traceback
            traceback.print_exc()
        
        # Validate input
        if not event_data.name or not event_data.name.strip():
            raise HTTPException(status_code=400, detail="Event name is required")
        
        if not event_data.admin_password:
            event_data.admin_password = "kjk_codedthisinonenight"  # Default password
        
        # Generate join code if not provided
        join_code = event_data.join_code
        if not join_code:
            # Generate a 6-character alphanumeric code
            join_code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))
            # Ensure uniqueness
            max_attempts = 10
            attempts = 0
            while db.query(Event).filter(Event.join_code == join_code).first() and attempts < max_attempts:
                join_code = ''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(6))
                attempts += 1
        
        # Hash the admin password
        password_hash = hashlib.sha256(event_data.admin_password.encode()).hexdigest()
        
        # Create event
        event = Event(
            name=event_data.name.strip(),
            join_code=join_code,
            admin_password=password_hash
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        
        print(f"✅ Event created successfully: {event.name} (ID: {event.id}, Join Code: {join_code})")
        
        # Return event with join_code
        return {
            "id": event.id,
            "name": event.name,
            "logo_path": getattr(event, 'logo_path', None),
            "join_code": getattr(event, 'join_code', None),
            "is_active": event.is_active,
            "start_time": event.start_time,
            "end_time": event.end_time
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Error creating event: {error_details}")
        raise HTTPException(status_code=500, detail=f"Error creating event: {str(e)}")

@router.post("/upload-logo/{event_id}")
async def upload_logo(event_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload college logo for event"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Save file
    file_ext = file.filename.split('.')[-1]
    filename = f"logo_{event_id}.{file_ext}"
    filepath = UPLOAD_DIR / filename
    
    with open(str(filepath), "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    event.logo_path = f"/static/logo/{filename}"
    db.commit()
    
    return {"logo_path": event.logo_path}

@router.get("/event/active", response_model=Optional[EventResponse])
async def get_active_event(db: Session = Depends(get_db)):
    """Get currently active event"""
    try:
        # First try to migrate if needed
        try:
            from ..database import engine
            import sqlite3
            conn = engine.raw_connection()
            cursor = conn.cursor()
            
            # Check if events table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
            if cursor.fetchone():
                cursor.execute("PRAGMA table_info(events)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'join_code' not in columns:
                    print("Migrating: Adding join_code column...")
                    cursor.execute("ALTER TABLE events ADD COLUMN join_code VARCHAR")
                    conn.commit()
                if 'admin_password' not in columns:
                    print("Migrating: Adding admin_password column...")
                    cursor.execute("ALTER TABLE events ADD COLUMN admin_password VARCHAR")
                    conn.commit()
            
            conn.close()
        except Exception as migrate_err:
            print(f"Migration attempt: {migrate_err}")
        
        # Now try to query
        try:
            event = db.query(Event).filter(Event.is_active == True).first()
            if not event:
                event = db.query(Event).order_by(Event.created_at.desc()).first()
            
            if event:
                return {
                    "id": event.id,
                    "name": event.name,
                    "logo_path": getattr(event, 'logo_path', None),
                    "join_code": getattr(event, 'join_code', None),
                    "is_active": event.is_active,
                    "start_time": event.start_time,
                    "end_time": event.end_time
                }
        except Exception as query_err:
            # If query fails due to missing columns, return None
            print(f"Query error (may need migration): {query_err}")
            return None
        
        return None
    except Exception as e:
        # If there's still an error, return None gracefully
        print(f"Error getting active event: {e}")
        import traceback
        traceback.print_exc()
        return None

@router.get("/event/by-code/{join_code}")
async def get_event_by_code(join_code: str, db: Session = Depends(get_db)):
    """Get event by join code"""
    event = db.query(Event).filter(Event.join_code == join_code).first()
    if not event:
        raise HTTPException(status_code=404, detail="Invalid join code")
    return {
        "id": event.id,
        "name": event.name,
        "join_code": event.join_code,
        "is_active": event.is_active
    }

@router.post("/verify-password/{event_id}")
async def verify_password(event_id: int, login_data: AdminLogin, db: Session = Depends(get_db)):
    """Verify admin password"""
    import hashlib
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # If event has no password set, allow any password (for backward compatibility)
    if not event.admin_password or event.admin_password.strip() == "":
        return {"verified": True, "message": "No password set for this event"}
    
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
    if event.admin_password == password_hash:
        return {"verified": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password. If this event was created with an older version, you may need to create a new event or use the password that was set when the event was created.")

@router.post("/event/{event_id}/update-password")
async def update_event_password(event_id: int, login_data: AdminLogin, db: Session = Depends(get_db)):
    """Update admin password for an event"""
    import hashlib
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Hash and update password
    password_hash = hashlib.sha256(login_data.password.encode()).hexdigest()
    event.admin_password = password_hash
    db.commit()
    
    return {"message": "Password updated successfully"}

@router.post("/event/{event_id}/start")
async def start_event(event_id: int, db: Session = Depends(get_db)):
    """Start the contest"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Deactivate other events
    db.query(Event).filter(Event.id != event_id).update({"is_active": False})
    
    event.is_active = True
    event.start_time = datetime.now()
    db.commit()
    
    # Broadcast to lobby
    await manager.broadcast_to_room({
        "type": "contest_started",
        "event_id": event_id,
        "event_name": event.name
    }, "lobby")
    
    return {"message": "Contest started", "event_id": event_id}

@router.post("/event/{event_id}/stop")
async def stop_event(event_id: int, db: Session = Depends(get_db)):
    """Stop the contest and finalize results"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    event.is_active = False
    event.end_time = datetime.now()
    
    # Update leaderboard ranks
    entries = db.query(Leaderboard).filter(
        Leaderboard.event_id == event_id
    ).order_by(
        desc(Leaderboard.score),
        Leaderboard.total_time
    ).all()
    
    for idx, entry in enumerate(entries, 1):
        entry.rank = idx
    
    # Add to Hall of Fame
    for entry in entries[:10]:  # Top 10
        user = db.query(User).filter(User.id == entry.user_id).first()
        if user:
            hall_entry = HallOfFame(
                winner_name=user.name,
                college_year=user.college_year,
                rank=entry.rank,
                score=entry.score,
                event_name=event.name,
                event_date=event.start_time or datetime.now(),
                questions_solved=entry.questions_solved,
                total_time=entry.total_time
            )
            db.add(hall_entry)
    
    db.commit()
    
    # Broadcast contest end
    await manager.broadcast_to_room({
        "type": "contest_ended",
        "event_id": event_id
    }, "contest")
    
    return {"message": "Contest stopped and results finalized"}

@router.post("/event/{event_id}/reset")
async def reset_event(event_id: int, db: Session = Depends(get_db)):
    """Reset contest (clear all submissions and progress)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Reset all users
    db.query(User).update({
        "current_level": 1,
        "current_question": 1,
        "score": 0.0,
        "total_time": 0.0
    })
    
    # Clear submissions and leaderboard
    db.query(Submission).delete()
    db.query(Leaderboard).filter(Leaderboard.event_id == event_id).delete()
    
    event.is_active = False
    event.start_time = None
    event.end_time = None
    
    db.commit()
    
    return {"message": "Contest reset"}

@router.get("/export/leaderboard/{event_id}")
async def export_leaderboard(event_id: int, db: Session = Depends(get_db)):
    """Export leaderboard as CSV"""
    import csv
    from io import StringIO
    
    entries = db.query(Leaderboard).filter(
        Leaderboard.event_id == event_id
    ).order_by(
        desc(Leaderboard.score),
        Leaderboard.total_time
    ).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Rank", "Name", "College Year", "Score", "Questions Solved", "Total Time"])
    
    for idx, entry in enumerate(entries, 1):
        user = db.query(User).filter(User.id == entry.user_id).first()
        if user:
            writer.writerow([
                idx,
                user.name,
                user.college_year,
                entry.score,
                entry.questions_solved,
                entry.total_time
            ])
    
    return {"csv": output.getvalue()}

@router.get("/export/hall-of-fame")
async def export_hall_of_fame(db: Session = Depends(get_db)):
    """Export Hall of Fame as CSV"""
    import csv
    from io import StringIO
    
    entries = db.query(HallOfFame).order_by(
        desc(HallOfFame.event_date),
        HallOfFame.rank
    ).all()
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Event Name", "Date", "Rank", "Winner Name", "College Year", "Score", "Questions Solved", "Total Time"])
    
    for entry in entries:
        writer.writerow([
            entry.event_name,
            entry.event_date.strftime("%Y-%m-%d %H:%M:%S"),
            entry.rank,
            entry.winner_name,
            entry.college_year,
            entry.score,
            entry.questions_solved,
            entry.total_time
        ])
    
    return {"csv": output.getvalue()}
