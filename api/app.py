# Import required FastAPI components for building the API
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# Import Pydantic for data validation and settings management
from pydantic import BaseModel
# Import OpenAI client for interacting with OpenAI's API
from openai import OpenAI, AsyncOpenAI
import os
import asyncio
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any

# Import aimakerspace components for RAG functionality (local copy for Vercel)
from aimakerspace.text_utils import PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase
from aimakerspace.openai_utils.embedding import EmbeddingModel

# Initialize FastAPI application with a title
app = FastAPI(title="OpenAI Chat API with RAG")

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the API to be accessed from different domains/origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin
    allow_credentials=True,  # Allows cookies to be included in requests
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers in requests
)

# Custom embedding model that accepts API key dynamically
class CustomEmbeddingModel:
    """Custom embedding model that uses provided API key instead of environment variable."""
    
    def __init__(self, api_key: str, embeddings_model_name: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.embeddings_model_name = embeddings_model_name
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
    
    def get_embedding(self, text: str) -> List[float]:
        """Return an embedding for a single text."""
        embedding = self.client.embeddings.create(
            input=text, model=self.embeddings_model_name
        )
        return embedding.data[0].embedding
    
    def get_embeddings(self, list_of_text: List[str]) -> List[List[float]]:
        """Return embeddings for multiple texts."""
        embedding_response = self.client.embeddings.create(
            input=list_of_text, model=self.embeddings_model_name
        )
        return [item.embedding for item in embedding_response.data]
    
    async def async_get_embedding(self, text: str) -> List[float]:
        """Return an embedding for a single text using async."""
        embedding = await self.async_client.embeddings.create(
            input=text, model=self.embeddings_model_name
        )
        return embedding.data[0].embedding
    
    async def async_get_embeddings(self, list_of_text: List[str]) -> List[List[float]]:
        """Return embeddings for multiple texts using async."""
        embedding_response = await self.async_client.embeddings.create(
            input=list(list_of_text), model=self.embeddings_model_name
        )
        return [item.embedding for item in embedding_response.data]

# For Vercel deployment, we need to handle stateless nature
import json
from pathlib import Path
import base64

# Define the data models for API requests using Pydantic
# This ensures incoming request data is properly validated
class ChatRequest(BaseModel):
    developer_message: str  # Message from the developer/system
    user_message: str      # Message from the user
    model: Optional[str] = "gpt-4o-mini"  # Optional model selection with default
    api_key: str          # OpenAI API key for authentication
    pdf_chunks: Optional[List[str]] = None  # Optional PDF chunks for RAG
    pdf_filename: Optional[str] = None  # Optional PDF filename for context

class PDFUploadResponse(BaseModel):
    message: str
    filename: str
    chunks_processed: int
    chunks: List[str]  # Return the processed chunks for client-side storage

class PDFStatusResponse(BaseModel):
    has_pdf: bool
    filename: str
    chunks_count: int
    note: str = "PDF state is not persistent in serverless environment"

# PDF upload endpoint
@app.post("/api/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...), api_key: str = Form(...)):
    """
    Upload and process a PDF file for RAG functionality.
    The PDF will be split into chunks and returned for client-side storage.
    Note: In serverless environment, state is not persistent between requests.
    """
    
    try:
        # Validate file type
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Check file size before processing (Vercel has 4.5MB limit for serverless functions)
        content = await file.read()
        if len(content) > 4 * 1024 * 1024:  # 4MB limit to be safe
            raise HTTPException(
                status_code=413, 
                detail="PDF file is too large. Please use a file smaller than 4MB for optimal processing on this platform."
            )
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Load and process the PDF using aimakerspace
            pdf_loader = PDFLoader(temp_file_path)
            pdf_loader.load_file()
            
            if not pdf_loader.documents:
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            
            pdf_content = pdf_loader.documents[0]
            
            # Debug: Check if PDF content was extracted
            if not pdf_content or len(pdf_content.strip()) == 0:
                raise HTTPException(status_code=400, detail="PDF appears to be empty or contains no extractable text")
            
            # Split the text into chunks
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split(pdf_content)
            
            # Debug: Check if chunks were created
            if not chunks or len(chunks) == 0:
                raise HTTPException(status_code=400, detail="Could not create text chunks from PDF content")
            
            # Validate API key (we don't need to test embeddings here to save time/cost)
            if not api_key or len(api_key.strip()) == 0:
                raise HTTPException(status_code=400, detail="OpenAI API key is required for PDF processing")
            
            # Return chunks for client-side storage (no server-side persistence in serverless)
            return PDFUploadResponse(
                message=f"PDF '{file.filename}' uploaded and processed successfully. Chunks are ready for RAG queries.",
                filename=file.filename,
                chunks_processed=len(chunks),
                chunks=chunks
            )
            
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# Check PDF status endpoint
@app.get("/api/pdf-status", response_model=PDFStatusResponse)
async def pdf_status():
    """
    Check PDF status. Note: In serverless environment, PDF state is not persistent.
    The client should manage PDF chunks and pass them with chat requests.
    """
    return PDFStatusResponse(
        has_pdf=False,
        filename="",
        chunks_count=0,
        note="PDF state is not persistent in serverless environment. Upload PDF and use chunks in chat requests."
    )

# Enhanced chat endpoint with RAG functionality
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """
    Enhanced chat endpoint that uses RAG when PDF chunks are provided.
    If no PDF chunks are provided, falls back to standard chat behavior.
    """
    try:
        # Initialize OpenAI client with the provided API key
        client = OpenAI(api_key=request.api_key)
        
        # Check if we have PDF chunks for RAG
        if request.pdf_chunks and len(request.pdf_chunks) > 0:
            # Create vector database on-the-fly for this request
            embedding_model = CustomEmbeddingModel(api_key=request.api_key)
            temp_vector_db = VectorDatabase(embedding_model=embedding_model)
            temp_vector_db = await temp_vector_db.abuild_from_list(request.pdf_chunks)
            
            # Use RAG approach: search for relevant context
            relevant_chunks = temp_vector_db.search_by_text(
                request.user_message, 
                k=3,  # Get top 3 most relevant chunks
                return_as_text=True
            )
            
            # Build context from relevant chunks
            context = "\n\n".join(relevant_chunks)
            
            # Create enhanced system message with context
            pdf_name = request.pdf_filename or "the uploaded document"
            enhanced_system_message = f"""You are an AI assistant that answers questions based solely on the provided context from {pdf_name}.

IMPORTANT INSTRUCTIONS:
- Only use information from the provided context to answer questions
- If the context doesn't contain enough information to answer the question, say "I cannot find that information in the uploaded document"
- Do not use your general knowledge - stick strictly to the provided context
- Be accurate and cite specific parts of the context when possible

Context from the document:
{context}

{request.developer_message}"""
            
            # Create chat completion with enhanced context
            response = client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": enhanced_system_message},
                    {"role": "user", "content": request.user_message}
                ],
                stream=False
            )
            
            return {"content": response.choices[0].message.content}
        
        else:
            # No PDF chunks provided - standard chat
            response = client.chat.completions.create(
                model=request.model,
                messages=[
                    {"role": "system", "content": request.developer_message},
                    {"role": "user", "content": request.user_message}
                ],
                stream=False
            )
            
            return {"content": response.choices[0].message.content}
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))

# Define a health check endpoint to verify API status
@app.get("/api/health")
async def health_check():
    # Detect if running on Vercel
    is_vercel = os.getenv("VERCEL") is not None
    
    return {
        "status": "ok",
        "environment": "vercel" if is_vercel else "local",
        "pdf_approach": "stateless - chunks processed per request" if is_vercel else "stateless - chunks processed per request",
        "note": "PDF chunks are processed on-the-fly for each chat request"
    }

# Entry point for running the application directly
if __name__ == "__main__":
    import uvicorn
    # Start the server on all network interfaces (0.0.0.0) on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)

# For Vercel deployment
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    # mangum not installed - running locally
    handler = None
