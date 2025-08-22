import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  BookOpen, 
  FileText, 
  Brain, 
  MessageSquare, 
  BarChart3,
  Plus,
  Upload,
  Settings
} from 'lucide-react';

const Sidebar: React.FC = () => {
  const location = useLocation();

  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Study Materials', href: '/materials', icon: BookOpen },
    { name: 'Quizzes', href: '/quizzes', icon: FileText },
    { name: 'Flashcards', href: '/flashcards', icon: Brain },
    { name: 'AI Tutor', href: '/tutor', icon: MessageSquare },
    { name: 'Progress', href: '/progress', icon: BarChart3 },
  ];

  const quickActions = [
    { name: 'Upload PDF', href: '/materials', icon: Upload, action: 'upload' },
    { name: 'Create Quiz', href: '/quizzes', icon: Plus, action: 'create' },
    { name: 'Study Session', href: '/progress', icon: Brain, action: 'session' },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="w-64 bg-white shadow-sm border-r border-gray-200 min-h-screen p-4">
      {/* Quick Actions Section */}
      <div className="mb-8">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Quick Actions
        </h3>
        <div className="space-y-2">
          {quickActions.map((item) => (
            <Link
              key={item.name}
              to={item.href}
              className="flex items-center space-x-3 px-3 py-2 text-sm text-gray-700 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors group"
            >
              <item.icon className="w-4 h-4 text-gray-400 group-hover:text-primary-500" />
              <span>{item.name}</span>
            </Link>
          ))}
        </div>
      </div>

      {/* Main Navigation */}
      <div className="mb-8">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Navigation
        </h3>
        <nav className="space-y-1">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-3 px-3 py-2 text-sm font-medium rounded-lg transition-colors group ${
                  isActive(item.href)
                    ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600'
                    : 'text-gray-700 hover:text-primary-600 hover:bg-primary-50'
                }`}
              >
                <Icon 
                  className={`w-4 h-4 ${
                    isActive(item.href) 
                      ? 'text-primary-500' 
                      : 'text-gray-400 group-hover:text-primary-500'
                  }`} 
                />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Study Stats */}
      <div className="mb-8">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Today's Goal
        </h3>
        <div className="bg-gradient-to-r from-primary-50 to-accent-50 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Study Time</span>
            <span className="text-sm text-primary-600 font-semibold">45/60 min</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-primary-500 to-accent-500 h-2 rounded-full transition-all duration-300"
              style={{ width: '75%' }}
            ></div>
          </div>
          <p className="text-xs text-gray-500 mt-2">Keep up the great work! 🚀</p>
        </div>
      </div>

      {/* Recent Activity */}
      <div className="mb-8">
        <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
          Recent Activity
        </h3>
        <div className="space-y-2">
          <div className="flex items-center space-x-2 text-xs text-gray-600">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span>Completed Physics Quiz</span>
          </div>
          <div className="flex items-center space-x-2 text-xs text-gray-600">
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <span>Uploaded Math Notes</span>
          </div>
          <div className="flex items-center space-x-2 text-xs text-gray-600">
            <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
            <span>Reviewed 15 Flashcards</span>
          </div>
        </div>
      </div>

      {/* Settings */}
      <div className="mt-auto">
        <Link
          to="/settings"
          className="flex items-center space-x-3 px-3 py-2 text-sm text-gray-600 hover:text-primary-600 hover:bg-gray-50 rounded-lg transition-colors"
        >
          <Settings className="w-4 h-4" />
          <span>Settings</span>
        </Link>
      </div>
    </div>
  );
};

export default Sidebar;