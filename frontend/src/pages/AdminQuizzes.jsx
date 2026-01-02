import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { quizAPI } from '../utils/api';

function AdminQuizzes() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('authToken');
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    if (!token || user.role !== 'admin') {
      navigate('/admin/login');
      return;
    }

    fetchQuizzes();
  }, [navigate]);

  const fetchQuizzes = async () => {
    try {
      setLoading(true);
      const response = await quizAPI.getAll();
      setQuizzes(response.quizzes || []);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load quizzes');
      console.error('Error fetching quizzes:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this quiz?')) {
      return;
    }

    try {
      await quizAPI.delete(id);
      setQuizzes(quizzes.filter((quiz) => quiz.id !== id));
    } catch (err) {
      alert(err.message || 'Failed to delete quiz');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading quizzes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">My Quizzes</h1>
          <Link
            to="/admin/quizzes/new"
            className="bg-orange-600 text-white px-6 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
          >
            Create New Quiz
          </Link>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {quizzes.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg shadow">
            <p className="text-gray-600 text-lg mb-4">No quizzes yet.</p>
            <Link
              to="/admin/quizzes/new"
              className="inline-block bg-blue-600 text-white px-6 py-2 rounded-md text-sm font-medium hover:bg-blue-700"
            >
              Create Your First Quiz
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
              >
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-xl font-semibold text-gray-900">
                    {quiz.title}
                  </h3>
                  <span
                    className={`px-2 py-1 text-xs rounded ${
                      quiz.is_active
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {quiz.is_active ? 'Active' : 'Inactive'}
                  </span>
                </div>
                {quiz.description && (
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {quiz.description}
                  </p>
                )}
                <div className="flex items-center justify-between mt-4">
                  <span className="text-sm text-gray-500">
                    {quiz.questions?.length || 0} questions
                  </span>
                  <div className="flex space-x-2">
                    <Link
                      to={`/admin/quizzes/${quiz.id}/edit`}
                      className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                    >
                      Edit
                    </Link>
                    <button
                      onClick={() => handleDelete(quiz.id)}
                      className="text-red-600 hover:text-red-800 text-sm font-medium"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminQuizzes;

