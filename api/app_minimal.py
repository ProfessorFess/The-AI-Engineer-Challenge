# Minimal FastAPI app to test deployment
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Minimal Test API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint."""
    return {
        "status": "minimal_deployment_working", 
        "environment": "vercel" if os.getenv("VERCEL") else "local"
    }

@app.get("/api/health")
async def health_check():
    """Basic health check."""
    return {"status": "ok", "version": "minimal"}

# For Vercel deployment
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = None
