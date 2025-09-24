# Lightweight FastAPI app for Vercel with PDF support
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI, AsyncOpenAI
import os
import tempfile
import math
from typing import Optional, List

# Initialize FastAPI application
app = FastAPI(title="AI Chat Assistant")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    developer_message: str
    user_message: str
    model: Optional[str] = "gpt-4o-mini"
    api_key: str
    pdf_chunks: Optional[List[str]] = None
    pdf_filename: Optional[str] = None

class PDFUploadResponse(BaseModel):
    message: str
    filename: str
    chunks_processed: int
    chunks: List[str]

class PDFStatusResponse(BaseModel):
    has_pdf: bool
    filename: str
    chunks_count: int
    note: str = "PDF processing handled client-side for serverless compatibility"

# Simple text chunking function
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """Simple text chunking with overlap."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    step = chunk_size - chunk_overlap
    
    for i in range(0, len(text), step):
        chunk = text[i:i + chunk_size]
        if chunk.strip():
            chunks.append(chunk)
    
    return chunks

# Simple cosine similarity
def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    dot_product = sum(x * y for x, y in zip(a, b))
    magnitude_a = math.sqrt(sum(x * x for x in a))
    magnitude_b = math.sqrt(sum(x * x for x in b))
    
    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0
    
    return dot_product / (magnitude_a * magnitude_b)

# Simple vector search
async def search_similar_chunks(query: str, chunks: List[str], api_key: str, k: int = 3) -> List[str]:
    """Find most similar chunks using OpenAI embeddings."""
    try:
        client = AsyncOpenAI(api_key=api_key)
        
        # Get embeddings for query and all chunks
        all_texts = [query] + chunks
        response = await client.embeddings.create(
            input=all_texts,
            model="text-embedding-3-small"
        )
        
        query_embedding = response.data[0].embedding
        chunk_embeddings = [item.embedding for item in response.data[1:]]
        
        # Calculate similarities
        similarities = []
        for i, chunk_embedding in enumerate(chunk_embeddings):
            similarity = cosine_similarity(query_embedding, chunk_embedding)
            similarities.append((similarity, chunks[i]))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in similarities[:k]]
        
    except Exception as e:
        # Fallback to simple text matching
        query_lower = query.lower()
        scored_chunks = []
        for chunk in chunks:
            score = sum(1 for word in query_lower.split() if word in chunk.lower())
            scored_chunks.append((score, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:k]]

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    return {
        "status": "working_with_pdf",
        "timestamp": "2024-09-24_complete",
        "environment": "vercel" if os.getenv("VERCEL") else "local",
        "features": ["chat", "pdf_upload", "pdf_rag"]
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# PDF Upload endpoint
@app.post("/api/upload-pdf", response_model=PDFUploadResponse)
async def upload_pdf(file: UploadFile = File(...), api_key: str = Form(...)):
    """Upload and process PDF file, return chunks for client-side storage."""
    try:
        # Validate file
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Check file size (4MB limit for Vercel)
        content = await file.read()
        if len(content) > 4 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="File too large. Maximum 4MB allowed.")
        
        # Process PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Import PyPDF2 inside function to handle import errors gracefully
            try:
                import PyPDF2
            except ImportError:
                raise HTTPException(status_code=500, detail="PDF processing library not available")
            
            # Extract text from PDF
            with open(temp_file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                raise HTTPException(status_code=400, detail="Could not extract text from PDF")
            
            # Chunk the text
            chunks = chunk_text(text)
            
            if not chunks:
                raise HTTPException(status_code=400, detail="No text chunks created from PDF")
            
            return PDFUploadResponse(
                message=f"PDF '{file.filename}' processed successfully",
                filename=file.filename,
                chunks_processed=len(chunks),
                chunks=chunks
            )
            
        finally:
            # Clean up temp file
            os.unlink(temp_file_path)
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

# PDF Status endpoint
@app.get("/api/pdf-status", response_model=PDFStatusResponse)
async def pdf_status():
    """PDF status - stateless architecture."""
    return PDFStatusResponse(
        has_pdf=False,
        filename="",
        chunks_count=0,
        note="PDF processing is stateless. Upload PDF and chunks are sent with each chat request."
    )

# Enhanced chat endpoint with PDF RAG support
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Chat endpoint with optional PDF RAG functionality."""
    try:
        client = OpenAI(api_key=request.api_key)
        
        # Check if we have PDF chunks for RAG
        if request.pdf_chunks and len(request.pdf_chunks) > 0:
            # Find relevant chunks using similarity search
            relevant_chunks = await search_similar_chunks(
                request.user_message, 
                request.pdf_chunks, 
                request.api_key,
                k=3
            )
            
            # Build context from relevant chunks
            context = "\n\n".join(relevant_chunks)
            
            # Create enhanced system message
            pdf_name = request.pdf_filename or "the uploaded document"
            enhanced_system_message = f"""You are an AI assistant that answers questions based on the provided context from {pdf_name}.

IMPORTANT:
- Only use information from the provided context to answer questions
- If the context doesn't contain enough information, say "I cannot find that information in the uploaded document"
- Be accurate and cite specific parts of the context when possible

Context from the document:
{context}

{request.developer_message}"""
            
            # Chat with context
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
            # Standard chat without PDF
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
        raise HTTPException(status_code=500, detail=str(e))

# For Vercel deployment - ASGI handler with proper pattern
from mangum import Mangum

# Create the handler in the pattern Vercel expects
handler = Mangum(app, lifespan="off")

# Also expose app directly for compatibility
application = app