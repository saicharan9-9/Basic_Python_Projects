from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import chromadb
from chromadb.utils import embedding_functions

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.models.document import Document
from app.api.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    language: str = "en"
    document_id: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    confidence: float

class DocumentIndexRequest(BaseModel):
    document_id: int

def get_or_create_collection(user_id: int, document_id: int):
    """Get or create a ChromaDB collection for a user's document"""
    collection_name = f"user_{user_id}_doc_{document_id}"
    
    try:
        collection = chroma_client.get_collection(
            name=collection_name,
            embedding_function=embedding_function
        )
    except:
        collection = chroma_client.create_collection(
            name=collection_name,
            embedding_function=embedding_function,
            metadata={"user_id": user_id, "document_id": document_id}
        )
    
    return collection

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        
        # If we're not at the end, try to break at a sentence boundary
        if end < len(text):
            # Look for sentence endings within the last 200 characters
            last_period = text.rfind('.', start, end)
            last_question = text.rfind('?', start, end)
            last_exclamation = text.rfind('!', start, end)
            
            sentence_end = max(last_period, last_question, last_exclamation)
            
            if sentence_end > start + chunk_size - 200:
                end = sentence_end + 1
        
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        
        start = end - overlap
    
    return chunks

@router.post("/index-document")
async def index_document(
    request: DocumentIndexRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Index a document for RAG-based questioning"""
    
    # Verify document exists and belongs to user
    document = db.query(Document).filter(
        Document.id == request.document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document.processing_status != "completed" or not document.extracted_text:
        raise HTTPException(
            status_code=400,
            detail="Document must be processed and have extracted text"
        )
    
    # Get or create collection
    collection = get_or_create_collection(current_user.id, document.id)
    
    # Check if already indexed
    existing_docs = collection.get()
    if existing_docs['ids']:
        return {"message": "Document already indexed", "chunks": len(existing_docs['ids'])}
    
    # Chunk the text
    chunks = chunk_text(document.extracted_text)
    
    # Create documents for ChromaDB
    documents = []
    metadatas = []
    ids = []
    
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        metadatas.append({
            "document_id": document.id,
            "chunk_index": i,
            "filename": document.original_filename,
            "file_type": document.file_type
        })
        ids.append(f"doc_{document.id}_chunk_{i}")
    
    # Add to collection
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    
    return {"message": f"Document indexed successfully with {len(chunks)} chunks"}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_tutor(
    chat_request: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Chat with AI tutor using RAG"""
    
    relevant_context = ""
    sources = []
    confidence = 0.0
    
    # If document_id is provided, search in that specific document
    if chat_request.document_id:
        document = db.query(Document).filter(
            Document.id == chat_request.document_id,
            Document.owner_id == current_user.id
        ).first()
        
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        try:
            collection = get_or_create_collection(current_user.id, document.id)
            
            # Search for relevant chunks
            results = collection.query(
                query_texts=[chat_request.message],
                n_results=3,
                include=["documents", "metadatas", "distances"]
            )
            
            if results['documents'] and results['documents'][0]:
                relevant_context = "\n\n".join(results['documents'][0])
                sources = [f"{document.original_filename} (chunk {i})" 
                          for i in range(len(results['documents'][0]))]
                
                # Calculate confidence based on similarity scores
                if results['distances'] and results['distances'][0]:
                    # Convert distance to similarity (lower distance = higher similarity)
                    similarities = [1 - d for d in results['distances'][0]]
                    confidence = max(similarities) if similarities else 0.0
        
        except Exception as e:
            print(f"Error searching document: {str(e)}")
    
    else:
        # Search across all user's documents
        try:
            user_documents = db.query(Document).filter(
                Document.owner_id == current_user.id,
                Document.processing_status == "completed"
            ).all()
            
            all_results = []
            
            for doc in user_documents:
                try:
                    collection = get_or_create_collection(current_user.id, doc.id)
                    results = collection.query(
                        query_texts=[chat_request.message],
                        n_results=2,
                        include=["documents", "metadatas", "distances"]
                    )
                    
                    if results['documents'] and results['documents'][0]:
                        for i, (document_text, metadata, distance) in enumerate(
                            zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
                        ):
                            all_results.append({
                                'text': document_text,
                                'source': metadata['filename'],
                                'distance': distance
                            })
                
                except Exception as e:
                    print(f"Error searching document {doc.id}: {str(e)}")
                    continue
            
            # Sort by similarity and take top 3
            all_results.sort(key=lambda x: x['distance'])
            top_results = all_results[:3]
            
            if top_results:
                relevant_context = "\n\n".join([r['text'] for r in top_results])
                sources = [r['source'] for r in top_results]
                confidence = 1 - top_results[0]['distance'] if top_results else 0.0
        
        except Exception as e:
            print(f"Error in global search: {str(e)}")
    
    # Generate response using AI service
    if not relevant_context:
        response = await ai_service.answer_question(
            chat_request.message,
            "I don't have specific context from your documents to answer this question. I can provide general information, but for more accurate answers, please upload relevant study materials.",
            chat_request.language
        )
        confidence = 0.1
    else:
        response = await ai_service.answer_question(
            chat_request.message,
            relevant_context,
            chat_request.language
        )
    
    return ChatResponse(
        response=response,
        sources=sources,
        confidence=confidence
    )

@router.get("/documents")
async def get_indexed_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of documents that have been indexed for RAG"""
    
    documents = db.query(Document).filter(
        Document.owner_id == current_user.id,
        Document.processing_status == "completed"
    ).all()
    
    indexed_docs = []
    
    for doc in documents:
        try:
            collection = get_or_create_collection(current_user.id, doc.id)
            existing_docs = collection.get()
            chunk_count = len(existing_docs['ids']) if existing_docs['ids'] else 0
            
            indexed_docs.append({
                "id": doc.id,
                "filename": doc.original_filename,
                "file_type": doc.file_type,
                "indexed": chunk_count > 0,
                "chunk_count": chunk_count,
                "created_at": doc.created_at.isoformat()
            })
        
        except Exception as e:
            indexed_docs.append({
                "id": doc.id,
                "filename": doc.original_filename,
                "file_type": doc.file_type,
                "indexed": False,
                "chunk_count": 0,
                "created_at": doc.created_at.isoformat(),
                "error": str(e)
            })
    
    return indexed_docs

@router.delete("/index/{document_id}")
async def remove_document_index(
    document_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a document's index from the vector database"""
    
    # Verify document belongs to user
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.owner_id == current_user.id
    ).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        collection_name = f"user_{current_user.id}_doc_{document_id}"
        chroma_client.delete_collection(name=collection_name)
        return {"message": "Document index removed successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error removing document index: {str(e)}"
        )