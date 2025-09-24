# Merge Instructions: PDF Upload Bug Fix

## Branch: `fix-pdf-upload-error`

### Summary
Fixed critical PDF upload functionality that was failing with `FUNCTION_INVOCATION_FAILED` error on Vercel deployment.

### Problem Identified
The root cause was an incompatibility between the custom `CustomEmbeddingModel` class and the `VectorDatabase` class:
- `VectorDatabase.abuild_from_list()` method called `await self.embedding_model.async_get_embeddings()` 
- The `CustomEmbeddingModel.async_get_embeddings()` was incorrectly implemented as a sync wrapper
- This caused the serverless function to fail during PDF processing

### Changes Made

#### 1. Fixed Async Compatibility (`api/app.py`)
- **Added AsyncOpenAI import**: Imported `AsyncOpenAI` alongside `OpenAI`
- **Enhanced CustomEmbeddingModel**: 
  - Added `self.async_client = AsyncOpenAI(api_key=api_key)` initialization
  - Implemented proper `async_get_embedding()` using `await self.async_client.embeddings.create()`
  - Implemented proper `async_get_embeddings()` using `await self.async_client.embeddings.create()`

#### 2. Added File Size Validation
- Added 4MB file size check before processing (respects Vercel's 4.5MB limit)
- Fixed duplicate file reading issue
- Provides clear error message for oversized files (HTTP 413)

### Files Modified
- `api/app.py`: Fixed async embedding methods and added file size validation

### Testing Recommendations
1. Test PDF upload with small file (< 1MB) to verify basic functionality
2. Test PDF upload with large file (> 4MB) to verify size limit enforcement
3. Test RAG chat functionality after successful PDF upload
4. Verify error handling with invalid file types

### Deployment Notes
- No dependency changes required (OpenAI 1.35.0 already supports AsyncOpenAI)
- Changes are backward compatible
- Function should now work properly in Vercel's serverless environment

### Merge Command
```bash
git checkout main
git merge fix-pdf-upload-error
git push origin main
```

### Post-Merge Verification
After merging and deploying to Vercel:
1. Upload a small PDF file to test the functionality
2. Ask questions about the PDF content to verify RAG is working
3. Monitor Vercel function logs for any remaining issues