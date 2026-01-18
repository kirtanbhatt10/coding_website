from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLite database - store in backend directory
import pathlib
DB_DIR = pathlib.Path(__file__).parent
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_DIR / 'competition.db'}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables and migrate if needed"""
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Check and migrate existing tables
        import sqlite3
        try:
            conn = engine.raw_connection()
            cursor = conn.cursor()
            
            # Check if events table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
            if cursor.fetchone():
                # Check events table columns
                cursor.execute("PRAGMA table_info(events)")
                columns = [row[1] for row in cursor.fetchall()]
                
                # Add missing columns if they don't exist
                if 'join_code' not in columns:
                    print("Adding join_code column to events table...")
                    cursor.execute("ALTER TABLE events ADD COLUMN join_code VARCHAR")
                    conn.commit()
                
                if 'admin_password' not in columns:
                    print("Adding admin_password column to events table...")
                    cursor.execute("ALTER TABLE events ADD COLUMN admin_password VARCHAR")
                    conn.commit()
            
            conn.close()
            print("Database tables created/verified successfully")
        except Exception as migrate_error:
            print(f"Migration check error: {migrate_error}")
            import traceback
            traceback.print_exc()
        
        # Check if questions exist, if not, seed them
        try:
            from .models import Question
            db = SessionLocal()
            question_count = db.query(Question).count()
            if question_count == 0:
                print("No questions found. Seeding database with default questions...")
                _seed_default_questions(db)
                print("Questions seeded successfully!")
            db.close()
        except Exception as seed_error:
            print(f"Question seeding check error: {seed_error}")
            import traceback
            traceback.print_exc()
            
    except Exception as e:
        print(f"Database initialization error: {e}")
        import traceback
        traceback.print_exc()

def _seed_default_questions(db):
    """Seed database with default questions if none exist"""
    import json
    from .models import Question
    
    questions = [
        # LEVEL 1 - Beginner (Questions 1-4)
        {
            "level": 1,
            "question_number": 1,
            "title": "Sum of Two Numbers",
            "description": "Write a Python program that takes two integers as input and prints their sum.\n\n**Input Format:** Two integers separated by a newline\n**Output Format:** The sum (you can format it any way you like, as long as the correct answer is present)",
            "starter_code": "",
            "test_cases": json.dumps(["5\n3", "10\n20", "-5\n5", "0\n0"]),
            "expected_outputs": json.dumps(["8", "30", "0", "0"]),
            "time_limit": None,
            "points": 10
        },
        {
            "level": 1,
            "question_number": 2,
            "title": "Check Even or Odd",
            "description": "Write a Python program that takes an integer as input and prints 'Even' if the number is even, otherwise prints 'Odd'.\n\nInput: A single integer\nOutput: 'Even' or 'Odd'",
            "starter_code": "",
            "test_cases": json.dumps(["4", "7", "0", "-3"]),
            "expected_outputs": json.dumps(["Even", "Odd", "Even", "Odd"]),
            "time_limit": None,
            "points": 10
        },
        {
            "level": 1,
            "question_number": 3,
            "title": "Sum of List Elements",
            "description": "Write a Python program that takes a list of integers as input (space-separated) and prints the sum of all elements.\n\nInput: Space-separated integers\nOutput: Sum of all integers",
            "starter_code": "",
            "test_cases": json.dumps(["1 2 3 4 5", "10 20 30", "-5 5 -3", "0"]),
            "expected_outputs": json.dumps(["15", "60", "-3", "0"]),
            "time_limit": None,
            "points": 10
        },
        {
            "level": 1,
            "question_number": 4,
            "title": "Count Vowels",
            "description": "Write a Python program that takes a string as input and prints the count of vowels (a, e, i, o, u) in the string (case-insensitive).\n\nInput: A string\nOutput: Count of vowels",
            "starter_code": "",
            "test_cases": json.dumps(["Hello", "Programming", "AEIOU", "xyz"]),
            "expected_outputs": json.dumps(["2", "3", "5", "0"]),
            "time_limit": None,
            "points": 10
        },
        # LEVEL 2 - Intermediate (Questions 5-8)
        {
            "level": 2,
            "question_number": 5,
            "title": "Factorial Function",
            "description": "Write a Python function that calculates the factorial of a number. The function should take an integer n and return n! (n factorial).\n\nInput: A single integer n (0 <= n <= 10)\nOutput: The factorial of n",
            "starter_code": "",
            "test_cases": json.dumps(["5", "0", "7", "10"]),
            "expected_outputs": json.dumps(["120", "1", "5040", "3628800"]),
            "time_limit": 30,
            "points": 15
        },
        {
            "level": 2,
            "question_number": 6,
            "title": "Find Maximum in Dictionary",
            "description": "Write a Python program that takes a dictionary as input (in format: key1:value1,key2:value2) and prints the key with the maximum value.\n\nInput: Dictionary as string (key:value pairs separated by commas)\nOutput: Key with maximum value",
            "starter_code": "",
            "test_cases": json.dumps(["a:10,b:20,c:15", "x:5,y:5,z:10", "one:100,two:50"]),
            "expected_outputs": json.dumps(["b", "z", "one"]),
            "time_limit": 30,
            "points": 15
        },
        {
            "level": 2,
            "question_number": 7,
            "title": "Reverse String Recursively",
            "description": "Write a recursive Python function that reverses a string.\n\nInput: A string\nOutput: Reversed string",
            "starter_code": "",
            "test_cases": json.dumps(["hello", "python", "a", "12345"]),
            "expected_outputs": json.dumps(["olleh", "nohtyp", "a", "54321"]),
            "time_limit": 30,
            "points": 15
        },
        {
            "level": 2,
            "question_number": 8,
            "title": "Count Word Frequencies",
            "description": "Write a Python program that takes a sentence as input and prints a dictionary with word frequencies (case-insensitive).\n\nInput: A sentence\nOutput: Dictionary string with word:count format",
            "starter_code": "",
            "test_cases": json.dumps(["hello world hello", "the quick brown fox", "a a a b b"]),
            "expected_outputs": json.dumps(["{'hello': 2, 'world': 1}", "{'the': 1, 'quick': 1, 'brown': 1, 'fox': 1}", "{'a': 3, 'b': 2}"]),
            "time_limit": 30,
            "points": 15
        },
        # LEVEL 3 - Advanced (Questions 9-12)
        {
            "level": 3,
            "question_number": 9,
            "title": "Find Prime Numbers",
            "description": "Write a Python program that takes an integer n as input and prints all prime numbers from 2 to n (inclusive).\n\nInput: A single integer n (2 <= n <= 100)\nOutput: Space-separated prime numbers",
            "starter_code": "",
            "test_cases": json.dumps(["10", "20", "30", "2"]),
            "expected_outputs": json.dumps(["2 3 5 7", "2 3 5 7 11 13 17 19", "2 3 5 7 11 13 17 19 23 29", "2"]),
            "time_limit": 60,
            "points": 20
        },
        {
            "level": 3,
            "question_number": 10,
            "title": "Binary Search",
            "description": "Write a Python program that implements binary search. Given a sorted list of integers and a target value, find the index of the target (return -1 if not found).\n\nInput: First line - space-separated sorted integers, Second line - target value\nOutput: Index of target or -1",
            "starter_code": "",
            "test_cases": json.dumps(["1 2 3 4 5\n3", "1 3 5 7 9\n6", "10 20 30 40\n20", "1\n1"]),
            "expected_outputs": json.dumps(["2", "-1", "1", "0"]),
            "time_limit": 60,
            "points": 20
        },
        {
            "level": 3,
            "question_number": 11,
            "title": "Longest Common Subsequence",
            "description": "Write a Python program that finds the length of the longest common subsequence (LCS) between two strings.\n\nInput: Two strings separated by a newline\nOutput: Length of LCS",
            "starter_code": "",
            "test_cases": json.dumps(["ABCDGH\nAEDFHR", "AGGTAB\nGXTXAYB", "abc\ndef", "a\na"]),
            "expected_outputs": json.dumps(["3", "4", "0", "1"]),
            "time_limit": 60,
            "points": 20
        },
        {
            "level": 3,
            "question_number": 12,
            "title": "Merge Sorted Arrays",
            "description": "Write a Python program that merges two sorted arrays into one sorted array without using built-in sort functions.\n\nInput: Two lines, each containing space-separated sorted integers\nOutput: Merged sorted array as space-separated integers",
            "starter_code": "",
            "test_cases": json.dumps(["1 3 5\n2 4 6", "1 2 3\n4 5 6", "10 20\n5 15", "1\n2"]),
            "expected_outputs": json.dumps(["1 2 3 4 5 6", "1 2 3 4 5 6", "5 10 15 20", "1 2"]),
            "time_limit": 60,
            "points": 20
        }
    ]
    
    for q_data in questions:
        question = Question(**q_data)
        db.add(question)
    
    db.commit()
