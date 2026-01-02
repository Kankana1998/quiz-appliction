"""
Database models for the Quiz Management System
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and authorization"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # 'admin' or 'student'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    quizzes_created = db.relationship('Quiz', backref='creator', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_email=False):
        """Convert user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'


class Quiz(db.Model):
    """Quiz model"""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan', order_by='Question.id')
    
    def to_dict(self, include_answers=False):
        """Convert quiz to dictionary"""
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'questions': [q.to_dict(include_answer=include_answers) for q in self.questions]
        }
        return data
    
    def __repr__(self):
        return f'<Quiz {self.title}>'


class Question(db.Model):
    """Question model for quiz questions"""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)  # 'multiple_choice', 'true_false', 'text'
    options = db.Column(JSON, nullable=True)  # For MCQ: ["option1", "option2", ...], For TF: ["True", "False"]
    correct_answer = db.Column(db.String(500), nullable=False)
    points = db.Column(db.Integer, default=1, nullable=False)
    order = db.Column(db.Integer, default=0, nullable=False)  # For ordering questions
    
    def to_dict(self, include_answer=False):
        """Convert question to dictionary"""
        data = {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options,
            'points': self.points,
            'order': self.order
        }
        if include_answer:
            data['correct_answer'] = self.correct_answer
        return data
    
    def check_answer(self, user_answer):
        """Check if user's answer is correct"""
        if self.question_type == 'true_false':
            # Normalize true/false answers
            user_answer = str(user_answer).strip().lower()
            correct = str(self.correct_answer).strip().lower()
            return user_answer == correct
        elif self.question_type == 'multiple_choice':
            # For multiple choice, compare exact match
            return str(user_answer).strip() == str(self.correct_answer).strip()
        elif self.question_type == 'text':
            # For text answers, case-insensitive comparison
            return str(user_answer).strip().lower() == str(self.correct_answer).strip().lower()
        return False
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:50]}...>'


class UserResponse(db.Model):
    """User response model for storing quiz submissions"""
    __tablename__ = 'user_responses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False, index=True)
    participant_name = db.Column(db.String(200), nullable=True)  # Name for anonymous participants
    answers = db.Column(JSON, nullable=False)  # {question_id: answer}
    score = db.Column(db.Integer, nullable=False)
    total_points = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref='responses', lazy=True)
    quiz = db.relationship('Quiz', backref='responses', lazy=True)
    
    def to_dict(self):
        """Convert response to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'participant_name': self.participant_name,
            'answers': self.answers,
            'score': self.score,
            'total_points': self.total_points,
            'submitted_at': self.submitted_at.isoformat() if self.submitted_at else None
        }
    
    def __repr__(self):
        return f'<UserResponse {self.id}: Quiz {self.quiz_id}, Score {self.score}/{self.total_points}>'

