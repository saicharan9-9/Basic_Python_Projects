import React from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  FileText, 
  Brain, 
  TrendingUp, 
  Clock, 
  Target,
  Calendar,
  Award,
  Plus
} from 'lucide-react';
import { progressAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import { useAuth } from '../../contexts/AuthContext';

const Dashboard = () => {
  const { t } = useLanguage();
  const { user } = useAuth();
  
  const { data: dashboardStats, isLoading } = useQuery(
    'dashboardStats',
    progressAPI.getDashboard,
    {
      select: (response) => response.data
    }
  );

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  const stats = dashboardStats || {};

  const formatTime = (minutes) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  const quickActions = [
    {
      title: 'Upload Document',
      description: 'Add new study material',
      icon: FileText,
      href: '/documents',
      color: 'bg-blue-500'
    },
    {
      title: 'Study Flashcards',
      description: 'Review with spaced repetition',
      icon: Brain,
      href: '/study-materials?type=flashcard',
      color: 'bg-green-500'
    },
    {
      title: 'Take Quiz',
      description: 'Test your knowledge',
      icon: Target,
      href: '/study-materials?type=quiz',
      color: 'bg-purple-500'
    },
    {
      title: 'AI Tutor',
      description: 'Get help from AI',
      icon: BookOpen,
      href: '/ai-tutor',
      color: 'bg-orange-500'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Welcome Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">
          {t('welcomeBack')}, {user?.full_name || user?.username}! 👋
        </h1>
        <p className="mt-2 text-gray-600">
          Ready to continue your learning journey?
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Clock className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {t('totalStudyTime')}
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {formatTime(stats.total_study_time || 0)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Calendar className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {t('studyStreak')}
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.study_streak || 0} days
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Brain className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {t('flashcardsMastered')}
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.mastered_flashcards || 0}/{stats.total_flashcards || 0}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Award className="h-6 w-6 text-orange-600" />
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    {t('averageQuizScore')}
                  </dt>
                  <dd className="text-lg font-medium text-gray-900">
                    {stats.quiz_average ? `${stats.quiz_average.toFixed(1)}%` : '0%'}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Quick Actions
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {quickActions.map((action) => {
                  const Icon = action.icon;
                  return (
                    <Link
                      key={action.title}
                      to={action.href}
                      className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300 hover:shadow-md transition-all duration-200"
                    >
                      <div>
                        <span className={`rounded-lg inline-flex p-3 ${action.color} text-white`}>
                          <Icon className="h-6 w-6" />
                        </span>
                      </div>
                      <div className="mt-4">
                        <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600">
                          {action.title}
                        </h3>
                        <p className="mt-2 text-sm text-gray-500">
                          {action.description}
                        </p>
                      </div>
                      <span className="pointer-events-none absolute top-6 right-6 text-gray-300 group-hover:text-gray-400">
                        <Plus className="h-6 w-6" />
                      </span>
                    </Link>
                  );
                })}
              </div>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div>
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                {t('recentActivity')}
              </h3>
              {stats.recent_activity && stats.recent_activity.length > 0 ? (
                <div className="space-y-3">
                  {stats.recent_activity.map((activity, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className="flex-shrink-0">
                        {activity.type === 'quiz' && (
                          <Target className="h-5 w-5 text-purple-500" />
                        )}
                        {activity.type === 'flashcard' && (
                          <Brain className="h-5 w-5 text-green-500" />
                        )}
                        {activity.type === 'reading' && (
                          <BookOpen className="h-5 w-5 text-blue-500" />
                        )}
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900">
                          {activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} Session
                        </p>
                        <p className="text-sm text-gray-500">
                          {activity.subject} • {formatTime(activity.duration)}
                          {activity.accuracy && ` • ${activity.accuracy.toFixed(0)}% accuracy`}
                        </p>
                      </div>
                      <div className="flex-shrink-0 text-xs text-gray-400">
                        {new Date(activity.date).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-6">
                  <TrendingUp className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No activity yet</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Start studying to see your activity here.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Subject Progress */}
      {stats.subject_progress && Object.keys(stats.subject_progress).length > 0 && (
        <div className="mt-8">
          <div className="bg-white shadow rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
                Subject Progress
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {Object.entries(stats.subject_progress).map(([subject, progress]) => (
                  <div key={subject} className="border rounded-lg p-4">
                    <h4 className="font-medium text-gray-900 mb-2">{subject}</h4>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Study Time</span>
                        <span className="font-medium">{formatTime(progress.study_time || 0)}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Flashcard Mastery</span>
                        <span className="font-medium">{(progress.flashcard_mastery || 0).toFixed(0)}%</span>
                      </div>
                      {progress.quiz_scores && progress.quiz_scores.length > 0 && (
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Avg Quiz Score</span>
                          <span className="font-medium">
                            {(progress.quiz_scores.reduce((a, b) => a + b, 0) / progress.quiz_scores.length).toFixed(0)}%
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;