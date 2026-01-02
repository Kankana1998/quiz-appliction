# Frontend Setup Instructions

## Installation Steps

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

   This will install:
   - React Router DOM (for routing)
   - Tailwind CSS and its dependencies
   - All other required packages

2. **Start the development server:**
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Navbar.jsx          # Navigation bar with Login button
│   ├── pages/
│   │   ├── LandingPage.jsx     # Public quiz list (homepage)
│   │   ├── AdminLogin.jsx      # Admin login page
│   │   ├── AdminQuizzes.jsx   # Admin dashboard (quiz management)
│   │   ├── CreateQuiz.jsx      # Create new quiz form
│   │   └── TakeQuiz.jsx        # Take quiz page (public)
│   ├── utils/
│   │   └── api.js              # API utility functions
│   ├── App.jsx                  # Main app with routing
│   ├── main.jsx                 # Entry point
│   └── index.css                # Tailwind CSS imports
├── tailwind.config.js           # Tailwind configuration
├── postcss.config.js            # PostCSS configuration
└── package.json
```

## Features Implemented

✅ **Public Landing Page** - No login required
- Displays all active quizzes
- "Take Quiz" button for each quiz
- "Login as Admin" button in navbar

✅ **Admin Login**
- Secure login with JWT authentication
- Redirects to admin dashboard on success

✅ **Admin Dashboard**
- View all quizzes
- Create new quizzes
- Edit/Delete quizzes
- Logout functionality

✅ **Create Quiz Form**
- Add quiz title and description
- Add multiple questions
- Support for:
  - Multiple Choice questions
  - True/False questions
  - Text answer questions
- Set points for each question

✅ **Take Quiz Page**
- Enter name (no login required)
- Answer all questions
- Submit and see results with:
  - Score and percentage
  - Per-question feedback
  - Correct/incorrect answers

## API Configuration

The API base URL is set in `src/utils/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:5001/api';
```

Make sure your backend is running on port 5001 (or update this URL if different).

## Routes

- `/` - Landing page (public quiz list)
- `/admin/login` - Admin login page
- `/admin/quizzes` - Admin dashboard
- `/admin/quizzes/new` - Create new quiz
- `/quizzes/:id` - Take quiz page

## Styling

The app uses Tailwind CSS for all styling. All components are fully responsive and use Tailwind utility classes.

## Next Steps

1. Run `npm install` to install dependencies
2. Start the dev server with `npm run dev`
3. Make sure the backend is running on port 5001
4. Test the application!

