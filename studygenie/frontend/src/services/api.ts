import axios from 'axios'
import {
  User,
  Document,
  StudyMaterial,
  Quiz,
  QuizResult,
  Flashcard,
  ProgressStats,
  TopicPerformance,
  HeatmapData,
  LearningCurvePoint,
  TutorResponse,
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await api.post('/api/auth/login', { email, password })
    return response.data
  },
  
  register: async (userData: {
    email: string
    password: string
    full_name: string
    preferred_language: string
  }) => {
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },
  
  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/api/auth/me')
    return response.data
  },
}

export const uploadAPI = {
  uploadDocument: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    
    const response = await api.post('/api/upload/document', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },
  
  generateStudyMaterial: async (documentId: string): Promise<StudyMaterial> => {
    const response = await api.post(`/api/upload/generate-study-material/${documentId}`)
    return response.data
  },
  
  getUserDocuments: async (): Promise<Document[]> => {
    const response = await api.get('/api/upload/documents')
    return response.data
  },
  
  deleteDocument: async (documentId: string) => {
    const response = await api.delete(`/api/upload/document/${documentId}`)
    return response.data
  },
}

export const studyAPI = {
  getQuiz: async (quizId: string): Promise<Quiz> => {
    const response = await api.get(`/api/study/quiz/${quizId}`)
    return response.data
  },
  
  submitQuizAttempt: async (quizId: string, answers: Record<string, string>): Promise<QuizResult> => {
    const response = await api.post(`/api/study/quiz/${quizId}/attempt`, {
      quiz_id: quizId,
      answers,
    })
    return response.data
  },
  
  getDueFlashcards: async (): Promise<Flashcard[]> => {
    const response = await api.get('/api/study/flashcards/due')
    return response.data
  },
  
  reviewFlashcard: async (flashcardId: string, quality: number) => {
    const response = await api.post(`/api/study/flashcard/${flashcardId}/review?quality=${quality}`)
    return response.data
  },
  
  askTutor: async (question: string, documentId?: string, language: string = 'en'): Promise<TutorResponse> => {
    const response = await api.post('/api/study/tutor/ask', {
      question,
      document_id: documentId,
      language,
    })
    return response.data
  },
  
  explainAnswer: async (quizId: string, questionId: string, userAnswer: string) => {
    const response = await api.get(
      `/api/study/quiz/${quizId}/explain/${questionId}?user_answer=${encodeURIComponent(userAnswer)}`
    )
    return response.data
  },
  
  startStudySession: async (sessionData: {
    document_id: string
    session_type: string
    duration: number
    score?: number
  }) => {
    const response = await api.post('/api/study/session/start', sessionData)
    return response.data
  },
}

export const progressAPI = {
  getDashboardStats: async (): Promise<ProgressStats> => {
    const response = await api.get('/api/progress/dashboard')
    return response.data
  },
  
  getStudyHeatmap: async (): Promise<{ heatmap_data: HeatmapData[] }> => {
    const response = await api.get('/api/progress/study-heatmap')
    return response.data
  },
  
  getTopicPerformance: async (): Promise<{ topic_performance: TopicPerformance[] }> => {
    const response = await api.get('/api/progress/topic-performance')
    return response.data
  },
  
  getLearningCurve: async (): Promise<{ learning_curve: LearningCurvePoint[] }> => {
    const response = await api.get('/api/progress/learning-curve')
    return response.data
  },
}

export default api