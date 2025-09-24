"""Hybrid solution: PDF RAG functionality using BaseHTTPRequestHandler pattern"""

from http.server import BaseHTTPRequestHandler
import json
import tempfile
import os
import math
from urllib.parse import urlparse, parse_qs
import cgi
import io

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/health':
                self._send_json_response({
                    "status": "ok",
                    "environment": "vercel" if os.getenv("VERCEL") else "local"
                })
            elif path == '/api/test':
                self._send_json_response({
                    "status": "working_with_pdf",
                    "timestamp": "2024-09-24_hybrid",
                    "environment": "vercel" if os.getenv("VERCEL") else "local",
                    "features": ["chat", "pdf_upload", "pdf_rag"]
                })
            elif path == '/api/pdf-status':
                self._send_json_response({
                    "has_pdf": False,
                    "filename": "",
                    "chunks_count": 0,
                    "note": "PDF processing is stateless. Upload PDF and chunks are sent with each chat request."
                })
            else:
                self._send_error_response(404, "Not Found")
                
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        try:
            if path == '/api/chat':
                self._handle_chat()
            elif path == '/api/upload-pdf':
                self._handle_pdf_upload()
            else:
                self._send_error_response(404, "Not Found")
                
        except Exception as e:
            self._send_error_response(500, str(e))
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self._send_cors_headers()
        self.end_headers()
    
    def _handle_chat(self):
        """Handle chat requests"""
        try:
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Validate required fields
            if not data.get('api_key') or not data.get('user_message'):
                self._send_error_response(400, "Missing required fields: api_key, user_message")
                return
            
            # Import OpenAI using v0.x API (Vercel-compatible)
            try:
                import openai
                
                # Set API key using v0.x style
                openai.api_key = data['api_key']
                
                model = data.get('model', 'gpt-3.5-turbo')
                developer_message = data.get('developer_message', 'You are a helpful AI assistant.')
                user_message = data['user_message']
                pdf_chunks = data.get('pdf_chunks')
                pdf_filename = data.get('pdf_filename')
                
                # Check if we have PDF chunks for RAG
                if pdf_chunks and len(pdf_chunks) > 0:
                    # Simple similarity search for relevant chunks
                    relevant_chunks = self._simple_similarity_search(user_message, pdf_chunks, 3)
                    context = "\n\n".join(relevant_chunks)
                    
                    # Enhanced system message with PDF context
                    pdf_name = pdf_filename or "the uploaded document"
                    enhanced_system_message = f"""You are an AI assistant that answers questions based on the provided context from {pdf_name}.

IMPORTANT:
- Only use information from the provided context to answer questions
- If the context doesn't contain enough information, say "I cannot find that information in the uploaded document"
- Be accurate and cite specific parts of the context when possible

Context from the document:
{context}

{developer_message}"""
                    
                    # Chat with PDF context
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": enhanced_system_message},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=500
                    )
                else:
                    # Standard chat without PDF
                    response = openai.ChatCompletion.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": developer_message},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=500
                    )
                
                self._send_json_response({
                    "content": response.choices[0].message.content
                })
                return
                    
            except Exception as e:
                self._send_error_response(500, f"OpenAI error: {str(e)}")
                return
            model = data.get('model', 'gpt-4o-mini')
            developer_message = data.get('developer_message', 'You are a helpful AI assistant.')
            user_message = data['user_message']
            pdf_chunks = data.get('pdf_chunks')
            pdf_filename = data.get('pdf_filename')
            
            # Check if we have PDF chunks for RAG
            if pdf_chunks and len(pdf_chunks) > 0:
                # Simple similarity search (basic implementation)
                relevant_chunks = self._simple_similarity_search(user_message, pdf_chunks, 3)
                context = "\n\n".join(relevant_chunks)
                
                # Enhanced system message with context
                pdf_name = pdf_filename or "the uploaded document"
                enhanced_system_message = f"""You are an AI assistant that answers questions based on the provided context from {pdf_name}.

IMPORTANT:
- Only use information from the provided context to answer questions
- If the context doesn't contain enough information, say "I cannot find that information in the uploaded document"
- Be accurate and cite specific parts of the context when possible

Context from the document:
{context}

{developer_message}"""
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": enhanced_system_message},
                        {"role": "user", "content": user_message}
                    ],
                    stream=False
                )
            else:
                # Standard chat without PDF
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": developer_message},
                        {"role": "user", "content": user_message}
                    ],
                    stream=False
                )
            
            self._send_json_response({
                "content": response.choices[0].message.content
            })
            
        except Exception as e:
            self._send_error_response(500, f"Chat error: {str(e)}")
    
    def _handle_pdf_upload(self):
        """Handle PDF upload requests"""
        try:
            # Parse multipart form data
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self._send_error_response(400, "Content-Type must be multipart/form-data")
                return
            
            # Read the body
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Parse form data (simplified - real implementation would need more robust parsing)
            self._send_error_response(501, "PDF upload temporarily disabled - working on multipart parsing")
            
        except Exception as e:
            self._send_error_response(500, f"PDF upload error: {str(e)}")
    
    def _simple_similarity_search(self, query, chunks, k=3):
        """Simple text-based similarity search (fallback when no embeddings)"""
        query_lower = query.lower()
        scored_chunks = []
        
        for chunk in chunks:
            # Simple scoring based on word overlap
            chunk_lower = chunk.lower()
            score = sum(1 for word in query_lower.split() if word in chunk_lower)
            scored_chunks.append((score, chunk))
        
        # Sort by score and return top k
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [chunk for _, chunk in scored_chunks[:k]]
    
    def _send_json_response(self, data, status_code=200):
        """Send JSON response with CORS headers"""
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_error_response(self, status_code, message):
        """Send error response"""
        self.send_response(status_code)
        self._send_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        error_data = {"detail": message}
        self.wfile.write(json.dumps(error_data).encode())
    
    def _send_cors_headers(self):
        """Send CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
