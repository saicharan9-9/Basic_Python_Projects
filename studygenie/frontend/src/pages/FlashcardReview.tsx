import React, { useState } from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material'
import {
  Psychology,
  Flip,
  ThumbUp,
  ThumbDown,
  Help,
  CheckCircle,
  Schedule,
} from '@mui/icons-material'
import { motion, AnimatePresence } from 'framer-motion'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import toast from 'react-hot-toast'

import { studyAPI } from '../services/api'
import { Flashcard } from '../types'

const FlashcardReview: React.FC = () => {
  const [currentCardIndex, setCurrentCardIndex] = useState(0)
  const [isFlipped, setIsFlipped] = useState(false)
  const [showInstructions, setShowInstructions] = useState(false)
  const [sessionComplete, setSessionComplete] = useState(false)
  const queryClient = useQueryClient()

  const { data: flashcards, isLoading } = useQuery('dueFlashcards', studyAPI.getDueFlashcards)

  const reviewMutation = useMutation(
    ({ flashcardId, quality }: { flashcardId: string; quality: number }) =>
      studyAPI.reviewFlashcard(flashcardId, quality),
    {
      onSuccess: () => {
        handleNextCard()
        queryClient.invalidateQueries('dueFlashcards')
      },
      onError: (error: any) => {
        toast.error(error.response?.data?.detail || 'Review failed')
      },
    }
  )

  const currentCard = flashcards?.[currentCardIndex]
  const progress = flashcards ? ((currentCardIndex + 1) / flashcards.length) * 100 : 0

  const handleReview = (quality: number) => {
    if (currentCard) {
      reviewMutation.mutate({ flashcardId: currentCard.id, quality })
    }
  }

  const handleNextCard = () => {
    setIsFlipped(false)
    if (flashcards && currentCardIndex < flashcards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1)
    } else {
      setSessionComplete(true)
    }
  }

  const qualityButtons = [
    { quality: 0, label: 'Complete Blackout', color: '#f44336', description: "Couldn't remember at all" },
    { quality: 1, label: 'Incorrect', color: '#ff5722', description: 'Wrong answer, but remembered when shown' },
    { quality: 2, label: 'Hard', color: '#ff9800', description: 'Wrong answer, but seemed easy to recall' },
    { quality: 3, label: 'Good', color: '#ffc107', description: 'Correct with serious difficulty' },
    { quality: 4, label: 'Easy', color: '#8bc34a', description: 'Correct after hesitation' },
    { quality: 5, label: 'Perfect', color: '#4caf50', description: 'Perfect response' },
  ]

  if (isLoading) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <LinearProgress />
        <Typography mt={2}>Loading flashcards...</Typography>
      </Container>
    )
  }

  if (!flashcards?.length) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <Paper elevation={3} sx={{ p: 6, borderRadius: 3 }}>
          <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
          <Typography variant="h5" gutterBottom fontWeight="bold">
            No Cards Due for Review!
          </Typography>
          <Typography variant="body1" color="text.secondary" mb={3}>
            Great job! You're all caught up with your flashcard reviews.
          </Typography>
          <Button variant="contained" onClick={() => window.location.href = '/dashboard'}>
            Back to Dashboard
          </Button>
        </Paper>
      </Container>
    )
  }

  if (sessionComplete) {
    return (
      <Container maxWidth="md" sx={{ py: 4, textAlign: 'center' }}>
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <Paper elevation={3} sx={{ p: 6, borderRadius: 3 }}>
            <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom fontWeight="bold">
              Session Complete! 🎉
            </Typography>
            <Typography variant="body1" color="text.secondary" mb={3}>
              You've reviewed {flashcards.length} flashcards. Great work!
            </Typography>
            <Box display="flex" gap={2} justifyContent="center">
              <Button variant="contained" onClick={() => window.location.href = '/dashboard'}>
                Back to Dashboard
              </Button>
              <Button variant="outlined" onClick={() => window.location.reload()}>
                Review More Cards
              </Button>
            </Box>
          </Paper>
        </motion.div>
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
              Flashcard Review
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Card {currentCardIndex + 1} of {flashcards.length}
            </Typography>
          </Box>
          <IconButton onClick={() => setShowInstructions(true)}>
            <Help />
          </IconButton>
        </Box>

        {/* Progress */}
        <Box mb={3}>
          <LinearProgress variant="determinate" value={progress} sx={{ height: 8, borderRadius: 4 }} />
        </Box>

        {/* Flashcard */}
        <motion.div
          key={currentCard?.id}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.3 }}
        >
          <Card
            elevation={8}
            sx={{
              minHeight: 300,
              mb: 3,
              cursor: 'pointer',
              perspective: '1000px',
            }}
            onClick={() => setIsFlipped(!isFlipped)}
          >
            <CardContent
              sx={{
                height: 300,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                textAlign: 'center',
                position: 'relative',
                background: isFlipped 
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                color: 'white',
                transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
                transition: 'transform 0.6s',
                transformStyle: 'preserve-3d',
              }}
            >
              <Box
                sx={{
                  transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
                  backfaceVisibility: 'hidden',
                }}
              >
                <Typography variant="h6" gutterBottom>
                  {isFlipped ? 'Answer' : 'Question'}
                </Typography>
                <Typography variant="h5" component="div" fontWeight="bold" mb={2}>
                  {isFlipped ? currentCard?.back : currentCard?.front}
                </Typography>
                
                <Box display="flex" gap={1} justifyContent="center" mt={3}>
                  <Chip
                    label={currentCard?.topic}
                    size="small"
                    sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                  />
                  <Chip
                    label={`Difficulty: ${currentCard?.difficulty}/5`}
                    size="small"
                    sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                  />
                </Box>
              </Box>

              {!isFlipped && (
                <Box
                  sx={{
                    position: 'absolute',
                    bottom: 16,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 1,
                  }}
                >
                  <Flip sx={{ fontSize: 20 }} />
                  <Typography variant="caption">Click to flip</Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Review Buttons */}
        <AnimatePresence>
          {isFlipped && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.3 }}
            >
              <Paper elevation={3} sx={{ p: 3, borderRadius: 3 }}>
                <Typography variant="h6" gutterBottom textAlign="center">
                  How well did you know this?
                </Typography>
                <Box display="flex" flexWrap="wrap" gap={1} justifyContent="center">
                  {qualityButtons.map((btn) => (
                    <Button
                      key={btn.quality}
                      variant="outlined"
                      size="small"
                      onClick={() => handleReview(btn.quality)}
                      disabled={reviewMutation.isLoading}
                      sx={{
                        borderColor: btn.color,
                        color: btn.color,
                        '&:hover': {
                          bgcolor: btn.color,
                          color: 'white',
                        },
                      }}
                      title={btn.description}
                    >
                      {btn.label}
                    </Button>
                  ))}
                </Box>
                <Typography variant="caption" display="block" textAlign="center" mt={2} color="text.secondary">
                  Hover over buttons for descriptions
                </Typography>
              </Paper>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Instructions Dialog */}
        <Dialog open={showInstructions} onClose={() => setShowInstructions(false)} maxWidth="sm" fullWidth>
          <DialogTitle>How to Review Flashcards</DialogTitle>
          <DialogContent>
            <Typography variant="body2" paragraph>
              1. <strong>Read the question</strong> on the front of the card
            </Typography>
            <Typography variant="body2" paragraph>
              2. <strong>Think of your answer</strong> before flipping
            </Typography>
            <Typography variant="body2" paragraph>
              3. <strong>Click the card</strong> to see the answer
            </Typography>
            <Typography variant="body2" paragraph>
              4. <strong>Rate your performance</strong> honestly:
            </Typography>
            <Box ml={2}>
              {qualityButtons.map((btn) => (
                <Typography key={btn.quality} variant="caption" display="block" color="text.secondary">
                  <strong>{btn.label}:</strong> {btn.description}
                </Typography>
              ))}
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setShowInstructions(false)}>Got it!</Button>
          </DialogActions>
        </Dialog>
      </motion.div>
    </Container>
  )
}

export default FlashcardReview