import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (formData) => api.post('/auth/token', formData),
  register: (userData) => api.post('/auth/register', userData),
  getProfile: () => api.get('/auth/me'),
};

// Documents API
export const documentsAPI = {
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAll: () => api.get('/documents/'),
  getById: (id) => api.get(`/documents/${id}`),
  delete: (id) => api.delete(`/documents/${id}`),
  reprocess: (id) => api.post(`/documents/${id}/reprocess`),
};

// Study Materials API
export const studyAPI = {
  generate: (data) => api.post('/study/generate', data),
  getAll: (contentType) => api.get('/study/', { params: { content_type: contentType } }),
  getById: (id) => api.get(`/study/${id}`),
  getQuiz: (materialId) => api.get(`/study/${materialId}/quiz`),
  getFlashcards: (materialId, dueOnly = false) => api.get(`/study/${materialId}/flashcards`, {
    params: { due_only: dueOnly }
  }),
  reviewFlashcard: (reviewData) => api.post('/study/flashcards/review', reviewData),
  delete: (id) => api.delete(`/study/${id}`),
};

// Progress API
export const progressAPI = {
  getDashboard: () => api.get('/progress/dashboard'),
  logSession: (sessionData) => api.post('/progress/session', sessionData),
  submitQuizAttempt: (attemptData) => api.post('/progress/quiz-attempt', attemptData),
  getAll: () => api.get('/progress/'),
  getBySubject: (subject) => api.get(`/progress/${subject}`),
};

// AI Tutor API
export const aiTutorAPI = {
  indexDocument: (data) => api.post('/ai-tutor/index-document', data),
  chat: (chatData) => api.post('/ai-tutor/chat', chatData),
  getIndexedDocuments: () => api.get('/ai-tutor/documents'),
  removeDocumentIndex: (documentId) => api.delete(`/ai-tutor/index/${documentId}`),
};

export default api;