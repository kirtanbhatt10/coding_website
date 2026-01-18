from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import json
from ..database import get_db
from ..models import Submission, User, Question, Event, Leaderboard
from ..code_executor import CodeExecutor
from ..security import security_manager
from ..websocket import manager

router = APIRouter(prefix="/api/submissions", tags=["submissions"])

class SubmitCode(BaseModel):
    question_id: int
    code: str
    time_taken: float = 0.0

class SubmissionResponse(BaseModel):
    id: int
    status: str
    execution_time: Optional[float]
    error_message: Optional[str]
    results: list
    
    class Config:
        from_attributes = True

@router.post("/run", response_model=dict)
async def run_code(submit_data: SubmitCode, session_id: str, db: Session = Depends(get_db)):
    """Run code without submitting (for testing)"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question = db.query(Question).filter(Question.id == submit_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Validate syntax
    executor = CodeExecutor(timeout=question.time_limit or 10)
    is_valid, syntax_error = executor.validate_syntax(submit_data.code)
    
    if not is_valid:
        return {
            "status": "error",
            "error_message": f"Syntax Error: {syntax_error}",
            "results": []
        }
    
    # Parse test cases
    test_cases = json.loads(question.test_cases)
    expected_outputs = json.loads(question.expected_outputs)
    
    # Execute code
    result = executor.execute_code(submit_data.code, test_cases, expected_outputs)
    
    return result

@router.post("/submit", response_model=SubmissionResponse)
async def submit_code(submit_data: SubmitCode, session_id: str, db: Session = Depends(get_db)):
    """Submit code for evaluation"""
    # Rate limiting
    if not security_manager.check_rate_limit(session_id):
        raise HTTPException(status_code=429, detail="Too many submissions. Please wait.")
    
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question = db.query(Question).filter(Question.id == submit_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if question is accessible
    if question.level > user.current_level:
        raise HTTPException(status_code=403, detail="Question not unlocked yet")
    
    # Check if already solved
    existing = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.question_id == question.id,
        Submission.status == "correct"
    ).first()
    
    if existing:
        return {
            "id": existing.id,
            "status": existing.status,
            "execution_time": existing.execution_time,
            "error_message": existing.error_message,
            "results": []
        }
    
    # Execute code
    executor = CodeExecutor(timeout=question.time_limit or 10)
    test_cases = json.loads(question.test_cases)
    expected_outputs = json.loads(question.expected_outputs)
    
    result = executor.execute_code(submit_data.code, test_cases, expected_outputs)
    
    # Save submission
    submission = Submission(
        user_id=user.id,
        question_id=question.id,
        code=submit_data.code,
        status=result["status"],
        execution_time=result.get("execution_time"),
        error_message=result.get("error_message"),
        time_taken=submit_data.time_taken
    )
    
    db.add(submission)
    
    # Update user progress if correct
    if result["status"] == "correct":
        # Calculate base points
        base_points = question.points
        speed_bonus = 0.0
        
        # Calculate speed bonus for top 3 fastest solvers
        event = db.query(Event).filter(Event.is_active == True).first()
        if event and event.start_time:
            # Get all correct submissions for this question, ordered by time_taken
            all_correct = db.query(Submission).filter(
                Submission.question_id == question.id,
                Submission.status == "correct"
            ).order_by(Submission.time_taken.asc()).all()
            
            # Find this user's rank (position) in solving this question
            user_rank = None
            for idx, sub in enumerate(all_correct, 1):
                if sub.user_id == user.id:
                    user_rank = idx
                    break
            
            # Award speed bonuses: 1st = 50%, 2nd = 30%, 3rd = 20%
            if user_rank == 1:
                speed_bonus = base_points * 0.50  # 50% bonus for fastest
            elif user_rank == 2:
                speed_bonus = base_points * 0.30  # 30% bonus for 2nd fastest
            elif user_rank == 3:
                speed_bonus = base_points * 0.20  # 20% bonus for 3rd fastest
        
        # Calculate total points (base + bonus)
        total_points = base_points + speed_bonus
        user.score += total_points
        user.total_time += submit_data.time_taken
        
        # Unlock next question
        if question.question_number < 12:
            next_q = db.query(Question).filter(
                Question.question_number == question.question_number + 1
            ).first()
            if next_q:
                if next_q.level > user.current_level:
                    user.current_level = next_q.level
                user.current_question = next_q.question_number
        
        # Update leaderboard
        if event:
            leaderboard = db.query(Leaderboard).filter(
                Leaderboard.user_id == user.id,
                Leaderboard.event_id == event.id
            ).first()
            
            if not leaderboard:
                leaderboard = Leaderboard(
                    user_id=user.id,
                    event_id=event.id,
                    score=user.score,
                    questions_solved=1,
                    total_time=user.total_time
                )
                db.add(leaderboard)
            else:
                # Recalculate total score from all correct submissions
                # This ensures points accumulate correctly
                all_user_correct = db.query(Submission).filter(
                    Submission.user_id == user.id,
                    Submission.status == "correct"
                ).all()
                
                # Recalculate total score
                recalculated_score = 0.0
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
                        
                        recalculated_score += base_pts + bonus
                
                user.score = recalculated_score
                leaderboard.score = recalculated_score
                leaderboard.questions_solved = len(all_user_correct)
                leaderboard.total_time = user.total_time
    
    db.commit()
    db.refresh(submission)
    
    # Broadcast leaderboard update
    await manager.broadcast_to_room({
        "type": "leaderboard_update",
        "user_id": user.id,
        "user_name": user.name,
        "score": user.score
    }, "leaderboard")
    
    response_data = {
        "id": submission.id,
        "status": submission.status,
        "execution_time": submission.execution_time,
        "error_message": submission.error_message,
        "results": result.get("results", [])
    }
    
    # Add bonus information if correct
    if result["status"] == "correct":
        response_data["points_earned"] = total_points
        response_data["base_points"] = base_points
        response_data["speed_bonus"] = speed_bonus
        if speed_bonus > 0:
            event = db.query(Event).filter(Event.is_active == True).first()
            if event:
                all_correct = db.query(Submission).filter(
                    Submission.question_id == question.id,
                    Submission.status == "correct"
                ).order_by(Submission.time_taken.asc()).all()
                user_rank = None
                for idx, sub in enumerate(all_correct, 1):
                    if sub.user_id == user.id:
                        user_rank = idx
                        break
                response_data["speed_rank"] = user_rank
    
    return response_data