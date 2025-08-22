import React, { useState, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { useDropzone } from 'react-dropzone';
import { 
  Upload, 
  FileText, 
  Trash2, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  Clock,
  Download,
  Eye
} from 'lucide-react';
import { documentsAPI } from '../../services/api';
import { useLanguage } from '../../contexts/LanguageContext';
import toast from 'react-hot-toast';

const Documents = () => {
  const { t } = useLanguage();
  const queryClient = useQueryClient();
  const [selectedDocument, setSelectedDocument] = useState(null);

  const { data: documents, isLoading } = useQuery(
    'documents',
    () => documentsAPI.getAll(),
    {
      select: (response) => response.data
    }
  );

  const uploadMutation = useMutation(documentsAPI.upload, {
    onSuccess: () => {
      queryClient.invalidateQueries('documents');
      toast.success('Document uploaded successfully!');
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Upload failed';
      toast.error(message);
    }
  });

  const deleteMutation = useMutation(documentsAPI.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('documents');
      toast.success('Document deleted successfully!');
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Delete failed';
      toast.error(message);
    }
  });

  const reprocessMutation = useMutation(documentsAPI.reprocess, {
    onSuccess: () => {
      queryClient.invalidateQueries('documents');
      toast.success('Document reprocessing started!');
    },
    onError: (error) => {
      const message = error.response?.data?.detail || 'Reprocess failed';
      toast.error(message);
    }
  });

  const onDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      const formData = new FormData();
      formData.append('file', file);
      uploadMutation.mutate(formData);
    });
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'text/plain': ['.txt'],
      'image/*': ['.png', '.jpg', '.jpeg']
    },
    multiple: true
  });

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      case 'processing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />;
      default:
        return <Clock className="h-5 w-5 text-yellow-500" />;
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'completed':
        return t('completed');
      case 'failed':
        return t('failed');
      case 'processing':
        return t('processing');
      default:
        return 'Pending';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleViewDocument = async (docId) => {
    try {
      const response = await documentsAPI.getById(docId);
      setSelectedDocument(response.data);
    } catch (error) {
      toast.error('Failed to load document details');
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
      {/* Upload Area */}
      <div className="mb-8">
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${isDragActive 
              ? 'border-primary-400 bg-primary-50' 
              : 'border-gray-300 hover:border-gray-400'
            }
          `}
        >
          <input {...getInputProps()} />
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {t('uploadDocument')}
          </h3>
          <p className="text-gray-500 mb-4">
            {isDragActive 
              ? 'Drop the files here...' 
              : 'Drag & drop files here, or click to select files'
            }
          </p>
          <p className="text-sm text-gray-400">
            {t('supportedFormats')}
          </p>
        </div>
      </div>

      {/* Documents Grid */}
      {documents && documents.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {documents.map((doc) => (
            <div key={doc.id} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <FileText className="h-8 w-8 text-blue-500" />
                  <div className="flex items-center space-x-1">
                    {getStatusIcon(doc.processing_status)}
                    <span className="text-sm text-gray-500">
                      {getStatusText(doc.processing_status)}
                    </span>
                  </div>
                </div>
                
                <h3 className="text-lg font-medium text-gray-900 mb-2 truncate" title={doc.original_filename}>
                  {doc.original_filename}
                </h3>
                
                <div className="space-y-2 text-sm text-gray-500">
                  <div className="flex justify-between">
                    <span>Type:</span>
                    <span className="uppercase">{doc.file_type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Size:</span>
                    <span>{formatFileSize(doc.file_size)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Uploaded:</span>
                    <span>{new Date(doc.created_at).toLocaleDateString()}</span>
                  </div>
                </div>
                
                <div className="mt-6 flex space-x-2">
                  {doc.processing_status === 'completed' && (
                    <button
                      onClick={() => handleViewDocument(doc.id)}
                      className="flex-1 btn-outline text-sm py-2"
                    >
                      <Eye className="h-4 w-4 mr-1" />
                      View
                    </button>
                  )}
                  
                  {doc.processing_status === 'failed' && (
                    <button
                      onClick={() => reprocessMutation.mutate(doc.id)}
                      disabled={reprocessMutation.isLoading}
                      className="flex-1 btn-secondary text-sm py-2"
                    >
                      <RefreshCw className={`h-4 w-4 mr-1 ${reprocessMutation.isLoading ? 'animate-spin' : ''}`} />
                      Retry
                    </button>
                  )}
                  
                  <button
                    onClick={() => {
                      if (window.confirm('Are you sure you want to delete this document?')) {
                        deleteMutation.mutate(doc.id);
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
          <FileText className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No documents</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by uploading your first document.
          </p>
        </div>
      )}

      {/* Document Detail Modal */}
      {selectedDocument && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-11/12 max-w-4xl shadow-lg rounded-md bg-white">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-medium text-gray-900">
                {selectedDocument.original_filename}
              </h3>
              <button
                onClick={() => setSelectedDocument(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <XCircle className="h-6 w-6" />
              </button>
            </div>
            
            <div className="mb-4 p-4 bg-gray-50 rounded-lg">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="font-medium">File Type:</span> {selectedDocument.file_type.toUpperCase()}
                </div>
                <div>
                  <span className="font-medium">Size:</span> {formatFileSize(selectedDocument.file_size)}
                </div>
                <div>
                  <span className="font-medium">Language:</span> {selectedDocument.language.toUpperCase()}
                </div>
                <div>
                  <span className="font-medium">Status:</span> {getStatusText(selectedDocument.processing_status)}
                </div>
              </div>
            </div>
            
            {selectedDocument.extracted_text && (
              <div>
                <h4 className="text-md font-medium text-gray-900 mb-2">Extracted Text:</h4>
                <div className="max-h-96 overflow-y-auto p-4 bg-gray-50 rounded-lg text-sm text-gray-700">
                  <pre className="whitespace-pre-wrap">{selectedDocument.extracted_text}</pre>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default Documents;