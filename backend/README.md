# Quiz Management System - Backend

Production-ready Flask backend for the Quiz Management System.

## Features

- **Authentication**: JWT-based authentication for admin users only
- **Student Access**: Students can participate in quizzes without login (just provide name)
- **Quiz Management**: Create, read, update, and delete quizzes (admin only)
- **Question Types**: Multiple choice, True/False, and text questions
- **Quiz Submissions**: Submit quizzes and get instant results with scoring
- **Response Tracking**: Store user responses with participant names for analytics

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory (or use the provided template):

```env
# Database: Leave DATABASE_URL unset to use SQLite (default for development)
# For PostgreSQL, uncomment and update:
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quizdb

SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ACCESS_TOKEN_EXPIRES=3600
CORS_ORIGINS=http://localhost:5173
```

**Note:** By default, the app uses SQLite (no setup required). The database file `quiz_app.db` will be created automatically in the `backend/` directory. For production, use PostgreSQL by setting the `DATABASE_URL` environment variable.

### 3. Database Setup

**For SQLite (Default - No PostgreSQL Required):**

The app will automatically use SQLite if `DATABASE_URL` is not set. Just initialize migrations:

```bash
# Initialize migrations (only needed once)
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migrations (creates quiz_app.db file)
flask db upgrade
```

**For PostgreSQL (Production):**

1. Install and start PostgreSQL
2. Create database: `CREATE DATABASE quizdb;`
3. Set `DATABASE_URL` in `.env` file
4. Run migrations as above

### 4. Create Admin User

Run the seed script to create an initial admin user:

```bash
python seed.py
```

Default admin credentials:
- Username: `admin`
- Password: `admin123`

**⚠️ IMPORTANT: Change the admin password in production!**

## Running the Application

### Development Mode

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Production Mode

Use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Endpoints

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/me` - Get current user (requires auth)

### Quizzes

- `GET /api/quizzes` - Get all quizzes (public) or all quizzes (admin)
- `GET /api/quizzes/<id>` - Get quiz details
- `POST /api/quizzes` - Create a new quiz (admin only)
- `PUT /api/quizzes/<id>` - Update a quiz (admin only)
- `DELETE /api/quizzes/<id>` - Delete a quiz (admin only)

### Submissions

- `POST /api/submissions/quizzes/<id>/submit` - Submit quiz answers (no authentication required for students)
  - Request body: `{ "name": "Student Name", "answers": { "1": "answer1", "2": "answer2" } }`
  - The `name` field is optional but recommended for displaying in results
- `GET /api/submissions/quizzes/<id>/submissions` - Get all submissions for a quiz (admin only)
- `GET /api/submissions/my-submissions` - Get current user's submissions (requires authentication)

### Health Check

- `GET /api/health` - Health check endpoint

## API Usage Examples

### Register Admin User

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "securepassword",
    "role": "admin"
  }'
```

### Login

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "securepassword"
  }'
```

### Create Quiz (Admin)

```bash
curl -X POST http://localhost:5000/api/quizzes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "title": "Python Basics",
    "description": "Test your Python knowledge",
    "is_active": true,
    "questions": [
      {
        "question_text": "What is Python?",
        "question_type": "multiple_choice",
        "options": ["A programming language", "A snake", "A framework"],
        "correct_answer": "A programming language",
        "points": 10
      },
      {
        "question_text": "Python is dynamically typed.",
        "question_type": "true_false",
        "correct_answer": "True",
        "points": 5
      }
    ]
  }'
```

### Submit Quiz (Student - No Authentication Required)

```bash
curl -X POST http://localhost:5000/api/submissions/quizzes/1/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "answers": {
      "1": "A programming language",
      "2": "True"
    }
  }'
```

**Note:** The `name` field is optional. If provided, it will be displayed in the results and stored with the submission.

## Database Models

### User
- `id` (PK)
- `username` (unique)
- `email` (unique)
- `password_hash`
- `role` (admin/student)
- `created_at`

### Quiz
- `id` (PK)
- `title`
- `description`
- `created_by` (FK to User)
- `created_at`
- `is_active`

### Question
- `id` (PK)
- `quiz_id` (FK to Quiz)
- `question_text`
- `question_type` (multiple_choice/true_false/text)
- `options` (JSON)
- `correct_answer`
- `points`
- `order`

### UserResponse
- `id` (PK)
- `user_id` (FK to User, nullable - for authenticated users)
- `quiz_id` (FK to Quiz)
- `participant_name` (String, nullable - for anonymous student submissions)
- `answers` (JSON)
- `score`
- `total_points`
- `submitted_at`

## Production Considerations

1. **Security**:
   - Change all default passwords
   - Use strong SECRET_KEY and JWT_SECRET_KEY
   - Enable HTTPS in production
   - Implement rate limiting
   - Add input sanitization

2. **Database**:
   - Use connection pooling
   - Set up database backups
   - Monitor query performance

3. **Deployment**:
   - Use environment variables for all secrets
   - Set `FLASK_ENV=production`
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Set up proper logging
   - Configure CORS for your frontend domain

4. **Monitoring**:
   - Set up error tracking (Sentry, etc.)
   - Monitor API response times
   - Track database performance

## License

MIT

