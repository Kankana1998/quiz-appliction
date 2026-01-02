"""
Seed script to create initial admin user
Run: python seed.py
"""
from app import app
from models import db, User

def create_admin():
    """Create an admin user if it doesn't exist"""
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
        admin = User(
            username='admin',
            email='admin@quizapp.com',
            role='admin'
        )
        admin.set_password('admin123')  # Change this in production!
        
        db.session.add(admin)
        db.session.commit()
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("⚠️  IMPORTANT: Change the password in production!")

if __name__ == '__main__':
    create_admin()

