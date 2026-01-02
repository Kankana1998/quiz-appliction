// API utility functions
const API_BASE_URL = 'http://localhost:5001/api';

// Helper function to make API requests
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if available
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || data.error || 'Request failed');
    }

    return data;
  } catch (error) {
    throw error;
  }
}

// Auth API
export const authAPI = {
  login: async (username, password) => {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  },
  register: async (username, email, password, role = 'student') => {
    return apiRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password, role }),
    });
  },
  getCurrentUser: async () => {
    return apiRequest('/auth/me');
  },
};

// Quiz API
export const quizAPI = {
  getAll: async () => {
    return apiRequest('/quizzes');
  },
  getById: async (id) => {
    return apiRequest(`/quizzes/${id}`);
  },
  create: async (quizData) => {
    return apiRequest('/quizzes', {
      method: 'POST',
      body: JSON.stringify(quizData),
    });
  },
  update: async (id, quizData) => {
    return apiRequest(`/quizzes/${id}`, {
      method: 'PUT',
      body: JSON.stringify(quizData),
    });
  },
  delete: async (id) => {
    return apiRequest(`/quizzes/${id}`, {
      method: 'DELETE',
    });
  },
};

// Submission API
export const submissionAPI = {
  submit: async (quizId, name, answers) => {
    return apiRequest(`/submissions/quizzes/${quizId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ name, answers }),
    });
  },
  getMySubmissions: async () => {
    return apiRequest('/submissions/my-submissions');
  },
  getQuizSubmissions: async (quizId) => {
    return apiRequest(`/submissions/quizzes/${quizId}/submissions`);
  },
};

