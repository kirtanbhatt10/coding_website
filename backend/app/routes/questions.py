from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models import Question, User

router = APIRouter(prefix="/api/questions", tags=["questions"])

class QuestionResponse(BaseModel):
    id: int
    level: int
    question_number: int
    title: str
    description: str
    starter_code: Optional[str]
    time_limit: Optional[int]
    points: int
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[QuestionResponse])
async def get_questions(session_id: str, db: Session = Depends(get_db)):
    """Get all questions for a user based on their progress"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Ensure user has at least level 1 access
    if user.current_level < 1:
        user.current_level = 1
        db.commit()
    
    # Get questions up to user's current level
    questions = db.query(Question).filter(
        Question.level <= user.current_level,
        Question.is_active == True
    ).order_by(Question.level, Question.question_number).all()
    
    # If no questions found, return all level 1 questions (for first-time setup)
    if not questions:
        questions = db.query(Question).filter(
            Question.level == 1,
            Question.is_active == True
        ).order_by(Question.question_number).all()
    
    return questions

@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: int, session_id: str, db: Session = Depends(get_db)):
    """Get a specific question"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Check if user has access to this question
    if question.level > user.current_level:
        raise HTTPException(status_code=403, detail="Question not unlocked yet")
    
    return question

@router.get("/{question_id}/test-cases")
async def get_test_cases(question_id: int, session_id: str, db: Session = Depends(get_db)):
    """Get test cases for a question (for validation only, not full details)"""
    user = db.query(User).filter(User.session_id == session_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    import json
    test_cases = json.loads(question.test_cases)
    # Return only count, not actual test cases
    return {"test_case_count": len(test_cases)}
