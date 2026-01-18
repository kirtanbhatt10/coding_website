from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from ..database import get_db
from ..models import User
from ..security import security_manager

router = APIRouter(prefix="/api/auth", tags=["auth"])

class UserRegister(BaseModel):
    name: str
    college_year: str
    join_code: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    college_year: str
    session_id: str
    current_level: int
    current_question: int
    score: float
    
    class Config:
        from_attributes = True

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    from ..models import Event
    
    # Verify join code if provided
    if user_data.join_code:
        event = db.query(Event).filter(Event.join_code == user_data.join_code).first()
        if not event:
            raise HTTPException(status_code=404, detail="Invalid join code. Please check and try again.")
    
    session_id = security_manager.generate_session_id()
    
    user = User(
        name=user_data.name,
        college_year=user_data.college_year,
        session_id=session_id,
        current_level=1,
        current_question=1
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/me/{session_id}", response_model=UserResponse)
async def get_user(session_id: str, db: Session = Depends(get_db)):
    """Get user by session ID"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
