# PDF RAG Testing Guide

This guide explains how to test the new PDF RAG functionality that has been implemented.

## Prerequisites

1. OpenAI API key
2. Python 3.8+ with pip
3. Node.js 18+ with npm
4. A PDF document for testing

## Backend Setup

1. **Navigate to the API directory:**
   ```bash
   cd api
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install new Python dependencies (if not already installed):**
   ```bash
   pip install PyPDF2 python-dotenv numpy
   ```

4. **Start the backend server:**
   ```bash
   python app.py
   ```
   
   Or alternatively:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```
   
   The backend should start on `http://localhost:8000`

**Note:** Make sure to keep the virtual environment activated for all backend operations.

## Frontend Setup

1. **Open a new terminal and navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   
   The frontend should start on `http://localhost:3000`

## Testing the PDF RAG Functionality

### Step 1: Configure API Key
1. Open `http://localhost:3000` in your browser
2. Click the settings icon or wait for the API key modal to appear
3. Enter your OpenAI API key
4. Optionally modify the system message and model selection
5. Click "Save Configuration"

### Step 2: Upload a PDF
1. You should see a PDF upload area on the left side
2. Either drag and drop a PDF file or click "Choose PDF File"
3. Watch the upload progress indicator
4. Once uploaded, you should see confirmation with:
   - Filename
   - Number of text chunks processed
   - Success message

### Step 3: Test RAG Chat
1. In the chat interface on the right side, ask questions about your PDF content
2. Examples:
   - "What is this document about?"
   - "Summarize the main points"
   - "What does the document say about [specific topic]?"

### Step 4: Verify RAG Behavior
1. **Context-only responses:** The AI should only answer based on the PDF content
2. **Fallback behavior:** If no PDF is uploaded, it works as a regular chat
3. **Error handling:** Try asking about content not in the PDF - it should say it cannot find that information

## API Endpoints for Manual Testing

You can also test the backend API directly:

### Health Check
```bash
curl http://localhost:8000/api/health
```

### PDF Status
```bash
curl http://localhost:8000/api/pdf-status
```

### Upload PDF
```bash
curl -X POST http://localhost:8000/api/upload-pdf \
  -F "file=@your-document.pdf" \
  -F "api_key=your-openai-api-key"
```

### Chat with RAG
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "developer_message": "You are a helpful assistant.",
    "user_message": "What is this document about?",
    "model": "gpt-4o-mini",
    "api_key": "your-openai-api-key"
  }'
```

## Expected Behavior

### With PDF Uploaded:
- Questions are answered using only the PDF content
- Responses include citations or references to specific parts
- AI refuses to answer questions outside the document scope

### Without PDF:
- Functions as a regular chat assistant
- Uses general knowledge and follows the system prompt

## Troubleshooting

### Backend Issues:
- **Import errors:** Make sure `aimakerspace` directory is in the project root
- **PDF processing errors:** Ensure PyPDF2 is installed and PDF is valid
- **Embedding errors:** Verify OpenAI API key is valid

### Frontend Issues:
- **API proxy errors:** Ensure backend is running on port 8000
- **Upload failures:** Check file size (max 10MB) and format (PDF only)
- **CORS issues:** Backend has CORS enabled for all origins

### Common Error Messages:
- "Only PDF files are allowed" - Upload a .pdf file
- "Could not extract text from PDF" - PDF might be image-based or corrupted
- "API Error: 401" - Invalid OpenAI API key
- "File size must be less than 10MB" - Reduce PDF size

## Architecture Overview

The implementation uses:
- **Backend:** FastAPI with aimakerspace library for RAG
- **PDF Processing:** PyPDF2 for text extraction
- **Text Chunking:** CharacterTextSplitter (1000 chars, 200 overlap)
- **Embeddings:** OpenAI text-embedding-3-small model
- **Vector Search:** Cosine similarity with top-3 results
- **Frontend:** Next.js with React components
- **Styling:** Tailwind CSS with earth-tone design system

## Performance Notes

- PDF processing time depends on document size
- First query after upload may be slower (embedding generation)
- Subsequent queries are fast (vector search)
- Memory usage scales with document size
