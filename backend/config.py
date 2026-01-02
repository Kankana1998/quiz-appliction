import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration class"""
    
    # Database configuration
    # Default to SQLite for development (no setup required)
    # For production, set DATABASE_URL environment variable to PostgreSQL connection string
    _database_url = os.getenv('DATABASE_URL')
    
    if _database_url:
        # PostgreSQL connection string provided
        # Convert postgresql:// to postgresql+psycopg:// for psycopg v3
        if _database_url.startswith('postgresql://'):
            _database_url = _database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        SQLALCHEMY_DATABASE_URI = _database_url
    else:
        # Use SQLite for development (file-based, no setup needed)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Secret keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    
    # JWT configuration
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hour default
    
    # CORS configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

