import React, { useState, useEffect } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  LinearProgress,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
} from '@mui/material'
import {
  Quiz as QuizIcon,
  Timer,
  CheckCircle,
  Cancel,
  Lightbulb,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from 'react-query'
import toast from 'react-hot-toast'

import { studyAPI } from '../services/api'
import { Quiz, QuizResult } from '../types'

const QuizPage: React.FC = () => {
  const { quizId } = useParams<{ quizId: string }>()
  const navigate = useNavigate()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [timeStarted, setTimeStarted] = useState<Date | null>(null)
  const [quizResult, setQuizResult] = useState<QuizResult | null>(null)
  const [showExplanation, setShowExplanation] = useState<string | null>(null)

  const { data: quiz, isLoading } = useQuery(
    ['quiz', quizId],
    () => studyAPI.getQuiz(quizId!),
    {
      enabled: !!quizId,
    }
  )

  const submitMutation = useMutation(
    () => studyAPI.submitQuizAttempt(quizId!, answers),
    {
      onSuccess: (result) => {
        setQuizResult(result)
        toast.success(`Quiz completed! Score: ${result.score}%`)
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Submission failed')
      },
    }
  )

  const explainMutation = useMutation(
    ({ questionId, userAnswer }: { questionId: string; userAnswer: string }) =>
      studyAPI.explainAnswer(quizId!, questionId, userAnswer),
    {
      onError: (error: any) => {
        toast.error('Failed to get explanation')
      },
    }
  )

  useEffect(() => {
    if (quiz && !timeStarted) {
      setTimeStarted(new Date())
    }
  }, [quiz])

  const currentQuestion = quiz?.questions[currentQuestionIndex]
  const progress = quiz ? ((currentQuestionIndex + 1) / quiz.questions.length) * 100 : 0
  const allAnswered = quiz?.questions.every(q => answers[q.id])

  const handleAnswerChange = (questionId: string, answer: string) => {
    setAnswers(prev => ({ ...prev, [questionId]: answer }))
  }

  const handleNext = () => {
    if (quiz && currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1)
    }
  }

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1)
    }
  }

  const handleSubmit = () => {
    if (allAnswered) {
      submitMutation.mutate()
    }
  }

  const handleExplainAnswer = (questionId: string, userAnswer: string) => {
    explainMutation.mutate({ questionId, userAnswer })
    setShowExplanation(questionId)
  }

  if (isLoading) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <LinearProgress />
        <Typography mt={2}>Loading quiz...</Typography>
      </Container>
    )
  }

  if (!quiz) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <Typography variant="h5">Quiz not found</Typography>
        <Button variant="contained" onClick={() => navigate('/dashboard')} sx={{ mt: 2 }}>
          Back to Dashboard
        </Button>
      </Container>
    )
  }

  // Show results
  if (quizResult) {
    return (
      <Container maxWidth="md" sx={{ py: 4 }}>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Paper elevation={3} sx={{ p: 4, borderRadius: 3, textAlign: 'center' }}>
            <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom fontWeight="bold">
              Quiz Complete! 🎉
            </Typography>
            
            <Box display="flex" justifyContent="center" gap={4} my={4}>
              <Box>
                <Typography variant="h3" fontWeight="bold" color="primary.main">
                  {quizResult.score.toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Final Score
                </Typography>
              </Box>
              <Box>
                <Typography variant="h3" fontWeight="bold">
                  {quizResult.correct_answers}/{quizResult.total_questions}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Correct Answers
                </Typography>
              </Box>
            </Box>

            {quizResult.weak_topics.length > 0 && (
              <Alert severity="info" sx={{ mb: 3, textAlign: 'left' }}>
                <Typography variant="subtitle2" gutterBottom>
                  Areas to focus on:
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                  {quizResult.weak_topics.map((topic) => (
                    <Chip key={topic} label={topic} size="small" color="warning" />
                  ))}
                </Box>
              </Alert>
            )}

            {quizResult.strong_topics.length > 0 && (
              <Alert severity="success" sx={{ mb: 3, textAlign: 'left' }}>
                <Typography variant="subtitle2" gutterBottom>
                  Strong areas:
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1}>
                  {quizResult.strong_topics.map((topic) => (
                    <Chip key={topic} label={topic} size="small" color="success" />
                  ))}
                </Box>
              </Alert>
            )}

            <Typography variant="h6" gutterBottom>
              Review Your Answers
            </Typography>
            
            <Box sx={{ maxHeight: 400, overflow: 'auto', mb: 3 }}>
              {quiz.questions.map((question, index) => {
                const userAnswer = answers[question.id]
                const isCorrect = userAnswer === question.correct_answer
                
                return (
                  <Card key={question.id} elevation={1} sx={{ mb: 2, textAlign: 'left' }}>
                    <CardContent>
                      <Box display="flex" alignItems="center" gap={1} mb={1}>
                        {isCorrect ? (
                          <CheckCircle color="success" />
                        ) : (
                          <Cancel color="error" />
                        )}
                        <Typography variant="subtitle2">
                          Question {index + 1}
                        </Typography>
                      </Box>
                      
                      <Typography variant="body2" paragraph>
                        {question.question_text}
                      </Typography>
                      
                      <Box display="flex" gap={2} mb={1}>
                        <Chip
                          label={`Your answer: ${userAnswer}`}
                          size="small"
                          color={isCorrect ? 'success' : 'error'}
                        />
                        {!isCorrect && (
                          <Chip
                            label={`Correct: ${question.correct_answer}`}
                            size="small"
                            color="success"
                            variant="outlined"
                          />
                        )}
                      </Box>

                      {!isCorrect && (
                        <Button
                          size="small"
                          startIcon={<Lightbulb />}
                          onClick={() => handleExplainAnswer(question.id, userAnswer)}
                          sx={{ mt: 1 }}
                        >
                          Explain Answer
                        </Button>
                      )}
                    </CardContent>
                  </Card>
                )
              })}
            </Box>

            <Box display="flex" gap={2} justifyContent="center">
              <Button variant="contained" onClick={() => navigate('/dashboard')}>
                Back to Dashboard
              </Button>
              <Button variant="outlined" onClick={() => navigate('/progress')}>
                View Progress
              </Button>
            </Box>
          </Paper>
        </motion.div>

        {/* Explanation Dialog */}
        <Dialog
          open={!!showExplanation}
          onClose={() => setShowExplanation(null)}
          maxWidth="sm"
          fullWidth
        >
          <DialogTitle>Answer Explanation</DialogTitle>
          <DialogContent>
            {explainMutation.isLoading ? (
              <LinearProgress />
            ) : explainMutation.data ? (
              <Typography variant="body2">
                {explainMutation.data.explanation}
              </Typography>
            ) : (
              <Typography variant="body2" color="text.secondary">
                Click "Explain Answer" to get an explanation
              </Typography>
            )}
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowExplanation(null)}>Close</Button>
          </DialogActions>
        </Dialog>
      </Container>
    )
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Header */}
        <Box display="flex" alignItems="center" justifyContent="between" mb={3}>
          <Box>
            <Typography variant="h5" gutterBottom fontWeight="bold">
              {quiz.title}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Question {currentQuestionIndex + 1} of {quiz.questions.length}
            </Typography>
          </Box>
          <Box display="flex" alignItems="center" gap={1}>
            <Timer />
            <Typography variant="body2">
              Est. {quiz.estimated_time} min
            </Typography>
          </Box>
        </Box>

        {/* Progress */}
        <Box mb={3}>
          <LinearProgress variant="determinate" value={progress} sx={{ height: 8, borderRadius: 4 }} />
        </Box>

        {/* Question */}
        {currentQuestion && (
          <motion.div
            key={currentQuestion.id}
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3 }}
          >
            <Card elevation={3} sx={{ mb: 3 }}>
              <CardContent sx={{ p: 4 }}>
                <Box display="flex" gap={1} mb={3}>
                  <Chip label={currentQuestion.topic} variant="outlined" />
                  <Chip 
                    label={`Difficulty: ${currentQuestion.difficulty}/5`} 
                    color={currentQuestion.difficulty > 3 ? 'error' : 'primary'}
                    variant="outlined"
                  />
                </Box>

                <Typography variant="h6" gutterBottom fontWeight="bold">
                  {currentQuestion.question_text}
                </Typography>

                {currentQuestion.question_type === 'mcq' && currentQuestion.options && (
                  <FormControl component="fieldset" sx={{ width: '100%' }}>
                    <RadioGroup
                      value={answers[currentQuestion.id] || ''}
                      onChange={(e) => handleAnswerChange(currentQuestion.id, e.target.value)}
                    >
                      {currentQuestion.options.map((option, index) => (
                        <FormControlLabel
                          key={index}
                          value={option.text}
                          control={<Radio />}
                          label={option.text}
                          sx={{
                            mb: 1,
                            p: 2,
                            border: '1px solid',
                            borderColor: 'divider',
                            borderRadius: 2,
                            '&:hover': {
                              bgcolor: 'action.hover',
                            },
                          }}
                        />
                      ))}
                    </RadioGroup>
                  </FormControl>
                )}
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Navigation */}
        <Box display="flex" justifyContent="between" alignItems="center">
          <Button
            variant="outlined"
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </Button>

          <Typography variant="body2" color="text.secondary">
            {Object.keys(answers).length} of {quiz.questions.length} answered
          </Typography>

          {currentQuestionIndex < quiz.questions.length - 1 ? (
            <Button
              variant="contained"
              onClick={handleNext}
            >
              Next
            </Button>
          ) : (
            <Button
              variant="contained"
              onClick={handleSubmit}
              disabled={!allAnswered || submitMutation.isLoading}
              color="success"
            >
              {submitMutation.isLoading ? 'Submitting...' : 'Submit Quiz'}
            </Button>
          )}
        </Box>

        {!allAnswered && currentQuestionIndex === quiz.questions.length - 1 && (
          <Alert severity="warning" sx={{ mt: 2 }}>
            Please answer all questions before submitting the quiz.
          </Alert>
        )}
      </motion.div>
    </Container>
  )
}

export default QuizPage