"""
Submission routes for quiz submissions and scoring
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models import db, Quiz, Question, UserResponse, User
from datetime import datetime

submissions_bp = Blueprint('submissions', __name__)


@submissions_bp.route('/quizzes/<int:quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    """Submit quiz answers and get results (no authentication required for students)"""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        # Check if quiz is active
        if not quiz.is_active:
            return jsonify({'error': 'Quiz is not available'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        answers = data.get('answers', {})  # {question_id: answer}
        participant_name = data.get('name', '').strip()  # Student name (optional)
        
        if not answers:
            return jsonify({'error': 'No answers provided'}), 400
        
        # Get user ID if authenticated (optional - only for logged-in users)
        user_id = None
        try:
            user_id_str = get_jwt_identity()
            user_id = int(user_id_str) if user_id_str else None
        except:
            pass  # Anonymous submission - this is allowed for students
        
        # Calculate score
        total_points = 0
        earned_points = 0
        results = {}
        
        for question in quiz.questions:
            question_id = question.id
            user_answer = answers.get(str(question_id)) or answers.get(question_id)
            
            total_points += question.points
            is_correct = question.check_answer(user_answer) if user_answer is not None else False
            
            if is_correct:
                earned_points += question.points
            
            results[question_id] = {
                'question_id': question_id,
                'question_text': question.question_text,
                'question_type': question.question_type,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
                'points': question.points,
                'earned_points': question.points if is_correct else 0
            }
        
        # Save response to database
        response = UserResponse(
            user_id=user_id,
            quiz_id=quiz_id,
            participant_name=participant_name if participant_name else None,
            answers=answers,
            score=earned_points,
            total_points=total_points
        )
        db.session.add(response)
        db.session.commit()
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'participant_name': participant_name,
            'score': earned_points,
            'total_points': total_points,
            'percentage': round((earned_points / total_points * 100) if total_points > 0 else 0, 2),
            'results': results,
            'submission_id': response.id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit quiz', 'message': str(e)}), 500


@submissions_bp.route('/quizzes/<int:quiz_id>/submissions', methods=['GET'])
@jwt_required()
def get_quiz_submissions(quiz_id):
    """Get all submissions for a quiz (admin only)"""
    try:
        # Check admin access
        claims = get_jwt()
        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        quiz = Quiz.query.get_or_404(quiz_id)
        
        submissions = UserResponse.query.filter_by(quiz_id=quiz_id).order_by(
            UserResponse.submitted_at.desc()
        ).all()
        
        return jsonify({
            'quiz_id': quiz_id,
            'quiz_title': quiz.title,
            'submissions': [sub.to_dict() for sub in submissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch submissions', 'message': str(e)}), 500


@submissions_bp.route('/my-submissions', methods=['GET'])
@jwt_required()
def get_my_submissions():
    """Get current user's submissions"""
    try:
        user_id_str = get_jwt_identity()
        user_id = int(user_id_str)
        
        submissions = UserResponse.query.filter_by(user_id=user_id).order_by(
            UserResponse.submitted_at.desc()
        ).all()
        
        return jsonify({
            'submissions': [sub.to_dict() for sub in submissions]
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch submissions', 'message': str(e)}), 500

