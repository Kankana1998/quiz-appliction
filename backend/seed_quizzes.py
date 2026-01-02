"""
Seed script to create sample quizzes with questions
Run: python seed_quizzes.py
"""
from app import app
from models import db, User, Quiz, Question

def seed_quizzes():
    """Create sample quizzes if they don't exist"""
    with app.app_context():
        # Get or create admin user
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user not found. Please run seed.py first to create admin user.")
            return
        
        # Check if quizzes already exist
        existing_quizzes = Quiz.query.count()
        if existing_quizzes > 0:
            print(f"Quizzes already exist ({existing_quizzes} quizzes found).")
            print("Adding sample quizzes anyway...")
        
        # Sample Quiz 1: Python Basics
        quiz1 = Quiz(
            title="Python Basics",
            description="Test your knowledge of fundamental Python concepts",
            created_by=admin.id,
            is_active=True
        )
        db.session.add(quiz1)
        db.session.flush()
        
        questions1 = [
            {
                "question_text": "What is Python?",
                "question_type": "multiple_choice",
                "options": ["A programming language", "A snake", "A framework", "A database"],
                "correct_answer": "A programming language",
                "points": 10
            },
            {
                "question_text": "Python is a dynamically typed language.",
                "question_type": "true_false",
                "options": None,
                "correct_answer": "True",
                "points": 5
            },
            {
                "question_text": "Which keyword is used to define a function in Python?",
                "question_type": "multiple_choice",
                "options": ["function", "def", "define", "func"],
                "correct_answer": "def",
                "points": 10
            },
            {
                "question_text": "What is the output of: print(2 ** 3)?",
                "question_type": "multiple_choice",
                "options": ["6", "8", "9", "5"],
                "correct_answer": "8",
                "points": 10
            }
        ]
        
        for idx, q_data in enumerate(questions1):
            question = Question(
                quiz_id=quiz1.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                points=q_data["points"],
                order=idx
            )
            db.session.add(question)
        
        # Sample Quiz 2: Web Development
        quiz2 = Quiz(
            title="Web Development Fundamentals",
            description="Basic concepts of web development including HTML, CSS, and JavaScript",
            created_by=admin.id,
            is_active=True
        )
        db.session.add(quiz2)
        db.session.flush()
        
        questions2 = [
            {
                "question_text": "What does HTML stand for?",
                "question_type": "multiple_choice",
                "options": [
                    "HyperText Markup Language",
                    "High Tech Modern Language",
                    "Home Tool Markup Language",
                    "Hyperlink and Text Markup Language"
                ],
                "correct_answer": "HyperText Markup Language",
                "points": 10
            },
            {
                "question_text": "CSS is used for styling web pages.",
                "question_type": "true_false",
                "options": None,
                "correct_answer": "True",
                "points": 5
            },
            {
                "question_text": "Which of the following is a JavaScript framework?",
                "question_type": "multiple_choice",
                "options": ["React", "HTML", "CSS", "Python"],
                "correct_answer": "React",
                "points": 10
            },
            {
                "question_text": "What is the purpose of the <div> tag in HTML?",
                "question_type": "text",
                "options": None,
                "correct_answer": "container",
                "points": 10
            }
        ]
        
        for idx, q_data in enumerate(questions2):
            question = Question(
                quiz_id=quiz2.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                points=q_data["points"],
                order=idx
            )
            db.session.add(question)
        
        # Sample Quiz 3: General Knowledge
        quiz3 = Quiz(
            title="General Knowledge Quiz",
            description="Test your general knowledge across various topics",
            created_by=admin.id,
            is_active=True
        )
        db.session.add(quiz3)
        db.session.flush()
        
        questions3 = [
            {
                "question_text": "What is the capital of France?",
                "question_type": "multiple_choice",
                "options": ["London", "Berlin", "Paris", "Madrid"],
                "correct_answer": "Paris",
                "points": 10
            },
            {
                "question_text": "The Earth is flat.",
                "question_type": "true_false",
                "options": None,
                "correct_answer": "False",
                "points": 5
            },
            {
                "question_text": "How many continents are there?",
                "question_type": "multiple_choice",
                "options": ["5", "6", "7", "8"],
                "correct_answer": "7",
                "points": 10
            }
        ]
        
        for idx, q_data in enumerate(questions3):
            question = Question(
                quiz_id=quiz3.id,
                question_text=q_data["question_text"],
                question_type=q_data["question_type"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                points=q_data["points"],
                order=idx
            )
            db.session.add(question)
        
        db.session.commit()
        
        print("\n✅ Sample quizzes created successfully!")
        print(f"   - Created {Quiz.query.count()} quiz(es)")
        print(f"   - Total questions: {Question.query.count()}")
        print("\nQuizzes available:")
        for quiz in Quiz.query.all():
            print(f"   - {quiz.title} ({len(quiz.questions)} questions)")

if __name__ == '__main__':
    seed_quizzes()

