import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  FileText, 
  Brain, 
  Target,
  Plus,
  Trash2,
  Eye,
  Play
} from 'lucide-react';
import { studyAPI, documentsAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import toast from 'react-hot-toast';

const StudyMaterials = () => {
  const { t, availableLanguages } = useLanguage();
  const queryClient = useQueryClient();
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createForm, setCreateForm] = useState({
    document_id: '',
    content_type: 'summary',
    language: 'en',
    difficulty_level: 'medium',
    subject: ''
  });

  const { data: materials, isLoading } = useQuery(
    'studyMaterials',
    () => studyAPI.getAll(),
    {
      select: (response) => response.data
    }
  );

  const { data: documents } = useQuery(
    'documents',
    () => documentsAPI.getAll(),
    {
      select: (response) => response.data.filter(doc => doc.processing_status === 'completed')
    }
  );

  const createMutation = useMutation(studyAPI.generate, {
    onSuccess: () => {
      queryClient.invalidateQueries('studyMaterials');
      setShowCreateModal(false);
      setCreateForm({
        document_id: '',
        content_type: 'summary',
        language: 'en',
        difficulty_level: 'medium',
        subject: ''
      });
      toast.success('Study material generation started!');
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Creation failed';
      toast.error(message);
    }
  });

  const deleteMutation = useMutation(studyAPI.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('studyMaterials');
      toast.success('Study material deleted successfully!');
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Delete failed';
      toast.error(message);
    }
  });

  const handleCreateSubmit = (e) => {
    e.preventDefault();
    createMutation.mutate(createForm);
  };

  const getContentTypeIcon = (type) => {
    switch (type) {
      case 'quiz':
        return <Target className="h-6 w-6 text-purple-500" />;
      case 'flashcard':
        return <Brain className="h-6 w-6 text-green-500" />;
      default:
        return <FileText className="h-6 w-6 text-blue-500" />;
    }
  };

  const getContentTypeColor = (type) => {
    switch (type) {
      case 'quiz':
        return 'bg-purple-50 border-purple-200';
      case 'flashcard':
        return 'bg-green-50 border-green-200';
      default:
        return 'bg-blue-50 border-blue-200';
    }
  };

  const getActionLink = (material) => {
    switch (material.content_type) {
      case 'quiz':
        return `/quiz/${material.id}`;
      case 'flashcard':
        return `/flashcards/${material.id}`;
      default:
        return null;
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white p-6 rounded-lg shadow">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                <div className="h-8 bg-gray-200 rounded w-full"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">{t('studyMaterials')}</h1>
          <p className="mt-1 text-gray-500">
            Generate and manage your study materials
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn-primary"
        >
          <Plus className="h-5 w-5 mr-2" />
          Create New
        </button>
      </div>

      {/* Materials Grid */}
      {materials && materials.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {materials.map((material) => (
            <div 
              key={material.id} 
              className={`bg-white rounded-lg shadow-md overflow-hidden border ${getContentTypeColor(material.content_type)}`}
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  {getContentTypeIcon(material.content_type)}
                  <span className="text-xs uppercase tracking-wide text-gray-500 font-semibold">
                    {material.content_type}
                  </span>
                </div>
                
                <h3 className="text-lg font-medium text-gray-900 mb-2 line-clamp-2">
                  {material.title}
                </h3>
                
                <div className="space-y-2 text-sm text-gray-500 mb-4">
                  {material.subject && (
                    <div className="flex justify-between">
                      <span>Subject:</span>
                      <span>{material.subject}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span>Language:</span>
                    <span className="uppercase">{material.language}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Difficulty:</span>
                    <span className="capitalize">{material.difficulty_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Created:</span>
                    <span>{new Date(material.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div className="flex space-x-2">
                  {getActionLink(material) && (
                    <Link
                      to={getActionLink(material)}
                      className="flex-1 btn-primary text-sm py-2 text-center"
                    >
                      <Play className="h-4 w-4 mr-1" />
                      Start
                    </Link>
                  )}
                  
                  {material.content_type === 'summary' && material.content && (
                    <button
                      onClick={() => {
                        // Open summary in modal or navigate to view
                        alert('Summary view coming soon!');
                      }}
                      className="flex-1 btn-outline text-sm py-2"
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      View
                    </button>
                  )}
                  
                  <button
                    onClick={() => {
                      if (window.confirm('Are you sure you want to delete this study material?')) {
                        deleteMutation.mutate(material.id);
                      }
                    }}
                    disabled={deleteMutation.isLoading}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-md transition-colors"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No study materials</h3>
          <p className="mt-1 text-sm text-gray-500">
            Create your first study material from uploaded documents.
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="mt-4 btn-primary"
          >
            <Plus className="h-5 w-5 mr-2" />
            Create Study Material
          </button>
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                Create Study Material
              </h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ×
              </button>
            </div>
            
            <form onSubmit={handleCreateSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Document
                </label>
                <select
                  value={createForm.document_id}
                  onChange={(e) => setCreateForm({...createForm, document_id: e.target.value})}
                  className="input w-full"
                  required
                >
                  <option value="">Select a document</option>
                  {documents?.map((doc) => (
                    <option key={doc.id} value={doc.id}>
                      {doc.original_filename}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Content Type
                </label>
                <select
                  value={createForm.content_type}
                  onChange={(e) => setCreateForm({...createForm, content_type: e.target.value})}
                  className="input w-full"
                >
                  <option value="summary">{t('generateSummary')}</option>
                  <option value="quiz">{t('generateQuiz')}</option>
                  <option value="flashcard">{t('generateFlashcards')}</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('language')}
                </label>
                <select
                  value={createForm.language}
                  onChange={(e) => setCreateForm({...createForm, language: e.target.value})}
                  className="input w-full"
                >
                  {availableLanguages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {t('difficulty')}
                </label>
                <select
                  value={createForm.difficulty_level}
                  onChange={(e) => setCreateForm({...createForm, difficulty_level: e.target.value})}
                  className="input w-full"
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Subject (Optional)
                </label>
                <input
                  type="text"
                  value={createForm.subject}
                  onChange={(e) => setCreateForm({...createForm, subject: e.target.value})}
                  className="input w-full"
                  placeholder="e.g., Mathematics, Physics"
                />
              </div>
              
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 btn-outline"
                >
                  {t('cancel')}
                </button>
                <button
                  type="submit"
                  disabled={createMutation.isLoading}
                  className="flex-1 btn-primary disabled:opacity-50"
                >
                  {createMutation.isLoading ? (
                    <div className="flex items-center justify-center">
                      <div className="spinner mr-2" />
                      Creating...
                    </div>
                  ) : (
                    'Create'
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default StudyMaterials;