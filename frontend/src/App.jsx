import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import LandingPage from './pages/LandingPage';
import AdminLogin from './pages/AdminLogin';
import AdminQuizzes from './pages/AdminQuizzes';
import CreateQuiz from './pages/CreateQuiz';
import EditQuiz from './pages/EditQuiz';
import TakeQuiz from './pages/TakeQuiz';

function App() {
  const [isAdmin, setIsAdmin] = useState(false);

  useEffect(() => {
    // Check if user is logged in as admin
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    setIsAdmin(user.role === 'admin');
  }, []);

  const handleLogout = () => {
    setIsAdmin(false);
  };

  const handleLogin = () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    setIsAdmin(user.role === 'admin');
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar isAdmin={isAdmin} onLogout={handleLogout} />
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/admin/login" element={<AdminLogin onLogin={handleLogin} />} />
          <Route path="/admin/quizzes" element={<AdminQuizzes />} />
          <Route path="/admin/quizzes/new" element={<CreateQuiz />} />
          <Route path="/admin/quizzes/:id/edit" element={<EditQuiz />} />
          <Route path="/quizzes/:id" element={<TakeQuiz />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
