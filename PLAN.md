# Quiz App Plan
I'm building a quiz management app for this assignment. The basic idea is pretty straightforward - admins can create quizzes and regular users can take them and see their results. I want to make sure it's actually deployable and shows decent architecture, even if it's a time-boxed project.

## What I'm building

Core features:
- Admin can create quizzes with multiple questions
- Users can take quizzes and see their score + which questions they got right/wrong
- Basic auth for the admin area (probably just login, maybe seed an admin user)
- Keep it simple but clean architecture-wise

## Scope

### What I'm including

Admin stuff:
- Admin login (maybe registration, but probably just seed one admin user to save time)
- Create quizzes with:
  - Title and description (description optional)
  - Multiple questions
  - Question types: multiple choice and true/false for now (can extend later)
- View list of all quizzes

User stuff:
- See list of available quizzes
- Take a quiz
- Submit and see:
  - Total score
  - Which questions were correct/incorrect

Tech requirements:
- REST API for everything (auth, quizzes, submissions)
- React frontend that talks to the API
- PostgreSQL 18 database with proper relationships
- Basic error handling and validation
- CORS setup so frontend and backend can communicate

### What I'm NOT doing (to keep scope manageable)

- No multi-tenant stuff or complex role systems (just admin vs student)
- No fancy quiz features like timers, negative marking, question randomization, analytics dashboards
- UI will be functional but minimal - not spending time on a design system
- No full i18n, accessibility audits, or comprehensive test suite (just basic manual testing)

### Assumptions

- Single environment (no staging/prod separation)
- Probably just one or a few admin users
- Small number of quizzes/questions, so don't need to worry about performance too much
- Backend and DB on single instance (no scaling concerns)

## Tech Stack

Frontend:
- React + Vite 
- JavaScript
- Tailwind CSS

Backend:
- Python Flask 
- Flask-SQLAlchemy for ORM
- Flask-Migrate for migrations
- Flask-CORS for CORS
- Flask-JWT-Extended for auth tokens
- Maybe Marshmallow for request/response schemas if I need it

Database:
- PostgreSQL 18 (database name: `quizdb`)
- SQLAlchemy models: User, Quiz, Question, maybe UserResponse

Tooling:
- Git + GitHub
- Using Cursor/AI for boilerplate stuff (but reviewing everything)
- Might record a demo with OBS or similar

## Architecture Overview

### Backend Structure

**app.py**
- Main Flask app
- Load config, initialize extensions:
  - db (SQLAlchemy)
  - Migrate
  - JWTManager
  - CORS
- Register blueprints:
  - `/api/auth` - login/register
  - `/api/quizzes` - quiz CRUD
  - `/api/responses` - quiz submission and scoring

**config.py**
- Config class with:
  - `SQLALCHEMY_DATABASE_URI` - `postgresql://postgres:postgres@localhost/quizdb` (or from env `DATABASE_URL`)
  - `SECRET_KEY`, `JWT_SECRET_KEY` from env vars
  - `SQLALCHEMY_TRACK_MODIFICATIONS = False` (always set this)

**models.py**
- `User`: id, username, email, password_hash, role, created_at
  - Methods: set_password, check_password, to_dict
- `Quiz`: id, title, description, created_by, created_at, is_active
  - Relationships: questions, responses
- `Question`: id, quiz_id, question_text, question_type, options (JSON), correct_answer, points
- `UserResponse` (maybe): id, user_id, quiz_id, answers (JSON), score, submitted_at

**API Routes**
- `/api/auth/login` - email/username + password → JWT token + role
- `/api/auth/register` - optional, or just seed an admin
- `/api/quizzes` (admin only):
  - POST - create quiz + questions in one request
  - GET - list all quizzes
- `/api/quizzes/<id>`:
  - GET - quiz details + questions (without correct answers)
- `/api/quizzes/<id>/submit`:
  - POST - user answers → calculate score and return results

### Frontend Structure

**App routing** (probably React Router, or maybe just simple routing):
- `/login` - admin login page
- `/admin/quizzes` - list quizzes, link to create new
- `/admin/quizzes/new` - create quiz form
- `/quizzes` - public quiz list
- `/quizzes/:id` - take quiz page

**State management:**
- Store JWT token in localStorage or memory
- Attach token to admin API requests (Authorization header)
- On quiz submit, show score and per-question feedback

## Data Model

**users table:**
- id (PK, integer)
- username (string)
- email (string)
- password_hash (string)
- role (string: 'admin' or 'student')
- created_at (datetime)

**quizzes table:**
- id (PK, integer)
- title (string)
- description (text, nullable)
- created_by (FK to users.id)
- created_at (datetime)
- is_active (boolean)

**questions table:**
- id (PK, integer)
- quiz_id (FK to quizzes.id)
- question_text (text)
- question_type (string: 'multiple_choice', 'true_false', maybe 'short_text')
- options (JSON - for MCQ/TF)
- correct_answer (string)
- points (integer)

**user_responses table** (if I have time):
- id (PK, integer)
- user_id (FK to users.id, nullable for anonymous)
- quiz_id (FK to quizzes.id)
- answers (JSON)
- score (integer)
- submitted_at (datetime)

## Development Plan

### Phase 1: Setup (~20-30 min)
- Create repo structure (backend/, frontend/, .gitignore, README)
- Set up Python venv, install Flask deps
- Set up Vite React app
- Initial commit

### Phase 2: Backend core (~30-40 min)
- Implement Config, models, DB init
- Create and run initial migration
- Implement auth routes (login, maybe register/seed admin)
- Implement quiz routes:
  - POST /api/quizzes
  - GET /api/quizzes
  - GET /api/quizzes/<id>
  - POST /api/quizzes/<id>/submit (with scoring logic)

### Phase 3: Frontend core (~40-50 min)
- Build login page, store JWT
- Build admin "Create Quiz" page:
  - Form for quiz title/description
  - Dynamic question inputs (type, text, options, correct answer)
- Build quiz list and take-quiz pages:
  - List quizzes from API
  - Render questions, collect answers
  - Show score after submission

### Phase 4: Polish & testing (~20-30 min)
- Add basic validation and error messages
- Handle loading/error states in frontend
- Make sure CORS is working
- Test end-to-end:
  - Admin login → create quiz
  - User → list quizzes → take quiz → see score
- Update README and this plan with actual status
- Maybe record a quick demo

## Using AI/Cursor

I'm using Cursor and AI tools for:
- Generating boilerplate (Flask app skeleton, React component structure)
- Repetitive code (type definitions, basic validation)
- Refactoring help (splitting components, simplifying functions)

But I'm reviewing everything manually, testing it, and throwing out stuff that doesn't fit. Just documenting this to be transparent about the process.

## Changes from original plan

(Will update this as I go)

- Probably skipping UserResponse persistence for now - just compute score on submission
- Limiting to multiple_choice and true_false question types (short_text can wait)
- Might skip admin registration and just seed one admin user
- Keeping frontend routing simple (no nested routes)

## Future improvements (if I had more time)

- Full user registration and persistent UserResponse records with results page
- Quiz analytics (average scores, attempts, question difficulty)
- Better UX/UI, more validation, accessibility improvements
- Unit/integration tests for backend endpoints and frontend components
- Pagination and filtering for quizzes/submissions
- Better security (rate limiting, stricter validation, better error handling)
