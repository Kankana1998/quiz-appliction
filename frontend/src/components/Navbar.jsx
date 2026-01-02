import { Link, useNavigate } from 'react-router-dom';

function Navbar({ isAdmin, onLogout }) {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('user');
    if (onLogout) onLogout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="text-3xl font-bold text-orange-500">
              Quiz App
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            {isAdmin ? (
              <>
                <Link
                  to="/admin/quizzes"
                  className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  My Quizzes
                </Link>
                <Link
                  to="/admin/quizzes/new"
                  className="bg-orange-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-orange-700"
                >
                  Create Quiz
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-sm font-medium"
                >
                  Logout
                </button>
              </>
            ) : (
              <Link
                to="/admin/login"
                className="bg-orange-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
              >
                Login as Admin
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;

