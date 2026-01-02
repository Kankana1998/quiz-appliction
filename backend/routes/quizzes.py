"""
Quiz routes for CRUD operations
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Quiz, Question, User
from datetime import datetime

quizzes_bp = Blueprint('quizzes', __name__)


def require_admin():
    """Helper function to check if user is admin"""
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None


@quizzes_bp.route('', methods=['GET'])
def get_quizzes():
    """Get all active quizzes (public) or all quizzes (admin)"""
    try:
        # Check if user is authenticated and admin
        is_admin = False
        try:
            claims = get_jwt()
            is_admin = claims.get('role') == 'admin'
        except:
            pass  # Not authenticated, treat as public user
        
        if is_admin:
            # Admin can see all quizzes
            quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
        else:
            # Public users only see active quizzes
            quizzes = Quiz.query.filter_by(is_active=True).order_by(Quiz.created_at.desc()).all()
        
        return jsonify({
            'quizzes': [quiz.to_dict(include_answers=False) for quiz in quizzes]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch quizzes', 'message': str(e)}), 500


@quizzes_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Get a specific quiz by ID (without answers for public, with answers for admin)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Check if quiz is active (for public users)
        is_admin = False
        include_answers = False
        try:
            claims = get_jwt()
            is_admin = claims.get('role') == 'admin'
            include_answers = is_admin
        except:
            pass  # Not authenticated
        
        if not is_admin and not quiz.is_active:
            return jsonify({'error': 'Quiz not found or not available'}), 404
        
        return jsonify({
            'quiz': quiz.to_dict(include_answers=include_answers)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch quiz', 'message': str(e)}), 500


@quizzes_bp.route('', methods=['POST'])
@jwt_required()
def create_quiz():
    """Create a new quiz with questions (admin only)"""
    try:
        # Check admin access
        admin_check = require_admin()
        if admin_check:
            return admin_check
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip() or None
        questions_data = data.get('questions', [])
        is_active = data.get('is_active', True)
        
        # Validation
        if not title:
            return jsonify({'error': 'Quiz title is required'}), 400
        if not questions_data or len(questions_data) == 0:
            return jsonify({'error': 'At least one question is required'}), 400
        
        # Validate questions
        for idx, q_data in enumerate(questions_data):
            question_text = q_data.get('question_text', '').strip()
            question_type = q_data.get('question_type', '').strip().lower()
            correct_answer = q_data.get('correct_answer', '').strip()
            points = q_data.get('points', 1)
            options = q_data.get('options', [])
            
            if not question_text:
                return jsonify({'error': f'Question {idx + 1}: Question text is required'}), 400
            if question_type not in ['multiple_choice', 'true_false', 'text']:
                return jsonify({'error': f'Question {idx + 1}: Invalid question type'}), 400
            if not correct_answer:
                return jsonify({'error': f'Question {idx + 1}: Correct answer is required'}), 400
            
            # Validate options for MCQ
            if question_type == 'multiple_choice':
                if not options or len(options) < 2:
                    return jsonify({'error': f'Question {idx + 1}: Multiple choice questions require at least 2 options'}), 400
                if correct_answer not in options:
                    return jsonify({'error': f'Question {idx + 1}: Correct answer must be one of the options'}), 400
            elif question_type == 'true_false':
                if correct_answer.lower() not in ['true', 'false']:
                    return jsonify({'error': f'Question {idx + 1}: True/False questions must have "True" or "False" as correct answer'}), 400
        
        # Get current user (JWT identity is a string, convert to int)
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Create quiz
        quiz = Quiz(
            title=title,
            description=description,
            created_by=user_id,
            is_active=is_active
        )
        db.session.add(quiz)
        db.session.flush()  # Get quiz.id
        
        # Create questions
        for idx, q_data in enumerate(questions_data):
            question = Question(
                quiz_id=quiz.id,
                question_text=q_data.get('question_text', '').strip(),
                question_type=q_data.get('question_type', '').strip().lower(),
                options=q_data.get('options', []),
                correct_answer=q_data.get('correct_answer', '').strip(),
                points=q_data.get('points', 1),
                order=idx
            )
            db.session.add(question)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz created successfully',
            'quiz': quiz.to_dict(include_answers=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create quiz', 'message': str(e)}), 500


@quizzes_bp.route('/<int:quiz_id>', methods=['PUT'])
@jwt_required()
def update_quiz(quiz_id):
    """Update a quiz (admin only)"""
    try:
        # Check admin access
        admin_check = require_admin()
        if admin_check:
            return admin_check
        
        quiz = Quiz.query.get_or_404(quiz_id)
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Update basic fields
        if 'title' in data:
            quiz.title = data['title'].strip()
        if 'description' in data:
            quiz.description = data['description'].strip() or None
        if 'is_active' in data:
            quiz.is_active = bool(data['is_active'])
        
        # Update questions if provided
        if 'questions' in data:
            questions_data = data['questions']
            
            # Validate questions
            for idx, q_data in enumerate(questions_data):
                question_text = q_data.get('question_text', '').strip()
                question_type = q_data.get('question_type', '').strip().lower()
                correct_answer = q_data.get('correct_answer', '').strip()
                points = q_data.get('points', 1)
                options = q_data.get('options', [])
                
                if not question_text:
                    return jsonify({'error': f'Question {idx + 1}: Question text is required'}), 400
                if question_type not in ['multiple_choice', 'true_false', 'text']:
                    return jsonify({'error': f'Question {idx + 1}: Invalid question type'}), 400
                if not correct_answer:
                    return jsonify({'error': f'Question {idx + 1}: Correct answer is required'}), 400
                
                # Validate options for MCQ
                if question_type == 'multiple_choice':
                    if not options or len(options) < 2:
                        return jsonify({'error': f'Question {idx + 1}: Multiple choice questions require at least 2 options'}), 400
                    if correct_answer not in options:
                        return jsonify({'error': f'Question {idx + 1}: Correct answer must be one of the options'}), 400
                elif question_type == 'true_false':
                    if correct_answer.lower() not in ['true', 'false']:
                        return jsonify({'error': f'Question {idx + 1}: True/False questions must have "True" or "False" as correct answer'}), 400
            
            # Delete existing questions
            Question.query.filter_by(quiz_id=quiz_id).delete()
            
            # Create new questions
            for idx, q_data in enumerate(questions_data):
                question = Question(
                    quiz_id=quiz_id,
                    question_text=q_data.get('question_text', '').strip(),
                    question_type=q_data.get('question_type', '').strip().lower(),
                    options=q_data.get('options', []),
                    correct_answer=q_data.get('correct_answer', '').strip(),
                    points=q_data.get('points', 1),
                    order=idx
                )
                db.session.add(question)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz updated successfully',
            'quiz': quiz.to_dict(include_answers=True)
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update quiz', 'message': str(e)}), 500


@quizzes_bp.route('/<int:quiz_id>', methods=['DELETE'])
@jwt_required()
def delete_quiz(quiz_id):
    """Delete a quiz (admin only)"""
    try:
        # Check admin access
        admin_check = require_admin()
        if admin_check:
            return admin_check
        
        quiz = Quiz.query.get_or_404(quiz_id)
        
        db.session.delete(quiz)
        db.session.commit()
        
        return jsonify({'message': 'Quiz deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete quiz', 'message': str(e)}), 500

