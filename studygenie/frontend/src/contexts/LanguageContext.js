import React, { createContext, useContext, useState } from 'react';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
};

const translations = {
  en: {
    // Navigation
    dashboard: 'Dashboard',
    documents: 'Documents',
    studyMaterials: 'Study Materials',
    aiTutor: 'AI Tutor',
    progress: 'Progress',
    settings: 'Settings',
    logout: 'Logout',
    
    // Common
    upload: 'Upload',
    delete: 'Delete',
    edit: 'Edit',
    save: 'Save',
    cancel: 'Cancel',
    loading: 'Loading...',
    error: 'Error',
    success: 'Success',
    
    // Dashboard
    welcomeBack: 'Welcome back',
    studyStreak: 'Study Streak',
    totalStudyTime: 'Total Study Time',
    flashcardsMastered: 'Flashcards Mastered',
    averageQuizScore: 'Average Quiz Score',
    recentActivity: 'Recent Activity',
    
    // Documents
    uploadDocument: 'Upload Document',
    supportedFormats: 'Supported formats: PDF, DOCX, TXT, Images',
    processing: 'Processing...',
    completed: 'Completed',
    failed: 'Failed',
    
    // Study Materials
    generateSummary: 'Generate Summary',
    generateQuiz: 'Generate Quiz',
    generateFlashcards: 'Generate Flashcards',
    difficulty: 'Difficulty',
    language: 'Language',
    
    // Quiz
    startQuiz: 'Start Quiz',
    nextQuestion: 'Next Question',
    submitAnswer: 'Submit Answer',
    quizCompleted: 'Quiz Completed!',
    yourScore: 'Your Score',
    correctAnswers: 'Correct Answers',
    
    // Flashcards
    showAnswer: 'Show Answer',
    nextCard: 'Next Card',
    markCorrect: 'I got it right',
    markIncorrect: 'I need more practice',
    confidence: 'Confidence',
    low: 'Low',
    medium: 'Medium',
    high: 'High',
    
    // AI Tutor
    askQuestion: 'Ask a question...',
    send: 'Send',
    aiTutorHelp: 'I can help you understand your study materials. Ask me anything!',
    
    // Auth
    login: 'Login',
    register: 'Register',
    email: 'Email',
    username: 'Username',
    password: 'Password',
    fullName: 'Full Name',
    preferredLanguage: 'Preferred Language'
  },
  hi: {
    // Navigation
    dashboard: 'डैशबोर्ड',
    documents: 'दस्तावेज़',
    studyMaterials: 'अध्ययन सामग्री',
    aiTutor: 'एआई शिक्षक',
    progress: 'प्रगति',
    settings: 'सेटिंग्स',
    logout: 'लॉग आउट',
    
    // Common
    upload: 'अपलोड',
    delete: 'मिटाएं',
    edit: 'संपादित करें',
    save: 'सेव करें',
    cancel: 'रद्द करें',
    loading: 'लोड हो रहा है...',
    error: 'त्रुटि',
    success: 'सफलता',
    
    // Dashboard
    welcomeBack: 'वापसी पर स्वागत',
    studyStreak: 'अध्ययन श्रृंखला',
    totalStudyTime: 'कुल अध्ययन समय',
    flashcardsMastered: 'फ्लैशकार्ड में महारत',
    averageQuizScore: 'औसत क्विज़ स्कोर',
    recentActivity: 'हाल की गतिविधि',
    
    // Documents
    uploadDocument: 'दस्तावेज़ अपलोड करें',
    supportedFormats: 'समर्थित प्रारूप: PDF, DOCX, TXT, छवियां',
    processing: 'प्रसंस्करण...',
    completed: 'पूर्ण',
    failed: 'असफल',
    
    // Study Materials
    generateSummary: 'सारांश बनाएं',
    generateQuiz: 'क्विज़ बनाएं',
    generateFlashcards: 'फ्लैशकार्ड बनाएं',
    difficulty: 'कठिनाई',
    language: 'भाषा',
    
    // Quiz
    startQuiz: 'क्विज़ शुरू करें',
    nextQuestion: 'अगला प्रश्न',
    submitAnswer: 'उत्तर सबमिट करें',
    quizCompleted: 'क्विज़ पूरी हुई!',
    yourScore: 'आपका स्कोर',
    correctAnswers: 'सही उत्तर',
    
    // Flashcards
    showAnswer: 'उत्तर दिखाएं',
    nextCard: 'अगला कार्ड',
    markCorrect: 'मैंने सही किया',
    markIncorrect: 'मुझे और अभ्यास चाहिए',
    confidence: 'आत्मविश्वास',
    low: 'कम',
    medium: 'मध्यम',
    high: 'उच्च',
    
    // AI Tutor
    askQuestion: 'एक प्रश्न पूछें...',
    send: 'भेजें',
    aiTutorHelp: 'मैं आपकी अध्ययन सामग्री को समझने में मदद कर सकता हूं। मुझसे कुछ भी पूछें!',
    
    // Auth
    login: 'लॉगिन',
    register: 'पंजीकरण',
    email: 'ईमेल',
    username: 'उपयोगकर्ता नाम',
    password: 'पासवर्ड',
    fullName: 'पूरा नाम',
    preferredLanguage: 'पसंदीदा भाषा'
  },
  mr: {
    // Navigation
    dashboard: 'डॅशबोर्ड',
    documents: 'दस्तऐवज',
    studyMaterials: 'अभ्यास सामग्री',
    aiTutor: 'एआय शिक्षक',
    progress: 'प्रगती',
    settings: 'सेटिंग्ज',
    logout: 'लॉग आउट',
    
    // Common
    upload: 'अपलोड',
    delete: 'हटवा',
    edit: 'संपादन',
    save: 'जतन करा',
    cancel: 'रद्द करा',
    loading: 'लोड होत आहे...',
    error: 'त्रुटी',
    success: 'यश',
    
    // Dashboard
    welcomeBack: 'परत स्वागत',
    studyStreak: 'अभ्यास शृंखला',
    totalStudyTime: 'एकूण अभ्यास वेळ',
    flashcardsMastered: 'फ्लॅशकार्डमध्ये प्रभुत्व',
    averageQuizScore: 'सरासरी क्विझ गुण',
    recentActivity: 'अलीकडील क्रियाकलाप',
    
    // Documents
    uploadDocument: 'दस्तऐवज अपलोड करा',
    supportedFormats: 'समर्थित स्वरूप: PDF, DOCX, TXT, प्रतिमा',
    processing: 'प्रक्रिया...',
    completed: 'पूर्ण',
    failed: 'अयशस्वी',
    
    // Study Materials
    generateSummary: 'सारांश तयार करा',
    generateQuiz: 'क्विझ तयार करा',
    generateFlashcards: 'फ्लॅशकार्ड तयार करा',
    difficulty: 'अडचण',
    language: 'भाषा',
    
    // Quiz
    startQuiz: 'क्विझ सुरू करा',
    nextQuestion: 'पुढील प्रश्न',
    submitAnswer: 'उत्तर सबमिट करा',
    quizCompleted: 'क्विझ पूर्ण झाली!',
    yourScore: 'तुमचा गुण',
    correctAnswers: 'बरोबर उत्तरे',
    
    // Flashcards
    showAnswer: 'उत्तर दाखवा',
    nextCard: 'पुढील कार्ड',
    markCorrect: 'मी बरोबर केले',
    markIncorrect: 'मला अधिक सराव हवा',
    confidence: 'आत्मविश्वास',
    low: 'कमी',
    medium: 'मध्यम',
    high: 'उच्च',
    
    // AI Tutor
    askQuestion: 'प्रश्न विचारा...',
    send: 'पाठवा',
    aiTutorHelp: 'मी तुमच्या अभ्यास सामग्रीला समजून घेण्यास मदत करू शकतो. मला काहीही विचारा!',
    
    // Auth
    login: 'लॉगिन',
    register: 'नोंदणी',
    email: 'ईमेल',
    username: 'वापरकर्ता नाव',
    password: 'पासवर्ड',
    fullName: 'पूर्ण नाव',
    preferredLanguage: 'पसंतीची भाषा'
  }
};

export const LanguageProvider = ({ children }) => {
  const [currentLanguage, setCurrentLanguage] = useState('en');

  const t = (key) => {
    return translations[currentLanguage][key] || key;
  };

  const changeLanguage = (language) => {
    if (translations[language]) {
      setCurrentLanguage(language);
    }
  };

  const value = {
    currentLanguage,
    changeLanguage,
    t,
    availableLanguages: [
      { code: 'en', name: 'English' },
      { code: 'hi', name: 'हिंदी' },
      { code: 'mr', name: 'मराठी' }
    ]
  };

  return (
    <LanguageContext.Provider value={value}>
      {children}
    </LanguageContext.Provider>
  );
};