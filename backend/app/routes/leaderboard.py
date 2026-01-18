from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import desc
from pydantic import BaseModel
from typing import List
from ..database import get_db
from ..models import Leaderboard, User, Event

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

class LeaderboardEntry(BaseModel):
    rank: int
    user_name: str
    college_year: str
    score: float
    questions_solved: int
    total_time: float
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[LeaderboardEntry])
async def get_leaderboard(db: Session = Depends(get_db)):
    """Get current leaderboard"""
    from ..models import Submission, Question
    
    event = db.query(Event).filter(Event.is_active == True).first()
    if not event:
        return []
    
    # Get all users who have submissions for this event
    users_with_submissions = db.query(User).join(Submission).filter(
        Submission.status == "correct"
    ).distinct().all()
    
    # Recalculate scores for all users to ensure accuracy
    leaderboard_entries = []
    for user in users_with_submissions:
        # Get all correct submissions for this user
        all_user_correct = db.query(Submission).filter(
            Submission.user_id == user.id,
            Submission.status == "correct"
        ).all()
        
        # Recalculate total score with bonuses
        total_score = 0.0
        for sub in all_user_correct:
            q = db.query(Question).filter(Question.id == sub.question_id).first()
            if q:
                base_pts = q.points
                # Check if this was in top 3 for this question
                question_subs = db.query(Submission).filter(
                    Submission.question_id == sub.question_id,
                    Submission.status == "correct"
                ).order_by(Submission.time_taken.asc()).all()
                
                sub_rank = None
                for idx, s in enumerate(question_subs, 1):
                    if s.id == sub.id:
                        sub_rank = idx
                        break
                
                bonus = 0.0
                if sub_rank == 1:
                    bonus = base_pts * 0.50
                elif sub_rank == 2:
                    bonus = base_pts * 0.30
                elif sub_rank == 3:
                    bonus = base_pts * 0.20
                
                total_score += base_pts + bonus
        
        # Update user score
        user.score = total_score
        
        # Update or create leaderboard entry
        leaderboard = db.query(Leaderboard).filter(
            Leaderboard.user_id == user.id,
            Leaderboard.event_id == event.id
        ).first()
        
        if not leaderboard:
            leaderboard = Leaderboard(
                user_id=user.id,
                event_id=event.id,
                score=total_score,
                questions_solved=len(all_user_correct),
                total_time=user.total_time
            )
            db.add(leaderboard)
        else:
            leaderboard.score = total_score
            leaderboard.questions_solved = len(all_user_correct)
            leaderboard.total_time = user.total_time
        
        leaderboard_entries.append({
            "user_id": user.id,
            "user_name": user.name,
            "college_year": user.college_year,
            "score": total_score,
            "questions_solved": len(all_user_correct),
            "total_time": user.total_time
        })
    
    db.commit()
    
    # Sort by score (descending), then by total_time (ascending)
    leaderboard_entries.sort(key=lambda x: (-x["score"], x["total_time"]))
    
    # Calculate ranks and format response
    leaderboard_data = []
    for idx, entry in enumerate(leaderboard_entries, 1):
        leaderboard_data.append({
            "rank": idx,
            "user_name": entry["user_name"],
            "college_year": entry["college_year"],
            "score": entry["score"],
            "questions_solved": entry["questions_solved"],
            "total_time": entry["total_time"]
        })
    
    return leaderboard_data
