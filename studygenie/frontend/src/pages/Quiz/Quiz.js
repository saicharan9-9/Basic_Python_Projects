import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation } from 'react-query';
import { CheckCircle, XCircle, Clock, ArrowRight, ArrowLeft } from 'lucide-react';
import { studyAPI, progressAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import toast from 'react-hot-toast';

const Quiz = () => {
  const { quizId } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [timeStarted] = useState(Date.now());

  const { data: quiz, isLoading } = useQuery(
    ['quiz', quizId],
    () => studyAPI.getQuiz(quizId),
    {
      select: (response) => response.data,
      enabled: !!quizId
    }
  );

  const submitMutation = useMutation(progressAPI.submitQuizAttempt, {
    onSuccess: (response) => {
      setShowResults(response.data);
      toast.success(`Quiz completed! Score: ${response.data.score.toFixed(1)}%`);
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Failed to submit quiz';
      toast.error(message);
    }
  });

  const handleAnswerSelect = (questionId, answer) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  const handleNext = () => {
    if (currentQuestionIndex < quiz.questions.length - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleSubmitQuiz = () => {
    const timeElapsed = Math.floor((Date.now() - timeStarted) / 1000);
    
    submitMutation.mutate({
      quiz_id: parseInt(quizId),
      answers,
      time_taken: timeElapsed
    });
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="bg-white rounded-lg shadow p-8">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="space-y-3">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="h-4 bg-gray-200 rounded w-full"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!quiz) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center py-12">
          <h2 className="text-2xl font-bold text-gray-900">Quiz not found</h2>
          <button
            onClick={() => navigate('/study-materials')}
            className="mt-4 btn-primary"
          >
            Back to Study Materials
          </button>
        </div>
      </div>
    );
  }

  if (showResults) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <CheckCircle className="mx-auto h-16 w-16 text-green-500 mb-4" />
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {t('quizCompleted')}
            </h2>
            <p className="text-xl text-gray-600">
              {t('yourScore')}: {showResults.score.toFixed(1)}%
            </p>
            <p className="text-lg text-gray-500">
              {showResults.correct_answers} out of {showResults.total_questions} correct
            </p>
          </div>

          {/* Detailed Results */}
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-gray-900">Detailed Results</h3>
            {showResults.detailed_results.map((result, index) => (
              <div
                key={result.question_id}
                className={`p-4 rounded-lg border ${
                  result.is_correct ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200'
                }`}
              >
                <div className="flex items-start space-x-3">
                  {result.is_correct ? (
                    <CheckCircle className="h-6 w-6 text-green-500 mt-1" />
                  ) : (
                    <XCircle className="h-6 w-6 text-red-500 mt-1" />
                  )}
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900 mb-2">
                      Question {index + 1}: {result.question_text}
                    </h4>
                    <div className="space-y-1 text-sm">
                      <p>
                        <span className="font-medium">Your answer:</span> {result.user_answer}
                      </p>
                      <p>
                        <span className="font-medium">Correct answer:</span> {result.correct_answer}
                      </p>
                      {result.explanation && (
                        <p className="text-gray-600 mt-2">
                          <span className="font-medium">Explanation:</span> {result.explanation}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-8 flex justify-center space-x-4">
            <button
              onClick={() => navigate('/study-materials')}
              className="btn-outline"
            >
              Back to Study Materials
            </button>
            <button
              onClick={() => window.location.reload()}
              className="btn-primary"
            >
              Retake Quiz
            </button>
          </div>
        </div>
      </div>
    );
  }

  const currentQuestion = quiz.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / quiz.questions.length) * 100;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        {/* Header */}
        <div className="bg-primary-600 text-white p-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold">{quiz.title}</h1>
              <p className="text-primary-100">
                Question {currentQuestionIndex + 1} of {quiz.questions.length}
              </p>
            </div>
            <div className="text-right">
              <div className="text-2xl font-bold">
                {Math.round(progress)}%
              </div>
              <div className="text-primary-100">Complete</div>
            </div>
          </div>
          
          {/* Progress Bar */}
          <div className="mt-4 bg-primary-700 rounded-full h-2">
            <div
              className="bg-white rounded-full h-2 transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Question */}
        <div className="p-8">
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">
              {currentQuestion.question_text}
            </h2>
            
            {/* Options */}
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => (
                <label
                  key={index}
                  className={`
                    flex items-center p-4 rounded-lg border-2 cursor-pointer transition-colors
                    ${answers[currentQuestion.id] === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }
                  `}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion.id}`}
                    value={option}
                    checked={answers[currentQuestion.id] === option}
                    onChange={() => handleAnswerSelect(currentQuestion.id, option)}
                    className="sr-only"
                  />
                  <div className={`
                    w-5 h-5 rounded-full border-2 mr-4 flex items-center justify-center
                    ${answers[currentQuestion.id] === option
                      ? 'border-primary-500 bg-primary-500'
                      : 'border-gray-300'
                    }
                  `}>
                    {answers[currentQuestion.id] === option && (
                      <div className="w-2 h-2 bg-white rounded-full" />
                    )}
                  </div>
                  <span className="text-gray-900">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center">
            <button
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
              className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="h-5 w-5 mr-2" />
              Previous
            </button>

            <div className="flex space-x-4">
              {currentQuestionIndex === quiz.questions.length - 1 ? (
                <button
                  onClick={handleSubmitQuiz}
                  disabled={submitMutation.isLoading || Object.keys(answers).length !== quiz.questions.length}
                  className="btn-primary disabled:opacity-50"
                >
                  {submitMutation.isLoading ? (
                    <>
                      <Clock className="h-5 w-5 mr-2 animate-spin" />
                      Submitting...
                    </>
                  ) : (
                    'Submit Quiz'
                  )}
                </button>
              ) : (
                <button
                  onClick={handleNext}
                  className="btn-primary"
                >
                  Next
                  <ArrowRight className="h-5 w-5 ml-2" />
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Quiz;