import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  FileText, 
  Brain, 
  TrendingUp, 
  Clock, 
  Target,
  Plus,
  Upload,
  Play,
  BarChart3
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface DashboardStats {
  totalMaterials: number;
  totalQuizzes: number;
  totalFlashcards: number;
  studyStreak: number;
  averageScore: number;
  totalStudyTime: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({
    totalMaterials: 0,
    totalQuizzes: 0,
    totalFlashcards: 0,
    studyStreak: 0,
    averageScore: 0,
    totalStudyTime: 0
  });

  // Mock data for demo - in real app, fetch from API
  useEffect(() => {
    setStats({
      totalMaterials: 12,
      totalQuizzes: 8,
      totalFlashcards: 45,
      studyStreak: 7,
      averageScore: 85.5,
      totalStudyTime: 320
    });
  }, []);

  const quickActions = [
    {
      title: 'Upload Study Material',
      description: 'Add new PDFs, notes, or documents',
      icon: Upload,
      href: '/materials',
      color: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50'
    },
    {
      title: 'Take a Quiz',
      description: 'Test your knowledge with AI-generated questions',
      icon: FileText,
      href: '/quizzes',
      color: 'from-green-500 to-green-600',
      bgColor: 'bg-green-50'
    },
    {
      title: 'Review Flashcards',
      description: 'Practice with spaced repetition',
      icon: Brain,
      href: '/flashcards',
      color: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50'
    },
    {
      title: 'Ask AI Tutor',
      description: 'Get help with difficult concepts',
      icon: Play,
      href: '/tutor',
      color: 'from-orange-500 to-orange-600',
      bgColor: 'bg-orange-50'
    }
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'quiz',
      title: 'Physics Chapter 3 Quiz',
      score: 92,
      time: '2 hours ago',
      icon: FileText,
      color: 'text-green-500'
    },
    {
      id: 2,
      type: 'material',
      title: 'Mathematics Notes Uploaded',
      time: '4 hours ago',
      icon: BookOpen,
      color: 'text-blue-500'
    },
    {
      id: 3,
      type: 'flashcard',
      title: '15 Flashcards Reviewed',
      time: '6 hours ago',
      icon: Brain,
      color: 'text-purple-500'
    },
    {
      id: 4,
      type: 'tutor',
      title: 'Asked AI Tutor about Quantum Physics',
      time: '1 day ago',
      icon: Play,
      color: 'text-orange-500'
    }
  ];

  return (
    <div className="space-y-6">
      {/* Welcome Header */}
      <div className="bg-gradient-to-r from-primary-500 to-accent-600 rounded-2xl p-8 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">
              Welcome back, {user?.full_name || user?.username}! 👋
            </h1>
            <p className="text-primary-100 text-lg">
              Ready to continue your learning journey? Let's make today productive!
            </p>
          </div>
          <div className="hidden md:block">
            <div className="text-right">
              <div className="text-4xl font-bold">{stats.studyStreak}</div>
              <div className="text-primary-100">Day Streak</div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Study Materials</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalMaterials}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-full">
              <BookOpen className="w-6 h-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Quizzes Taken</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalQuizzes}</p>
            </div>
            <div className="p-3 bg-green-100 rounded-full">
              <FileText className="w-6 h-6 text-green-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Flashcards</p>
              <p className="text-2xl font-bold text-gray-900">{stats.totalFlashcards}</p>
            </div>
            <div className="p-3 bg-purple-100 rounded-full">
              <Brain className="w-6 h-6 text-purple-600" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Average Score</p>
              <p className="text-2xl font-bold text-gray-900">{stats.averageScore}%</p>
            </div>
            <div className="p-3 bg-orange-100 rounded-full">
              <TrendingUp className="w-6 h-6 text-orange-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <Link
              key={index}
              to={action.href}
              className="card hover:shadow-lg transition-all duration-200 group"
            >
              <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${action.color} flex items-center justify-center mb-4`}>
                <action.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2 group-hover:text-primary-600 transition-colors">
                {action.title}
              </h3>
              <p className="text-sm text-gray-600">{action.description}</p>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity & Study Goals */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Activity */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Recent Activity</h2>
            <Link to="/progress" className="text-primary-600 hover:text-primary-700 text-sm font-medium">
              View All
            </Link>
          </div>
          <div className="space-y-4">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-50 transition-colors">
                <div className={`p-2 rounded-full bg-gray-100`}>
                  <activity.icon className={`w-4 h-4 ${activity.color}`} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {activity.title}
                  </p>
                  <p className="text-xs text-gray-500">{activity.time}</p>
                </div>
                {activity.score && (
                  <div className="text-sm font-semibold text-green-600">
                    {activity.score}%
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Study Goals */}
        <div className="card">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">Today's Goals</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-primary-50 to-primary-100 rounded-lg">
              <div className="flex items-center space-x-3">
                <Target className="w-5 h-5 text-primary-600" />
                <div>
                  <p className="font-medium text-gray-900">Study Time</p>
                  <p className="text-sm text-gray-600">Target: 60 minutes</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-primary-600">{stats.totalStudyTime}</p>
                <p className="text-sm text-gray-500">minutes</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-green-50 to-green-100 rounded-lg">
              <div className="flex items-center space-x-3">
                <FileText className="w-5 h-5 text-green-600" />
                <div>
                  <p className="font-medium text-gray-900">Quiz Goal</p>
                  <p className="text-sm text-gray-600">Complete 2 quizzes</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-green-600">1/2</p>
                <p className="text-sm text-gray-500">completed</p>
              </div>
            </div>

            <div className="flex items-center justify-between p-4 bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg">
              <div className="flex items-center space-x-3">
                <Brain className="w-5 h-5 text-purple-600" />
                <div>
                  <p className="font-medium text-gray-900">Flashcard Review</p>
                  <p className="text-sm text-gray-600">Review 20 cards</p>
                </div>
              </div>
              <div className="text-right">
                <p className="text-lg font-bold text-purple-600">15/20</p>
                <p className="text-sm text-gray-500">reviewed</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Study Tips */}
      <div className="card bg-gradient-to-r from-accent-50 to-primary-50 border-accent-200">
        <div className="flex items-start space-x-4">
          <div className="p-3 bg-accent-100 rounded-full">
            <Brain className="w-6 h-6 text-accent-600" />
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              💡 Study Tip of the Day
            </h3>
            <p className="text-gray-700 mb-3">
              "Use the Pomodoro Technique: Study for 25 minutes, then take a 5-minute break. 
              This helps maintain focus and prevents mental fatigue."
            </p>
            <div className="flex space-x-2">
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-accent-100 text-accent-800">
                Productivity
              </span>
              <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                Focus
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;