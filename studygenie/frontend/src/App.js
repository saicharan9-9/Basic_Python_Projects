import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { LanguageProvider } from './contexts/LanguageContext';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/Auth/ProtectedRoute';

// Pages
import Login from './pages/Auth/Login';
import Register from './pages/Auth/Register';
import Dashboard from './pages/Dashboard/Dashboard';
import Documents from './pages/Documents/Documents';
import StudyMaterials from './pages/StudyMaterials/StudyMaterials';
import Quiz from './pages/Quiz/Quiz';
import Flashcards from './pages/Flashcards/Flashcards';
import AITutor from './pages/AITutor/AITutor';
import Progress from './pages/Progress/Progress';
import Settings from './pages/Settings/Settings';

function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <div className="min-h-screen bg-gray-50">
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            
            {/* Protected routes */}
            <Route
              path="/*"
              element={
                <ProtectedRoute>
                  <Layout>
                    <Routes>
                      <Route path="/" element={<Dashboard />} />
                      <Route path="/dashboard" element={<Dashboard />} />
                      <Route path="/documents" element={<Documents />} />
                      <Route path="/study-materials" element={<StudyMaterials />} />
                      <Route path="/quiz/:quizId" element={<Quiz />} />
                      <Route path="/flashcards/:setId" element={<Flashcards />} />
                      <Route path="/ai-tutor" element={<AITutor />} />
                      <Route path="/progress" element={<Progress />} />
                      <Route path="/settings" element={<Settings />} />
                    </Routes>
                  </Layout>
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </LanguageProvider>
    </AuthProvider>
  );
}

export default App;