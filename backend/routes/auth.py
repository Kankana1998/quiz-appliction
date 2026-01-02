"""
Authentication routes for login and registration
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


def validate_email(email):
    """Basic email validation"""
    if not email or '@' not in email:
        return False
    return True


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user (admin or student)"""
    try:
        # Handle JSON parsing more gracefully
        if not request.is_json:
            # Try to parse as JSON even if Content-Type is not set
            try:
                data = request.get_json(force=True)
            except:
                return jsonify({
                    'error': 'Invalid request',
                    'message': 'Request must be JSON. Please set Content-Type: application/json header.'
                }), 400
        else:
            data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        role = data.get('role', 'student').strip().lower()
        
        # Validation
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        if not password or len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        if role not in ['admin', 'student']:
            return jsonify({'error': 'Role must be either "admin" or "student"'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # Create new user
        user = User(
            username=username,
            email=email,
            role=role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Generate token (identity must be a string)
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed', 'message': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        # Handle JSON parsing more gracefully
        if not request.is_json:
            # Try to parse as JSON even if Content-Type is not set
            try:
                data = request.get_json(force=True)
            except:
                return jsonify({
                    'error': 'Invalid request',
                    'message': 'Request must be JSON. Please set Content-Type: application/json header.'
                }), 400
        else:
            data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body is empty. Please provide username and password.',
                'example': {'username': 'admin', 'password': 'admin123'}
            }), 400
        
        username_or_email = data.get('username', '').strip() if data.get('username') else ''
        password = data.get('password', '') if data.get('password') else ''
        
        if not username_or_email:
            return jsonify({
                'error': 'Username or email is required',
                'message': 'Please provide a username or email in the request body.',
                'received': list(data.keys()) if data else []
            }), 400
        if not password:
            return jsonify({
                'error': 'Password is required',
                'message': 'Please provide a password in the request body.',
                'received': list(data.keys()) if data else []
            }), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate token (identity must be a string)
        access_token = create_access_token(identity=str(user.id), additional_claims={'role': user.role})
        
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Login error: {str(e)}")
        print(f"Traceback: {error_trace}")
        # Return detailed error in debug mode
        error_response = {'error': 'Login failed', 'message': str(e)}
        if current_app.debug:
            error_response['details'] = error_trace
        return jsonify(error_response), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current authenticated user"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get user', 'message': str(e)}), 500

