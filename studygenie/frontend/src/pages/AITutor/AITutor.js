import React, { useState, useRef, useEffect } from 'react';
import { useQuery, useMutation } from 'react-query';
import { Send, Bot, User, FileText, Loader2 } from 'lucide-react';
import { aiTutorAPI, documentsAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import toast from 'react-hot-toast';

const AITutor = () => {
  const { t, availableLanguages } = useLanguage();
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'ai',
      content: t('aiTutorHelp'),
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [selectedDocument, setSelectedDocument] = useState('');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const { data: documents } = useQuery(
    'documents',
    () => documentsAPI.getAll(),
    {
      select: (response) => response.data.filter(doc => doc.processing_status === 'completed')
    }
  );

  const { data: indexedDocuments } = useQuery(
    'indexedDocuments',
    aiTutorAPI.getIndexedDocuments,
    {
      select: (response) => response.data
    }
  );

  const chatMutation = useMutation(aiTutorAPI.chat, {
    onSuccess: (response) => {
      const aiMessage = {
        id: Date.now(),
        type: 'ai',
        content: response.data.response,
        sources: response.data.sources,
        confidence: response.data.confidence,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Failed to get response';
      toast.error(message);
      
      const errorMessage = {
        id: Date.now(),
        type: 'ai',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
  });

  const indexMutation = useMutation(aiTutorAPI.indexDocument, {
    onSuccess: () => {
      toast.success('Document indexed successfully!');
      // Refresh indexed documents
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Failed to index document';
      toast.error(message);
    }
  });

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    
    const chatData = {
      message: inputMessage,
      language: selectedLanguage,
      ...(selectedDocument && { document_id: parseInt(selectedDocument) })
    };

    chatMutation.mutate(chatData);
    setInputMessage('');
  };

  const handleIndexDocument = (documentId) => {
    indexMutation.mutate({ document_id: documentId });
  };

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    });
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 h-full">
      <div className="bg-white rounded-lg shadow-lg h-[calc(100vh-8rem)] flex flex-col">
        {/* Header */}
        <div className="border-b border-gray-200 p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="flex-shrink-0">
                <Bot className="h-8 w-8 text-primary-600" />
              </div>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">{t('aiTutor')}</h1>
                <p className="text-sm text-gray-500">Ask questions about your study materials</p>
              </div>
            </div>
            
            {/* Controls */}
            <div className="flex items-center space-x-4">
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="text-sm border border-gray-300 rounded-md px-3 py-1"
              >
                {availableLanguages.map((lang) => (
                  <option key={lang.code} value={lang.code}>
                    {lang.name}
                  </option>
                ))}
              </select>
              
              <select
                value={selectedDocument}
                onChange={(e) => setSelectedDocument(e.target.value)}
                className="text-sm border border-gray-300 rounded-md px-3 py-1"
              >
                <option value="">All Documents</option>
                {documents?.map((doc) => (
                  <option key={doc.id} value={doc.id}>
                    {doc.original_filename}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Document Indexing Status */}
        {documents && documents.length > 0 && (
          <div className="border-b border-gray-200 p-4 bg-gray-50">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium text-gray-700">Document Index Status:</span>
              <div className="flex space-x-2">
                {documents.map((doc) => {
                  const indexed = indexedDocuments?.find(idx => idx.id === doc.id);
                  return (
                    <div key={doc.id} className="flex items-center space-x-1">
                      <FileText className="h-4 w-4 text-gray-400" />
                      <span className="text-xs text-gray-600 truncate max-w-20" title={doc.original_filename}>
                        {doc.original_filename}
                      </span>
                      {indexed?.indexed ? (
                        <span className="text-xs text-green-600">✓</span>
                      ) : (
                        <button
                          onClick={() => handleIndexDocument(doc.id)}
                          disabled={indexMutation.isLoading}
                          className="text-xs text-blue-600 hover:text-blue-800"
                        >
                          Index
                        </button>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-xs lg:max-w-md xl:max-w-lg ${
                message.type === 'user' 
                  ? 'bg-primary-600 text-white' 
                  : 'bg-gray-100 text-gray-900'
              } rounded-lg px-4 py-2`}>
                <div className="flex items-start space-x-2">
                  {message.type === 'ai' && (
                    <Bot className="h-5 w-5 mt-0.5 text-primary-600" />
                  )}
                  {message.type === 'user' && (
                    <User className="h-5 w-5 mt-0.5 text-white" />
                  )}
                  <div className="flex-1">
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    
                    {/* Sources */}
                    {message.sources && message.sources.length > 0 && (
                      <div className="mt-2 pt-2 border-t border-gray-200">
                        <p className="text-xs text-gray-500 mb-1">Sources:</p>
                        <div className="space-y-1">
                          {message.sources.map((source, index) => (
                            <div key={index} className="text-xs text-gray-600 bg-white bg-opacity-50 rounded px-2 py-1">
                              📄 {source}
                            </div>
                          ))}
                        </div>
                        {message.confidence && (
                          <div className="mt-1 text-xs text-gray-500">
                            Confidence: {(message.confidence * 100).toFixed(0)}%
                          </div>
                        )}
                      </div>
                    )}
                    
                    <p className="text-xs mt-2 opacity-75">
                      {formatTimestamp(message.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          {/* Loading indicator */}
          {chatMutation.isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 rounded-lg px-4 py-2">
                <div className="flex items-center space-x-2">
                  <Bot className="h-5 w-5 text-primary-600" />
                  <div className="flex space-x-1">
                    <div className="pulse-dot" />
                    <div className="pulse-dot" />
                    <div className="pulse-dot" />
                  </div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <form onSubmit={handleSendMessage} className="flex space-x-2">
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder={t('askQuestion')}
              className="flex-1 input"
              disabled={chatMutation.isLoading}
            />
            <button
              type="submit"
              disabled={chatMutation.isLoading || !inputMessage.trim()}
              className="btn-primary px-4 py-2 disabled:opacity-50"
            >
              {chatMutation.isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AITutor;