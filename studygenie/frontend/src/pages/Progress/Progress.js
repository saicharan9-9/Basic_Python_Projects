import React from 'react';
import { useQuery } from 'react-query';
import { 
  TrendingUp, 
  Clock, 
  Target, 
  Brain, 
  Calendar,
  Award,
  BarChart3
} from 'lucide-react';
import { progressAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';

const Progress = () => {
  const { t } = useLanguage();

  const { data: dashboardStats, isLoading } = useQuery(
    'dashboardStats',
    progressAPI.getDashboard,
    {
      select: (response) => response.data
    }
  );

  const formatTime = (minutes) => {
    if (minutes < 60) return `${minutes}m`;
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map((i) => (
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">{t('progress')}</h1>
        <p className="mt-2 text-gray-600">
          Track your learning journey and achievements
        </p>
      </div>

      {/* Overview Stats */}
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
                    Total Study Time
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
                    Study Streak
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
                    Flashcards Mastered
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
                    Average Quiz Score
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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Recent Activity
            </h3>
            {stats.recent_activity && stats.recent_activity.length > 0 ? (
              <div className="space-y-4">
                {stats.recent_activity.map((activity, index) => (
                  <div key={index} className="flex items-center space-x-4 p-4 bg-gray-50 rounded-lg">
                    <div className="flex-shrink-0">
                      {activity.type === 'quiz' && (
                        <Target className="h-8 w-8 text-purple-500" />
                      )}
                      {activity.type === 'flashcard' && (
                        <Brain className="h-8 w-8 text-green-500" />
                      )}
                      {activity.type === 'reading' && (
                        <Clock className="h-8 w-8 text-blue-500" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900">
                        {activity.type.charAt(0).toUpperCase() + activity.type.slice(1)} Session
                      </p>
                      <p className="text-sm text-gray-500">
                        {activity.subject} • {formatTime(activity.duration)}
                      </p>
                      {activity.accuracy && (
                        <p className="text-sm text-gray-500">
                          Accuracy: {activity.accuracy.toFixed(0)}%
                        </p>
                      )}
                    </div>
                    <div className="flex-shrink-0 text-xs text-gray-400">
                      {new Date(activity.date).toLocaleDateString()}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <BarChart3 className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No activity yet</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Start studying to see your activity here.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Subject Progress */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
              Subject Progress
            </h3>
            {stats.subject_progress && Object.keys(stats.subject_progress).length > 0 ? (
              <div className="space-y-6">
                {Object.entries(stats.subject_progress).map(([subject, progress]) => (
                  <div key={subject}>
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="font-medium text-gray-900">{subject}</h4>
                      <span className="text-sm text-gray-500">
                        {formatTime(progress.study_time || 0)}
                      </span>
                    </div>
                    
                    <div className="space-y-3">
                      {/* Flashcard Mastery */}
                      <div>
                        <div className="flex justify-between text-sm text-gray-600 mb-1">
                          <span>Flashcard Mastery</span>
                          <span>{(progress.flashcard_mastery || 0).toFixed(0)}%</span>
                        </div>
                        <div className="bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-green-500 rounded-full h-2"
                            style={{ width: `${progress.flashcard_mastery || 0}%` }}
                          />
                        </div>
                      </div>

                      {/* Quiz Performance */}
                      {progress.quiz_scores && progress.quiz_scores.length > 0 && (
                        <div>
                          <div className="flex justify-between text-sm text-gray-600 mb-1">
                            <span>Quiz Performance</span>
                            <span>
                              {(progress.quiz_scores.reduce((a, b) => a + b, 0) / progress.quiz_scores.length).toFixed(0)}%
                            </span>
                          </div>
                          <div className="bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-purple-500 rounded-full h-2"
                              style={{ 
                                width: `${progress.quiz_scores.reduce((a, b) => a + b, 0) / progress.quiz_scores.length}%` 
                              }}
                            />
                          </div>
                        </div>
                      )}

                      {/* Weak Topics */}
                      {progress.weak_topics && progress.weak_topics.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-red-600 mb-1">
                            Areas for Improvement:
                          </p>
                          <div className="flex flex-wrap gap-1">
                            {progress.weak_topics.slice(0, 3).map((topic, index) => (
                              <span
                                key={index}
                                className="inline-block px-2 py-1 text-xs bg-red-100 text-red-800 rounded"
                              >
                                {topic.length > 30 ? `${topic.substring(0, 30)}...` : topic}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Strong Topics */}
                      {progress.strong_topics && progress.strong_topics.length > 0 && (
                        <div>
                          <p className="text-sm font-medium text-green-600 mb-1">
                            Strengths:
                          </p>
                          <div className="flex flex-wrap gap-1">
                            {progress.strong_topics.slice(0, 3).map((topic, index) => (
                              <span
                                key={index}
                                className="inline-block px-2 py-1 text-xs bg-green-100 text-green-800 rounded"
                              >
                                {topic.length > 30 ? `${topic.substring(0, 30)}...` : topic}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <TrendingUp className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No subject data</h3>
                <p className="mt-1 text-sm text-gray-500">
                  Complete quizzes and flashcards to see subject progress.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Study Streak Visualization */}
      <div className="mt-8 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 mb-4">
            Study Consistency
          </h3>
          <div className="text-center py-8">
            <div className="inline-flex items-center justify-center w-24 h-24 bg-primary-100 rounded-full mb-4">
              <Calendar className="h-12 w-12 text-primary-600" />
            </div>
            <h4 className="text-2xl font-bold text-gray-900 mb-2">
              {stats.study_streak || 0} Day Streak
            </h4>
            <p className="text-gray-600">
              {stats.study_streak > 0 
                ? "Great job! Keep up the momentum!" 
                : "Start your study streak today!"
              }
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Progress;