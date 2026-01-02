import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { quizAPI } from '../utils/api';

function LandingPage() {
  const [quizzes, setQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchQuizzes();
  }, []);

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
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Welcome to Quiz App
          </h1>
          <p className="text-xl text-gray-600">
            Test your knowledge with our interactive quizzes
          </p>
        </div>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {quizzes.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 text-lg">No quizzes available yet.</p>
            <p className="text-gray-500 mt-2">
              Check back later or login as admin to create quizzes.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {quizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-6"
              >
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {quiz.title}
                </h3>
                {quiz.description && (
                  <p className="text-gray-600 mb-4 line-clamp-2">
                    {quiz.description}
                  </p>
                )}
                <div className="flex items-center justify-between mt-4">
                  <span className="text-sm text-gray-500">
                    {quiz.questions?.length || 0} questions
                  </span>
                  <Link
                    to={`/quizzes/${quiz.id}`}
                    className="bg-orange-400 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors"
                  >
                    Take Quiz
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default LandingPage;

