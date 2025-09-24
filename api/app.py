# Lightweight FastAPI app for Vercel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from typing import Optional

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

# Test endpoint
@app.get("/api/test")
async def test_endpoint():
    return {
        "status": "working",
        "timestamp": "2024-09-24_minimal",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# Health check
@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

# Chat endpoint (basic - no PDF for now)
@app.post("/api/chat")
async def chat(request: ChatRequest):
    """Basic chat endpoint using OpenAI."""
    try:
        client = OpenAI(api_key=request.api_key)
        
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

# Placeholder for PDF endpoints (will add back once basic app works)
@app.get("/api/pdf-status")
async def pdf_status():
    return {
        "has_pdf": False,
        "filename": "",
        "chunks_count": 0,
        "note": "PDF functionality temporarily disabled - basic chat working"
    }

# For Vercel deployment
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = None