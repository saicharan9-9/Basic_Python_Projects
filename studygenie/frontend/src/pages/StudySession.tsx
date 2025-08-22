import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  TextField,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Avatar,
  Divider,
} from '@mui/material'
import {
  Psychology,
  Quiz,
  SmartToy,
  Send,
  MenuBook,
  AutoAwesome,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation } from 'react-query'
import ReactMarkdown from 'react-markdown'

import { uploadAPI, studyAPI } from '../services/api'
import { TutorResponse } from '../types'

const StudySession: React.FC = () => {
  const { documentId } = useParams<{ documentId: string }>()
  const navigate = useNavigate()
  const [tutorQuestion, setTutorQuestion] = useState('')
  const [tutorResponse, setTutorResponse] = useState<TutorResponse | null>(null)
  const [showTutor, setShowTutor] = useState(false)

  const { data: documents } = useQuery('userDocuments', uploadAPI.getUserDocuments)
  const document = documents?.find(doc => doc.id === documentId)

  const { data: studyMaterial, isLoading } = useQuery(
    ['studyMaterial', documentId],
    () => uploadAPI.generateStudyMaterial(documentId!),
    {
      enabled: !!documentId && !!document?.has_study_material,
    }
  )

  const tutorMutation = useMutation(
    (question: string) => studyAPI.askTutor(question, documentId),
    {
      onSuccess: (response) => {
        setTutorResponse(response)
      },
      onError: (error: any) => {
        console.error('Tutor question failed:', error)
      },
    }
  )

  const handleTutorSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (tutorQuestion.trim()) {
      tutorMutation.mutate(tutorQuestion.trim())
    }
  }

  if (!document) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <Typography variant="h5">Document not found</Typography>
        <Button variant="contained" onClick={() => navigate('/dashboard')} sx={{ mt: 2 }}>
          Back to Dashboard
        </Button>
      </Container>
    )
  }

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box mb={4}>
          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            📚 {document.filename}
          </Typography>
          <Box display="flex" gap={1}>
            <Chip label={document.document_type.toUpperCase()} variant="outlined" />
            {document.page_count && (
              <Chip label={`${document.page_count} pages`} variant="outlined" />
            )}
          </Box>
        </Box>

        {!document.has_study_material ? (
          <Paper elevation={3} sx={{ p: 4, textAlign: 'center' }}>
            <AutoAwesome sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              Study material not generated yet
            </Typography>
            <Typography variant="body2" color="text.secondary" mb={3}>
              Generate flashcards and quizzes from this document to start studying
            </Typography>
            <Button
              variant="contained"
              onClick={() => navigate('/upload')}
              startIcon={<AutoAwesome />}
            >
              Generate Study Material
            </Button>
          </Paper>
        ) : (
          <Grid container spacing={3}>
            {/* Main Content */}
            <Grid item xs={12} md={8}>
              {/* Summary */}
              <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                <Typography variant="h6" gutterBottom fontWeight="bold">
                  📝 Summary
                </Typography>
                {studyMaterial?.summary ? (
                  <ReactMarkdown>{studyMaterial.summary}</ReactMarkdown>
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    Loading summary...
                  </Typography>
                )}
              </Paper>

              {/* Key Topics */}
              {studyMaterial?.key_topics && (
                <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
                  <Typography variant="h6" gutterBottom fontWeight="bold">
                    🏷️ Key Topics
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {studyMaterial.key_topics.map((topic) => (
                      <Chip key={topic} label={topic} variant="outlined" />
                    ))}
                  </Box>
                </Paper>
              )}

              {/* Study Actions */}
              <Paper elevation={3} sx={{ p: 3 }}>
                <Typography variant="h6" gutterBottom fontWeight="bold">
                  🎯 Study Options
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <Card elevation={2} sx={{ cursor: 'pointer' }} onClick={() => navigate('/flashcards')}>
                      <CardContent sx={{ textAlign: 'center', py: 3 }}>
                        <Psychology sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                        <Typography variant="h6" gutterBottom>
                          Review Flashcards
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {studyMaterial?.flashcards?.length || 0} cards available
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  
                  <Grid item xs={12} sm={6}>
                    <Card 
                      elevation={2} 
                      sx={{ cursor: 'pointer' }} 
                      onClick={() => navigate(`/quiz/${studyMaterial?.quiz?.id}`)}
                    >
                      <CardContent sx={{ textAlign: 'center', py: 3 }}>
                        <Quiz sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                        <Typography variant="h6" gutterBottom>
                          Take Quiz
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {studyMaterial?.quiz?.total_questions || 0} questions
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>
              </Paper>
            </Grid>

            {/* AI Tutor Sidebar */}
            <Grid item xs={12} md={4}>
              <Paper elevation={3} sx={{ p: 3, position: 'sticky', top: 20 }}>
                <Box display="flex" alignItems="center" gap={1} mb={3}>
                  <Avatar sx={{ bgcolor: 'secondary.main' }}>
                    <SmartToy />
                  </Avatar>
                  <Typography variant="h6" fontWeight="bold">
                    AI Tutor
                  </Typography>
                </Box>

                <Typography variant="body2" color="text.secondary" mb={3}>
                  Ask questions about this document and get instant answers!
                </Typography>

                <form onSubmit={handleTutorSubmit}>
                  <TextField
                    fullWidth
                    multiline
                    rows={3}
                    placeholder="Ask a question about this material..."
                    value={tutorQuestion}
                    onChange={(e) => setTutorQuestion(e.target.value)}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    startIcon={<Send />}
                    disabled={!tutorQuestion.trim() || tutorMutation.isLoading}
                  >
                    {tutorMutation.isLoading ? 'Thinking...' : 'Ask Tutor'}
                  </Button>
                </form>

                {tutorResponse && (
                  <Box mt={3}>
                    <Divider sx={{ mb: 2 }} />
                    <Typography variant="subtitle2" gutterBottom>
                      AI Tutor Response:
                    </Typography>
                    <Paper elevation={1} sx={{ p: 2, bgcolor: 'grey.50' }}>
                      <ReactMarkdown>{tutorResponse.answer}</ReactMarkdown>
                      <Box display="flex" justifyContent="between" alignItems="center" mt={2}>
                        <Typography variant="caption" color="text.secondary">
                          Confidence: {(tutorResponse.confidence * 100).toFixed(0)}%
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Sources: {tutorResponse.sources.length}
                        </Typography>
                      </Box>
                    </Paper>
                  </Box>
                )}
              </Paper>
            </Grid>
          </Grid>
        )}
      </motion.div>
    </Container>
  )
}

export default StudySession