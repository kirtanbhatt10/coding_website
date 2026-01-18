from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List
from ..database import get_db
from ..models import HallOfFame

router = APIRouter(prefix="/api/hall-of-fame", tags=["hall-of-fame"])

class HallOfFameEntry(BaseModel):
    id: int
    winner_name: str
    college_year: str
    rank: int
    score: float
    event_name: str
    event_date: str
    questions_solved: int
    total_time: float
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[HallOfFameEntry])
async def get_hall_of_fame(db: Session = Depends(get_db)):
    """Get all Hall of Fame entries"""
    entries = db.query(HallOfFame).order_by(
        desc(HallOfFame.event_date),
        HallOfFame.rank
    ).all()
    
    # Convert event_date to string
    result = []
    for entry in entries:
        entry_dict = {
            "id": entry.id,
            "winner_name": entry.winner_name,
            "college_year": entry.college_year,
            "rank": entry.rank,
            "score": entry.score,
            "event_name": entry.event_name,
            "event_date": entry.event_date.strftime("%Y-%m-%d %H:%M:%S"),
            "questions_solved": entry.questions_solved,
            "total_time": entry.total_time
        }
        result.append(entry_dict)
    
    return result

@router.get("/event/{event_name}", response_model=List[HallOfFameEntry])
async def get_hall_of_fame_by_event(event_name: str, db: Session = Depends(get_db)):
    """Get Hall of Fame entries for a specific event"""
    entries = db.query(HallOfFame).filter(
        HallOfFame.event_name == event_name
    ).order_by(HallOfFame.rank).all()
    
    result = []
    for entry in entries:
        entry_dict = {
            "id": entry.id,
            "winner_name": entry.winner_name,
            "college_year": entry.college_year,
            "rank": entry.rank,
            "score": entry.score,
            "event_name": entry.event_name,
            "event_date": entry.event_date.strftime("%Y-%m-%d %H:%M:%S"),
            "questions_solved": entry.questions_solved,
            "total_time": entry.total_time
        }
        result.append(entry_dict)
    
    return result
