import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Brain, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { useLanguage } from '../../contexts/LanguageContext';

const Register = () => {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
    preferred_language: 'en'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const { t, availableLanguages } = useLanguage();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    const success = await register(formData);
    
    if (success) {
      navigate('/login');
    } else {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-secondary-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <div className="flex justify-center">
            <div className="flex items-center">
              <Brain className="w-12 h-12 text-primary-600" />
              <span className="ml-2 text-3xl font-bold text-gray-900">StudyGenie</span>
            </div>
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {t('register')}
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link
              to="/login"
              className="font-medium text-primary-600 hover:text-primary-500"
            >
              {t('login')}
            </Link>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                {t('email')}
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                className="mt-1 input w-full"
                placeholder={t('email')}
                value={formData.email}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700">
                {t('username')}
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                className="mt-1 input w-full"
                placeholder={t('username')}
                value={formData.username}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700">
                {t('fullName')}
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                className="mt-1 input w-full"
                placeholder={t('fullName')}
                value={formData.full_name}
                onChange={handleChange}
              />
            </div>

            <div>
              <label htmlFor="preferred_language" className="block text-sm font-medium text-gray-700">
                {t('preferredLanguage')}
              </label>
              <select
                id="preferred_language"
                name="preferred_language"
                className="mt-1 input w-full"
                value={formData.preferred_language}
                onChange={handleChange}
              >
                {availableLanguages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                {t('password')}
              </label>
              <div className="mt-1 relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  className="input w-full pr-10"
                  placeholder={t('password')}
                  value={formData.password}
                  onChange={handleChange}
                />
                <button
                  type="button"
                  className="absolute inset-y-0 right-0 pr-3 flex items-center"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </button>
              </div>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full btn-primary py-3 text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="spinner mr-2" />
                  {t('loading')}
                </div>
              ) : (
                t('register')
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;