import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { quizAPI, submissionAPI } from '../utils/api';

function TakeQuiz() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [participantName, setParticipantName] = useState('');
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);

  useEffect(() => {
    fetchQuiz();
  }, [id]);

  const fetchQuiz = async () => {
    try {
      setLoading(true);
      const response = await quizAPI.getById(id);
      setQuiz(response.quiz);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load quiz');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: answer,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!participantName.trim()) {
      alert('Please enter your name');
      return;
    }

    try {
      setLoading(true);
      const response = await submissionAPI.submit(
        parseInt(id),
        participantName.trim(),
        answers
      );
      setResults(response);
      setSubmitted(true);
    } catch (err) {
      setError(err.message || 'Failed to submit quiz');
    } finally {
      setLoading(false);
    }
  };

  if (loading && !submitted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading quiz...</p>
        </div>
      </div>
    );
  }

  if (error && !submitted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-lg mb-4">{error}</p>
          <button
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  if (submitted && results) {
    return (
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Quiz Results
            </h1>
            <p className="text-gray-600 mb-6">Great job, {results.participant_name}!</p>

            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
              <div className="text-center">
                <div className="text-4xl font-bold text-blue-600 mb-2">
                  {results.score} / {results.total_points}
                </div>
                <div className="text-2xl font-semibold text-gray-700">
                  {results.percentage}%
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h2 className="text-xl font-semibold text-gray-900">Question Review</h2>
              {Object.values(results.results).map((result, index) => (
                <div
                  key={result.question_id}
                  className={`border rounded-lg p-4 ${
                    result.is_correct
                      ? 'bg-green-50 border-green-200'
                      : 'bg-red-50 border-red-200'
                  }`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="font-medium text-gray-900">
                      Question {index + 1}
                    </h3>
                    <span
                      className={`px-2 py-1 text-xs rounded ${
                        result.is_correct
                          ? 'bg-green-200 text-green-800'
                          : 'bg-red-200 text-red-800'
                      }`}
                    >
                      {result.is_correct ? 'Correct' : 'Incorrect'}
                    </span>
                  </div>
                  <p className="text-gray-700 mb-2">{result.question_text}</p>
                  <div className="text-sm space-y-1">
                    <p>
                      <span className="font-medium">Your answer:</span>{' '}
                      <span className={result.is_correct ? 'text-green-700' : 'text-red-700'}>
                        {result.user_answer || 'No answer'}
                      </span>
                    </p>
                    {!result.is_correct && (
                      <p>
                        <span className="font-medium">Correct answer:</span>{' '}
                        <span className="text-green-700">{result.correct_answer}</span>
                      </p>
                    )}
                    <p className="text-gray-600">
                      Points: {result.earned_points} / {result.points}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 flex justify-center">
              <button
                onClick={() => navigate('/')}
                className="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700"
              >
                Back to Quizzes
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!quiz) return null;

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{quiz.title}</h1>
          {quiz.description && (
            <p className="text-gray-600 mb-6">{quiz.description}</p>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Your Name *
              </label>
              <input
                type="text"
                required
                value={participantName}
                onChange={(e) => setParticipantName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Enter your name"
              />
            </div>

            <div className="space-y-6 mb-6">
              {quiz.questions?.map((question, index) => (
                <div key={question.id} className="border border-gray-200 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">
                    Question {index + 1}: {question.question_text}
                  </h3>

                  {question.question_type === 'multiple_choice' && (
                    <div className="space-y-2">
                      {question.options?.map((option, optIndex) => (
                        <label
                          key={optIndex}
                          className="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer"
                        >
                          <input
                            type="radio"
                            name={`question-${question.id}`}
                            value={option}
                            checked={answers[question.id] === option}
                            onChange={() => handleAnswerChange(question.id, option)}
                            className="mr-3"
                          />
                          <span className="text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}

                  {question.question_type === 'true_false' && (
                    <div className="space-y-2">
                      {['True', 'False'].map((option) => (
                        <label
                          key={option}
                          className="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer"
                        >
                          <input
                            type="radio"
                            name={`question-${question.id}`}
                            value={option}
                            checked={answers[question.id] === option}
                            onChange={() => handleAnswerChange(question.id, option)}
                            className="mr-3"
                          />
                          <span className="text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  )}

                  {question.question_type === 'text' && (
                    <input
                      type="text"
                      value={answers[question.id] || ''}
                      onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your answer"
                    />
                  )}
                </div>
              ))}
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-orange-600 text-white px-6 py-3 rounded-md hover:bg-orange-700 disabled:opacity-50 font-medium"
            >
              {loading ? 'Submitting...' : 'Submit Quiz'}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default TakeQuiz;

