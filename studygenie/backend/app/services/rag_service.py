import faiss
import numpy as np
import pickle
import os
from typing import List, Tuple, Dict
from sentence_transformers import SentenceTransformer
import openai
from ..models import TutorResponse

class RAGService:
    def __init__(self, vector_db_path: str = "./data/vector_db"):
        self.vector_db_path = vector_db_path
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = 384  # Dimension of all-MiniLM-L6-v2 embeddings
        self.client = openai.OpenAI()
        
        # Create directory if it doesn't exist
        os.makedirs(vector_db_path, exist_ok=True)
        
        # Initialize or load existing index
        self.index = None
        self.documents = {}  # document_id -> {chunks: [], metadata: {}}
        self.chunk_to_doc = {}  # chunk_index -> document_id
        self.load_or_create_index()
    
    def load_or_create_index(self):
        """Load existing FAISS index or create a new one"""
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        metadata_path = os.path.join(self.vector_db_path, "metadata.pkl")
        
        if os.path.exists(index_path) and os.path.exists(metadata_path):
            try:
                self.index = faiss.read_index(index_path)
                with open(metadata_path, 'rb') as f:
                    metadata = pickle.load(f)
                    self.documents = metadata.get('documents', {})
                    self.chunk_to_doc = metadata.get('chunk_to_doc', {})
                print("Loaded existing FAISS index")
            except Exception as e:
                print(f"Error loading index: {e}. Creating new index.")
                self.index = faiss.IndexFlatIP(self.dimension)
        else:
            self.index = faiss.IndexFlatIP(self.dimension)
            print("Created new FAISS index")
    
    def save_index(self):
        """Save FAISS index and metadata to disk"""
        index_path = os.path.join(self.vector_db_path, "faiss_index.bin")
        metadata_path = os.path.join(self.vector_db_path, "metadata.pkl")
        
        faiss.write_index(self.index, index_path)
        
        metadata = {
            'documents': self.documents,
            'chunk_to_doc': self.chunk_to_doc
        }
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks for better retrieval"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            if chunk.strip():
                chunks.append(chunk)
        
        return chunks
    
    def add_document(self, document_id: str, text: str, metadata: Dict = None):
        """Add a document to the vector database"""
        # Chunk the text
        chunks = self.chunk_text(text)
        
        if not chunks:
            return
        
        # Generate embeddings for chunks
        embeddings = self.embedding_model.encode(chunks)
        
        # Normalize embeddings for cosine similarity
        embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Add to FAISS index
        start_idx = self.index.ntotal
        self.index.add(embeddings.astype('float32'))
        
        # Store document metadata
        self.documents[document_id] = {
            'chunks': chunks,
            'metadata': metadata or {},
            'start_idx': start_idx,
            'end_idx': start_idx + len(chunks)
        }
        
        # Update chunk to document mapping
        for i, chunk_idx in enumerate(range(start_idx, start_idx + len(chunks))):
            self.chunk_to_doc[chunk_idx] = document_id
        
        # Save to disk
        self.save_index()
    
    def search_similar_chunks(self, query: str, document_id: str = None, top_k: int = 5) -> List[Tuple[str, float, str]]:
        """Search for similar text chunks"""
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query])
        query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
        
        # Search in FAISS
        scores, indices = self.index.search(query_embedding.astype('float32'), top_k * 2)  # Get more to filter
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # No more results
                break
            
            chunk_doc_id = self.chunk_to_doc.get(idx)
            if document_id and chunk_doc_id != document_id:
                continue  # Skip if not from the specified document
            
            if chunk_doc_id in self.documents:
                doc_info = self.documents[chunk_doc_id]
                chunk_idx_in_doc = idx - doc_info['start_idx']
                if 0 <= chunk_idx_in_doc < len(doc_info['chunks']):
                    chunk_text = doc_info['chunks'][chunk_idx_in_doc]
                    results.append((chunk_text, float(score), chunk_doc_id))
        
        return results[:top_k]
    
    def answer_question(self, question: str, document_id: str = None, language: str = "en") -> TutorResponse:
        """Answer a question using RAG"""
        # Search for relevant chunks
        relevant_chunks = self.search_similar_chunks(question, document_id, top_k=3)
        
        if not relevant_chunks:
            return TutorResponse(
                answer="I don't have enough information to answer this question based on the provided materials.",
                sources=[],
                confidence=0.0
            )
        
        # Prepare context from relevant chunks
        context = "\n\n".join([chunk for chunk, _, _ in relevant_chunks])
        
        language_map = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi"
        }
        
        prompt = f"""
        You are a helpful AI tutor. Answer the student's question based ONLY on the provided context in {language_map.get(language, 'English')}.
        
        Context from study materials:
        {context}
        
        Student's Question: {question}
        
        Requirements:
        - Answer in simple, clear language appropriate for students
        - Base your answer ONLY on the provided context
        - If the context doesn't contain enough information, say so
        - Be encouraging and supportive
        - Provide examples when helpful
        - Keep the answer concise but complete
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Calculate confidence based on relevance scores
            avg_score = np.mean([score for _, score, _ in relevant_chunks])
            confidence = min(avg_score * 2, 1.0)  # Scale to 0-1
            
            sources = [f"Document chunk {i+1}" for i, _ in enumerate(relevant_chunks)]
            
            return TutorResponse(
                answer=answer,
                sources=sources,
                confidence=confidence
            )
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")
    
    def remove_document(self, document_id: str):
        """Remove a document from the vector database"""
        if document_id not in self.documents:
            return
        
        # Note: FAISS doesn't support efficient deletion, so we'd need to rebuild
        # For now, we'll mark it as deleted in metadata
        del self.documents[document_id]
        
        # Update chunk mapping
        self.chunk_to_doc = {k: v for k, v in self.chunk_to_doc.items() if v != document_id}
        
        self.save_index()
    
    def get_document_stats(self) -> Dict:
        """Get statistics about the vector database"""
        return {
            "total_documents": len(self.documents),
            "total_chunks": self.index.ntotal,
            "dimension": self.dimension
        }