export interface User {
  id: number
  email: string
  full_name: string
  preferred_language: string
  created_at: string
}

export interface Document {
  id: string
  filename: string
  document_type: 'pdf' | 'image' | 'text'
  page_count?: number
  created_at: string
  has_study_material: boolean
}

export interface MCQOption {
  text: string
  is_correct: boolean
}

export interface Question {
  id: string
  question_text: string
  question_type: 'mcq' | 'true_false' | 'short_answer' | 'fill_blank'
  options?: MCQOption[]
  correct_answer: string
  explanation: string
  difficulty: number
  topic: string
}

export interface Quiz {
  id: string
  title: string
  questions: Question[]
  total_questions: number
  estimated_time: number
}

export interface Flashcard {
  id: string
  front: string
  back: string
  topic: string
  difficulty: number
  repetitions: number
  ease_factor: number
  created_at: string
}

export interface StudyMaterial {
  document_id: string
  summary: string
  flashcards: Flashcard[]
  quiz: Quiz
  key_topics: string[]
}

export interface QuizResult {
  quiz_id: string
  score: number
  total_questions: number
  correct_answers: number
  time_taken: number
  weak_topics: string[]
  strong_topics: string[]
}

export interface ProgressStats {
  total_study_time: number
  study_streak: number
  topics_mastered: number
  average_quiz_score: number
  weak_subjects: string[]
  strong_subjects: string[]
  recent_activity: RecentActivity[]
}

export interface RecentActivity {
  type: string
  description: string
  timestamp: string
  score?: number
}

export interface TopicPerformance {
  topic: string
  accuracy: number
  questions_answered: number
  correct_answers: number
}

export interface HeatmapData {
  date: string
  study_time: number
  session_count: number
  intensity: number
}

export interface LearningCurvePoint {
  attempt_number: number
  score: number
  average_score: number
  date: string
  quiz_title: string
}

export interface TutorResponse {
  answer: string
  sources: string[]
  confidence: number
}