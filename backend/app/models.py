from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    college_year = Column(String, nullable=False)  # "1st", "2nd", "3rd", "4th"
    session_id = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    current_level = Column(Integer, default=1)  # 1, 2, or 3
    current_question = Column(Integer, default=1)  # 1-12
    score = Column(Float, default=0.0)
    total_time = Column(Float, default=0.0)  # Total time in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    logo_path = Column(String, nullable=True)
    join_code = Column(String, unique=True, index=True, nullable=True)  # Unique code for joining
    admin_password = Column(String, nullable=True)  # Password for admin access
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, nullable=False)  # 1, 2, or 3
    question_number = Column(Integer, nullable=False)  # 1-12
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=True)
    test_cases = Column(Text, nullable=False)  # JSON string
    expected_outputs = Column(Text, nullable=False)  # JSON string
    time_limit = Column(Integer, nullable=True)  # seconds, None for level 1
    points = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String, nullable=False)  # "correct", "incorrect", "timeout", "error"
    execution_time = Column(Float, nullable=True)
    error_message = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    time_taken = Column(Float, default=0.0)  # Time taken to solve in seconds
    
    user = relationship("User")
    question = relationship("Question")

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    score = Column(Float, default=0.0)
    questions_solved = Column(Integer, default=0)
    total_time = Column(Float, default=0.0)
    rank = Column(Integer, nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship("User")
    event = relationship("Event")

class HallOfFame(Base):
    __tablename__ = "hall_of_fame"
    
    id = Column(Integer, primary_key=True, index=True)
    winner_name = Column(String, nullable=False)
    college_year = Column(String, nullable=False)
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    event_name = Column(String, nullable=False)
    event_date = Column(DateTime(timezone=True), nullable=False)
    questions_solved = Column(Integer, default=0)
    total_time = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
