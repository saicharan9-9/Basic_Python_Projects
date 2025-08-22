import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  LinearProgress,
  Alert,
  Stepper,
  Step,
  StepLabel,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material'
import {
  CloudUpload,
  Description,
  Quiz,
  Psychology,
  CheckCircle,
  AutoAwesome,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { useMutation, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'
import { useNavigate } from 'react-router-dom'

import { uploadAPI } from '../services/api'
import { StudyMaterial } from '../types'

const Upload: React.FC = () => {
  const [uploadedFile, setUploadedFile] = useState<any>(null)
  const [studyMaterial, setStudyMaterial] = useState<StudyMaterial | null>(null)
  const [activeStep, setActiveStep] = useState(0)
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const uploadMutation = useMutation(uploadAPI.uploadDocument, {
    onSuccess: (data) => {
      setUploadedFile(data)
      setActiveStep(1)
      toast.success('File uploaded successfully!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Upload failed')
    },
  })

  const generateMutation = useMutation(uploadAPI.generateStudyMaterial, {
    onSuccess: (data) => {
      setStudyMaterial(data)
      setActiveStep(2)
      queryClient.invalidateQueries('userDocuments')
      toast.success('Study material generated!')
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Generation failed')
    },
  })

  const onDrop = (acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      uploadMutation.mutate(acceptedFiles[0])
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png', '.tiff', '.bmp'],
      'text/plain': ['.txt'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  })

  const handleGenerateStudyMaterial = () => {
    if (uploadedFile) {
      generateMutation.mutate(uploadedFile.document_id)
    }
  }

  const steps = ['Upload Document', 'Generate Study Material', 'Ready to Study']

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box textAlign="center" mb={4}>
          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            Upload Study Material
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Upload PDFs, images, or text files to generate personalized study content
          </Typography>
        </Box>

        <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {activeStep === 0 && (
          <Paper
            elevation={3}
            sx={{
              p: 4,
              borderRadius: 3,
              border: isDragActive ? '2px dashed #1976d2' : '2px dashed #ccc',
              backgroundColor: isDragActive ? 'rgba(25, 118, 210, 0.04)' : 'background.paper',
              transition: 'all 0.3s ease',
            }}
          >
            <Box
              {...getRootProps()}
              sx={{
                textAlign: 'center',
                cursor: 'pointer',
                py: 6,
              }}
            >
              <input {...getInputProps()} />
              <motion.div
                animate={{ scale: isDragActive ? 1.1 : 1 }}
                transition={{ duration: 0.2 }}
              >
                <CloudUpload sx={{ fontSize: 80, color: 'primary.main', mb: 2 }} />
              </motion.div>
              
              <Typography variant="h5" gutterBottom fontWeight="bold">
                {isDragActive ? 'Drop your file here' : 'Drag & drop your file here'}
              </Typography>
              
              <Typography variant="body1" color="text.secondary" mb={3}>
                or click to browse files
              </Typography>
              
              <Button
                variant="contained"
                size="large"
                startIcon={<CloudUpload />}
                sx={{ mb: 3 }}
              >
                Choose File
              </Button>
              
              <Box>
                <Typography variant="body2" color="text.secondary">
                  Supported formats: PDF, JPG, PNG, TXT (max 10MB)
                </Typography>
              </Box>
            </Box>

            {uploadMutation.isLoading && (
              <Box mt={3}>
                <LinearProgress />
                <Typography variant="body2" textAlign="center" mt={1}>
                  Uploading and extracting text...
                </Typography>
              </Box>
            )}
          </Paper>
        )}

        {activeStep === 1 && uploadedFile && (
          <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
            <Box textAlign="center" mb={3}>
              <CheckCircle sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom fontWeight="bold">
                File Uploaded Successfully!
              </Typography>
              <Typography variant="body1" color="text.secondary">
                {uploadedFile.filename}
              </Typography>
            </Box>

            <Alert severity="info" sx={{ mb: 3 }}>
              <Typography variant="body2">
                Text extracted: {uploadedFile.extracted_text.substring(0, 150)}...
              </Typography>
            </Alert>

            <Box textAlign="center">
              <Button
                variant="contained"
                size="large"
                startIcon={<AutoAwesome />}
                onClick={handleGenerateStudyMaterial}
                disabled={generateMutation.isLoading}
                sx={{ mb: 2 }}
              >
                {generateMutation.isLoading ? 'Generating...' : 'Generate Study Material'}
              </Button>
              
              {generateMutation.isLoading && (
                <Box>
                  <LinearProgress sx={{ mb: 2 }} />
                  <Typography variant="body2" color="text.secondary">
                    AI is creating flashcards and quizzes for you...
                  </Typography>
                </Box>
              )}
            </Box>
          </Paper>
        )}

        {activeStep === 2 && studyMaterial && (
          <Paper elevation={3} sx={{ p: 4, borderRadius: 3 }}>
            <Box textAlign="center" mb={3}>
              <CheckCircle sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" gutterBottom fontWeight="bold">
                Study Material Ready!
              </Typography>
            </Box>

            <Card elevation={2} sx={{ mb: 3 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  📝 Summary
                </Typography>
                <Typography variant="body2" paragraph>
                  {studyMaterial.summary.substring(0, 200)}...
                </Typography>
                
                <Typography variant="h6" gutterBottom>
                  🏷️ Key Topics
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1} mb={2}>
                  {studyMaterial.key_topics.map((topic) => (
                    <Chip key={topic} label={topic} variant="outlined" />
                  ))}
                </Box>
              </CardContent>
            </Card>

            <Box display="flex" gap={2} mb={3}>
              <Card elevation={2} sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Psychology sx={{ fontSize: 40, color: 'primary.main', mb: 1 }} />
                  <Typography variant="h6" gutterBottom>
                    {studyMaterial.flashcards.length} Flashcards
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Ready for spaced repetition
                  </Typography>
                </CardContent>
              </Card>

              <Card elevation={2} sx={{ flex: 1 }}>
                <CardContent sx={{ textAlign: 'center' }}>
                  <Quiz sx={{ fontSize: 40, color: 'secondary.main', mb: 1 }} />
                  <Typography variant="h6" gutterBottom>
                    {studyMaterial.quiz.total_questions} Quiz Questions
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Test your knowledge
                  </Typography>
                </CardContent>
              </Card>
            </Box>

            <Box display="flex" gap={2} justifyContent="center">
              <Button
                variant="contained"
                startIcon={<Psychology />}
                onClick={() => navigate('/flashcards')}
              >
                Start Flashcards
              </Button>
              <Button
                variant="outlined"
                startIcon={<Quiz />}
                onClick={() => navigate(`/quiz/${studyMaterial.quiz.id}`)}
              >
                Take Quiz
              </Button>
            </Box>
          </Paper>
        )}
      </motion.div>
    </Container>
  )
}

export default Upload