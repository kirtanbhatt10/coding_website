"""
Script to update all questions to have empty starter_code
Run this to fix existing questions in the database
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.database import SessionLocal, init_db
from app.models import Question

def update_questions():
    """Update all questions to have empty starter_code"""
    init_db()
    db = SessionLocal()
    
    try:
        questions = db.query(Question).all()
        updated_count = 0
        
        for question in questions:
            if question.starter_code and question.starter_code.strip() != '':
                question.starter_code = ""
                updated_count += 1
        
        db.commit()
        print(f"Successfully updated {updated_count} questions with empty starter_code!")
        print(f"Total questions: {len(questions)}")
    except Exception as e:
        db.rollback()
        print(f"Error updating questions: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_questions()
