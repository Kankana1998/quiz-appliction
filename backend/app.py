"""
Main Flask application for Quiz Management System
"""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade
from config import Config
from models import db

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    try:
        upgrade()
        print("✅ Database migrations completed successfully")
    except Exception as e:
        # Log error but don't crash - migrations might already be up to date or not initialized
        error_msg = str(e)
        if "Target database is not up to date" in error_msg or "Can't locate revision" in error_msg:
            print(f"⚠️  Migration note: {error_msg}")
        else:
            print(f"⚠️  Migration warning: {error_msg}")
        # App will still start - migrations can be run manually if needed

# Configure JWT
app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = app.config.get('JWT_ACCESS_TOKEN_EXPIRES', 3600)
jwt = JWTManager(app)

# Configure CORS - handle both string and list formats
cors_origins = app.config.get('CORS_ORIGINS', [])
if isinstance(cors_origins, str):
    # If it's a string, split by comma and strip whitespace
    cors_origins = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
elif not isinstance(cors_origins, list):
    # Fallback to default if not string or list
    cors_origins = ['http://localhost:5173']

cors = CORS(app, origins=cors_origins, supports_credentials=True)

# Register blueprints
from routes.auth import auth_bp
from routes.quizzes import quizzes_bp
from routes.submissions import submissions_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(quizzes_bp, url_prefix='/api/quizzes')
app.register_blueprint(submissions_bp, url_prefix='/api/submissions')


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    """Handle 400 Bad Request errors"""
    return jsonify({'error': 'Bad request', 'message': str(error)}), 400


@app.errorhandler(401)
def unauthorized(error):
    """Handle 401 Unauthorized errors"""
    return jsonify({'error': 'Unauthorized', 'message': 'Authentication required'}), 401


@app.errorhandler(403)
def forbidden(error):
    """Handle 403 Forbidden errors"""
    return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource'}), 403


@app.errorhandler(404)
def not_found(error):
    """Handle 404 Not Found errors"""
    return jsonify({'error': 'Not found', 'message': 'The requested resource was not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error', 'message': 'An unexpected error occurred'}), 500


# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Quiz API is running'}), 200


if __name__ == '__main__':
    # Default to port 5001 to avoid conflict with macOS AirPlay Receiver on port 5000
    # Can be overridden with PORT environment variable: PORT=5000 python app.py
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)

