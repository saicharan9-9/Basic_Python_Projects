import React from 'react'
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CardActions,
  Button,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
} from '@mui/material'
import {
  Upload,
  Quiz,
  Psychology,
  TrendingUp,
  AccessTime,
  EmojiEvents,
  School,
  Analytics,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useQuery } from 'react-query'
import { useNavigate } from 'react-router-dom'
import { format } from 'date-fns'

import { progressAPI, uploadAPI, studyAPI } from '../services/api'
import { useAuth } from '../hooks/useAuth'

const Dashboard: React.FC = () => {
  const { user } = useAuth()
  const navigate = useNavigate()

  const { data: stats, isLoading: statsLoading } = useQuery(
    'dashboardStats',
    progressAPI.getDashboardStats
  )

  const { data: documents, isLoading: documentsLoading } = useQuery(
    'userDocuments',
    uploadAPI.getUserDocuments
  )

  const { data: dueFlashcards, isLoading: flashcardsLoading } = useQuery(
    'dueFlashcards',
    studyAPI.getDueFlashcards
  )

  const statCards = [
    {
      title: 'Study Streak',
      value: stats?.study_streak || 0,
      unit: 'days',
      icon: <EmojiEvents />,
      color: '#ff9800',
    },
    {
      title: 'Total Study Time',
      value: Math.floor((stats?.total_study_time || 0) / 60),
      unit: 'hours',
      icon: <AccessTime />,
      color: '#2196f3',
    },
    {
      title: 'Topics Mastered',
      value: stats?.topics_mastered || 0,
      unit: 'topics',
      icon: <School />,
      color: '#4caf50',
    },
    {
      title: 'Avg Quiz Score',
      value: stats?.average_quiz_score || 0,
      unit: '%',
      icon: <TrendingUp />,
      color: '#9c27b0',
    },
  ]

  const quickActions = [
    {
      title: 'Upload New Material',
      description: 'Add PDFs, images, or notes',
      icon: <Upload />,
      action: () => navigate('/upload'),
      color: '#1976d2',
    },
    {
      title: 'Review Flashcards',
      description: `${dueFlashcards?.length || 0} cards due`,
      icon: <Psychology />,
      action: () => navigate('/flashcards'),
      color: '#dc004e',
      disabled: !dueFlashcards?.length,
    },
    {
      title: 'View Progress',
      description: 'See your learning analytics',
      icon: <Analytics />,
      action: () => navigate('/progress'),
      color: '#388e3c',
    },
  ]

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Box mb={4}>
          <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
            Welcome back, {user?.full_name?.split(' ')[0]}! 👋
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Ready to continue your learning journey?
          </Typography>
        </Box>

        {/* Stats Cards */}
        <Grid container spacing={3} mb={4}>
          {statCards.map((stat, index) => (
            <Grid item xs={12} sm={6} md={3} key={stat.title}>
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                <Card elevation={3} sx={{ height: '100%' }}>
                  <CardContent>
                    <Box display="flex" alignItems="center" mb={2}>
                      <Avatar sx={{ bgcolor: stat.color, mr: 2 }}>
                        {stat.icon}
                      </Avatar>
                      <Typography variant="h6" component="div">
                        {stat.title}
                      </Typography>
                    </Box>
                    <Typography variant="h3" component="div" fontWeight="bold">
                      {stat.value}
                      <Typography variant="h6" component="span" color="text.secondary" ml={1}>
                        {stat.unit}
                      </Typography>
                    </Typography>
                  </CardContent>
                </Card>
              </motion.div>
            </Grid>
          ))}
        </Grid>

        <Grid container spacing={3}>
          {/* Quick Actions */}
          <Grid item xs={12} md={8}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Quick Actions
              </Typography>
              <Grid container spacing={2}>
                {quickActions.map((action, index) => (
                  <Grid item xs={12} sm={4} key={action.title}>
                    <motion.div
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                    >
                      <Card
                        elevation={2}
                        sx={{
                          cursor: action.disabled ? 'not-allowed' : 'pointer',
                          opacity: action.disabled ? 0.6 : 1,
                        }}
                        onClick={action.disabled ? undefined : action.action}
                      >
                        <CardContent sx={{ textAlign: 'center', py: 3 }}>
                          <Avatar
                            sx={{
                              bgcolor: action.color,
                              mx: 'auto',
                              mb: 2,
                              width: 56,
                              height: 56,
                            }}
                          >
                            {action.icon}
                          </Avatar>
                          <Typography variant="h6" gutterBottom>
                            {action.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {action.description}
                          </Typography>
                        </CardContent>
                      </Card>
                    </motion.div>
                  </Grid>
                ))}
              </Grid>
            </Paper>

            {/* Recent Documents */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Recent Documents
              </Typography>
              {documentsLoading ? (
                <LinearProgress />
              ) : documents?.length ? (
                <List>
                  {documents.slice(0, 5).map((doc, index) => (
                    <ListItem
                      key={doc.id}
                      sx={{
                        border: '1px solid',
                        borderColor: 'divider',
                        borderRadius: 2,
                        mb: 1,
                        cursor: 'pointer',
                        '&:hover': { bgcolor: 'action.hover' },
                      }}
                      onClick={() => navigate(`/study/${doc.id}`)}
                    >
                      <ListItemIcon>
                        <Avatar sx={{ bgcolor: 'primary.main' }}>
                          {doc.filename.charAt(0).toUpperCase()}
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText
                        primary={doc.filename}
                        secondary={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Chip
                              label={doc.document_type.toUpperCase()}
                              size="small"
                              variant="outlined"
                            />
                            <Typography variant="caption">
                              {format(new Date(doc.created_at), 'MMM d, yyyy')}
                            </Typography>
                            {doc.has_study_material && (
                              <Chip label="Study Material Ready" size="small" color="success" />
                            )}
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Box textAlign="center" py={4}>
                  <Typography variant="body1" color="text.secondary" mb={2}>
                    No documents uploaded yet
                  </Typography>
                  <Button
                    variant="contained"
                    startIcon={<Upload />}
                    onClick={() => navigate('/upload')}
                  >
                    Upload Your First Document
                  </Button>
                </Box>
              )}
            </Paper>
          </Grid>

          {/* Sidebar */}
          <Grid item xs={12} md={4}>
            {/* Performance Overview */}
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Performance Overview
              </Typography>
              
              {stats?.weak_subjects?.length ? (
                <Box mb={2}>
                  <Typography variant="subtitle2" color="error.main" gutterBottom>
                    Areas to Focus On:
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {stats.weak_subjects.slice(0, 3).map((subject) => (
                      <Chip
                        key={subject}
                        label={subject}
                        size="small"
                        color="error"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </Box>
              ) : null}

              {stats?.strong_subjects?.length ? (
                <Box>
                  <Typography variant="subtitle2" color="success.main" gutterBottom>
                    Strong Areas:
                  </Typography>
                  <Box display="flex" flexWrap="wrap" gap={1}>
                    {stats.strong_subjects.slice(0, 3).map((subject) => (
                      <Chip
                        key={subject}
                        label={subject}
                        size="small"
                        color="success"
                        variant="outlined"
                      />
                    ))}
                  </Box>
                </Box>
              ) : null}
            </Paper>

            {/* Recent Activity */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                Recent Activity
              </Typography>
              {stats?.recent_activity?.length ? (
                <List dense>
                  {stats.recent_activity.slice(0, 5).map((activity, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemText
                        primary={activity.description}
                        secondary={format(new Date(activity.timestamp), 'MMM d, h:mm a')}
                        primaryTypographyProps={{ variant: 'body2' }}
                        secondaryTypographyProps={{ variant: 'caption' }}
                      />
                      {activity.score && (
                        <Chip
                          label={`${activity.score}%`}
                          size="small"
                          color={activity.score > 80 ? 'success' : activity.score > 60 ? 'warning' : 'error'}
                        />
                      )}
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No recent activity
                </Typography>
              )}
            </Paper>
          </Grid>
        </Grid>
      </motion.div>
    </Container>
  )
}

export default Dashboard