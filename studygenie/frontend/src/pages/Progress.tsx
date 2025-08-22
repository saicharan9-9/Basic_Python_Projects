import React from 'react'
import {
  Container,
  Paper,
  Typography,
  Box,
  Grid,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  Avatar,
} from '@mui/material'
import {
  TrendingUp,
  School,
  EmojiEvents,
  AccessTime,
  Analytics,
  Psychology,
} from '@mui/icons-material'
import { motion } from 'framer-motion'
import { useQuery } from 'react-query'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

import { progressAPI } from '../services/api'

const Progress: React.FC = () => {
  const { data: stats, isLoading: statsLoading } = useQuery(
    'dashboardStats',
    progressAPI.getDashboardStats
  )

  const { data: topicPerformance, isLoading: topicLoading } = useQuery(
    'topicPerformance',
    progressAPI.getTopicPerformance
  )

  const { data: learningCurve, isLoading: curveLoading } = useQuery(
    'learningCurve',
    progressAPI.getLearningCurve
  )

  const { data: heatmapData, isLoading: heatmapLoading } = useQuery(
    'studyHeatmap',
    progressAPI.getStudyHeatmap
  )

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

  const statCards = [
    {
      title: 'Study Streak',
      value: stats?.study_streak || 0,
      unit: 'days',
      icon: <EmojiEvents />,
      color: '#ff9800',
      description: 'Consecutive days studied',
    },
    {
      title: 'Total Study Time',
      value: Math.floor((stats?.total_study_time || 0) / 60),
      unit: 'hours',
      icon: <AccessTime />,
      color: '#2196f3',
      description: 'Total time spent studying',
    },
    {
      title: 'Topics Mastered',
      value: stats?.topics_mastered || 0,
      unit: 'topics',
      icon: <School />,
      color: '#4caf50',
      description: 'Subjects with >80% accuracy',
    },
    {
      title: 'Avg Quiz Score',
      value: stats?.average_quiz_score || 0,
      unit: '%',
      icon: <TrendingUp />,
      color: '#9c27b0',
      description: 'Average performance across all quizzes',
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
            📊 Learning Analytics
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Track your progress and identify areas for improvement
          </Typography>
        </Box>

        {/* Stats Overview */}
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
                      <Box>
                        <Typography variant="h6" component="div">
                          {stat.title}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {stat.description}
                        </Typography>
                      </Box>
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
          {/* Learning Curve */}
          <Grid item xs={12} md={8}>
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                📈 Learning Curve
              </Typography>
              {curveLoading ? (
                <LinearProgress />
              ) : learningCurve?.learning_curve?.length ? (
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={learningCurve.learning_curve}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="attempt_number" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip 
                      formatter={(value: any, name: string) => [`${value}%`, name === 'score' ? 'Quiz Score' : 'Average Score']}
                      labelFormatter={(label) => `Attempt ${label}`}
                    />
                    <Line
                      type="monotone"
                      dataKey="score"
                      stroke="#8884d8"
                      strokeWidth={2}
                      dot={{ fill: '#8884d8', strokeWidth: 2, r: 4 }}
                    />
                    <Line
                      type="monotone"
                      dataKey="average_score"
                      stroke="#82ca9d"
                      strokeWidth={3}
                      dot={{ fill: '#82ca9d', strokeWidth: 2, r: 6 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
                  No quiz data available yet. Take some quizzes to see your progress!
                </Typography>
              )}
            </Paper>

            {/* Topic Performance */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                📚 Topic Performance
              </Typography>
              {topicLoading ? (
                <LinearProgress />
              ) : topicPerformance?.topic_performance?.length ? (
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={topicPerformance.topic_performance}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="topic" 
                      angle={-45}
                      textAnchor="end"
                      height={100}
                    />
                    <YAxis domain={[0, 100]} />
                    <Tooltip formatter={(value: any) => [`${value}%`, 'Accuracy']} />
                    <Bar 
                      dataKey="accuracy" 
                      fill="#8884d8"
                      radius={[4, 4, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <Typography variant="body2" color="text.secondary" textAlign="center" py={4}>
                  No topic data available yet. Complete some quizzes to see topic breakdown!
                </Typography>
              )}
            </Paper>
          </Grid>

          {/* Sidebar */}
          <Grid item xs={12} md={4}>
            {/* Subject Strengths & Weaknesses */}
            <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                🎯 Focus Areas
              </Typography>
              
              {stats?.weak_subjects?.length ? (
                <Box mb={3}>
                  <Typography variant="subtitle2" color="error.main" gutterBottom>
                    Need Improvement:
                  </Typography>
                  <Box display="flex" flexDirection="column" gap={1}>
                    {stats.weak_subjects.map((subject) => (
                      <Chip
                        key={subject}
                        label={subject}
                        size="small"
                        color="error"
                        variant="outlined"
                        sx={{ alignSelf: 'flex-start' }}
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
                  <Box display="flex" flexDirection="column" gap={1}>
                    {stats.strong_subjects.map((subject) => (
                      <Chip
                        key={subject}
                        label={subject}
                        size="small"
                        color="success"
                        variant="outlined"
                        sx={{ alignSelf: 'flex-start' }}
                      />
                    ))}
                  </Box>
                </Box>
              ) : null}

              {!stats?.weak_subjects?.length && !stats?.strong_subjects?.length && (
                <Typography variant="body2" color="text.secondary" textAlign="center" py={2}>
                  Take more quizzes to see your subject analysis
                </Typography>
              )}
            </Paper>

            {/* Recent Activity */}
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom fontWeight="bold">
                📅 Recent Activity
              </Typography>
              {stats?.recent_activity?.length ? (
                <List dense>
                  {stats.recent_activity.slice(0, 8).map((activity, index) => (
                    <ListItem key={index} sx={{ px: 0 }}>
                      <ListItemText
                        primary={
                          <Typography variant="body2">
                            {activity.description}
                          </Typography>
                        }
                        secondary={
                          <Typography variant="caption" color="text.secondary">
                            {new Date(activity.timestamp).toLocaleDateString()}
                          </Typography>
                        }
                      />
                      {activity.score && (
                        <Chip
                          label={`${activity.score}%`}
                          size="small"
                          color={
                            activity.score > 80 ? 'success' : 
                            activity.score > 60 ? 'warning' : 'error'
                          }
                        />
                      )}
                    </ListItem>
                  ))}
                </List>
              ) : (
                <Typography variant="body2" color="text.secondary" textAlign="center" py={2}>
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

export default Progress