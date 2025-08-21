import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { 
  RotateCcw, 
  ArrowRight, 
  ArrowLeft, 
  Eye, 
  EyeOff,
  CheckCircle,
  XCircle,
  Brain
} from 'lucide-react';
import { studyAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import toast from 'react-hot-toast';

const Flashcards = () => {
  const { setId } = useParams();
  const navigate = useNavigate();
  const { t } = useLanguage();
  const queryClient = useQueryClient();
  
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [studyMode, setStudyMode] = useState('all'); // 'all' or 'due'

  const { data: flashcards, isLoading } = useQuery(
    ['flashcards', setId, studyMode],
    () => studyAPI.getFlashcards(setId, studyMode === 'due'),
    {
      select: (response) => response.data,
      enabled: !!setId
    }
  );

  const reviewMutation = useMutation(studyAPI.reviewFlashcard, {
    onSuccess: () => {
      queryClient.invalidateQueries(['flashcards', setId]);
      handleNext();
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Failed to record review';
      toast.error(message);
    }
  });

  const handleReview = (correct, confidence = 'medium') => {
    if (!flashcards || flashcards.length === 0) return;
    
    const currentCard = flashcards[currentCardIndex];
    reviewMutation.mutate({
      flashcard_id: currentCard.id,
      correct,
      confidence
    });
  };

  const handleNext = () => {
    if (flashcards && currentCardIndex < flashcards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
      setShowAnswer(false);
    } else if (flashcards && currentCardIndex === flashcards.length - 1) {
      // End of flashcards
      toast.success('Great job! You\'ve completed all flashcards.');
      navigate('/study-materials');
    }
  };

  const handlePrevious = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1);
      setShowAnswer(false);
    }
  };

  const handleReset = () => {
    setCurrentCardIndex(0);
    setShowAnswer(false);
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-8"></div>
          <div className="bg-white rounded-lg shadow-lg p-8 h-96">
            <div className="h-6 bg-gray-200 rounded w-3/4 mb-4"></div>
            <div className="h-32 bg-gray-200 rounded w-full"></div>
          </div>
        </div>
      </div>
    );
  }

  if (!flashcards || flashcards.length === 0) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center py-12">
          <Brain className="mx-auto h-16 w-16 text-gray-400 mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            {studyMode === 'due' ? 'No cards due for review' : 'No flashcards found'}
          </h2>
          <p className="text-gray-600 mb-6">
            {studyMode === 'due' 
              ? 'Great job! Come back later for more reviews.'
              : 'This flashcard set doesn\'t exist or has no cards.'
            }
          </p>
          <div className="space-x-4">
            {studyMode === 'due' && (
              <button
                onClick={() => setStudyMode('all')}
                className="btn-outline"
              >
                Study All Cards
              </button>
            )}
            <button
              onClick={() => navigate('/study-materials')}
              className="btn-primary"
            >
              Back to Study Materials
            </button>
          </div>
        </div>
      </div>
    );
  }

  const currentCard = flashcards[currentCardIndex];
  const progress = ((currentCardIndex + 1) / flashcards.length) * 100;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Flashcard Study</h1>
          <p className="text-gray-600">
            Card {currentCardIndex + 1} of {flashcards.length}
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <label className="text-sm font-medium text-gray-700">Study Mode:</label>
            <select
              value={studyMode}
              onChange={(e) => {
                setStudyMode(e.target.value);
                setCurrentCardIndex(0);
                setShowAnswer(false);
              }}
              className="text-sm border border-gray-300 rounded-md px-2 py-1"
            >
              <option value="all">All Cards</option>
              <option value="due">Due for Review</option>
            </select>
          </div>
          
          <button
            onClick={handleReset}
            className="btn-outline"
          >
            <RotateCcw className="h-4 w-4 mr-2" />
            Reset
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>Progress</span>
          <span>{Math.round(progress)}%</span>
        </div>
        <div className="bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 rounded-full h-2 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* Flashcard */}
      <div className="bg-white rounded-lg shadow-lg overflow-hidden mb-8">
        <div 
          className="p-8 min-h-[300px] flex items-center justify-center cursor-pointer hover:bg-gray-50 transition-colors"
          onClick={() => setShowAnswer(!showAnswer)}
        >
          <div className="text-center w-full">
            <div className="mb-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-800">
                {showAnswer ? 'Answer' : 'Question'}
              </span>
            </div>
            
            <div className="text-xl font-medium text-gray-900 mb-4">
              {showAnswer ? currentCard.back_text : currentCard.front_text}
            </div>
            
            {!showAnswer && (
              <div className="flex items-center justify-center text-gray-500 text-sm">
                <Eye className="h-4 w-4 mr-2" />
                Click to reveal answer
              </div>
            )}
            
            {showAnswer && (
              <div className="mt-6 pt-4 border-t border-gray-200">
                <div className="text-sm text-gray-600 mb-4">
                  <strong>Question:</strong> {currentCard.front_text}
                </div>
                <div className="flex items-center justify-center text-gray-500 text-sm">
                  <EyeOff className="h-4 w-4 mr-2" />
                  Click to hide answer
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Card Info */}
      <div className="bg-gray-50 rounded-lg p-4 mb-8">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Difficulty:</span>
            <span className="ml-2 capitalize">{currentCard.difficulty}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Reviews:</span>
            <span className="ml-2">{currentCard.review_count}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Interval:</span>
            <span className="ml-2">{currentCard.review_interval} days</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Next Review:</span>
            <span className="ml-2">
              {currentCard.next_review 
                ? new Date(currentCard.next_review).toLocaleDateString()
                : 'Now'
              }
            </span>
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex justify-between items-center">
        <button
          onClick={handlePrevious}
          disabled={currentCardIndex === 0}
          className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ArrowLeft className="h-5 w-5 mr-2" />
          Previous
        </button>

        {showAnswer ? (
          <div className="flex space-x-4">
            <div className="text-center">
              <p className="text-sm text-gray-600 mb-2">How did you do?</p>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleReview(false, 'low')}
                  disabled={reviewMutation.isLoading}
                  className="flex items-center px-4 py-2 bg-red-100 text-red-700 rounded-md hover:bg-red-200 transition-colors"
                >
                  <XCircle className="h-4 w-4 mr-2" />
                  Hard
                </button>
                <button
                  onClick={() => handleReview(true, 'medium')}
                  disabled={reviewMutation.isLoading}
                  className="flex items-center px-4 py-2 bg-yellow-100 text-yellow-700 rounded-md hover:bg-yellow-200 transition-colors"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Good
                </button>
                <button
                  onClick={() => handleReview(true, 'high')}
                  disabled={reviewMutation.isLoading}
                  className="flex items-center px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 transition-colors"
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Easy
                </button>
              </div>
            </div>
          </div>
        ) : (
          <button
            onClick={() => setShowAnswer(true)}
            className="btn-primary"
          >
            {t('showAnswer')}
          </button>
        )}

        <button
          onClick={handleNext}
          disabled={!showAnswer}
          className="btn-outline disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {currentCardIndex === flashcards.length - 1 ? 'Finish' : 'Skip'}
          <ArrowRight className="h-5 w-5 ml-2" />
        </button>
      </div>
    </div>
  );
};

export default Flashcards;