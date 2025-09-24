'use client'

import { useState, useEffect } from 'react'
import { FileText } from 'lucide-react'
import ChatInterface from '@/components/ChatInterface'
import PDFUpload from '@/components/PDFUpload'
import Header from '@/components/Header'

export default function Home() {
  const [isConfigured, setIsConfigured] = useState(false)
  const [apiKey, setApiKey] = useState('')
  const [uploadedFile, setUploadedFile] = useState('')
  const [chunksCount, setChunksCount] = useState(0)
  const [uploadError, setUploadError] = useState('')
  const [pdfChunks, setPdfChunks] = useState<string[]>([])  // Store PDF chunks

  const handleUploadSuccess = (filename: string, chunksProcessed: number, chunks: string[]) => {
    setUploadedFile(filename)
    setChunksCount(chunksProcessed)
    setPdfChunks(chunks)  // Store the actual PDF chunks
    setUploadError('')
  }

  const handleUploadError = (error: string) => {
    setUploadError(error)
    setUploadedFile('')
    setChunksCount(0)
    setPdfChunks([])  // Clear PDF chunks on error
  }

  const handleConfigured = (key: string) => {
    setApiKey(key)
    setIsConfigured(true)
  }

  return (
    <main className="min-h-screen">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-earth-800 mb-4">
              AI Chat Assistant with PDF RAG
            </h1>
            {/* Force deployment refresh - {new Date().toISOString()} */}
            <p className="text-lg text-earth-600 max-w-3xl mx-auto">
              Upload a PDF document and chat with its content using advanced retrieval-augmented generation (RAG). 
              The AI will answer questions based solely on your uploaded document.
            </p>
          </div>
          
          <div className="grid gap-6 lg:grid-cols-2">
            {/* PDF Upload Section */}
            <div className="space-y-4">
              {isConfigured ? (
                <>
                  <PDFUpload
                    apiKey={apiKey}
                    onUploadSuccess={handleUploadSuccess}
                    onUploadError={handleUploadError}
                    currentFile={uploadedFile}
                  />
                  
                  {uploadError && (
                    <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                      <div className="flex items-center space-x-2">
                        <div className="text-red-600">⚠️</div>
                        <p className="text-red-700">{uploadError}</p>
                      </div>
                    </div>
                  )}
                  
                  {uploadedFile && (
                    <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                      <div className="text-sm text-blue-700">
                        <p><strong>Document:</strong> {uploadedFile}</p>
                        <p><strong>Text chunks processed:</strong> {chunksCount}</p>
                        <p className="mt-2 italic">
                          You can now ask questions about the content of this document!
                        </p>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="bg-white rounded-2xl shadow-lg border border-earth-200 p-6">
                  <div className="text-center">
                    <div className="mx-auto w-12 h-12 bg-sage-100 rounded-full flex items-center justify-center mb-4">
                      <FileText className="h-6 w-6 text-sage-600" />
                    </div>
                    <h3 className="text-lg font-medium text-earth-700 mb-2">PDF Upload</h3>
                    <p className="text-earth-600">
                      Configure your OpenAI API key in the chat interface to enable PDF upload and processing.
                    </p>
                  </div>
                </div>
              )}
            </div>
            
            {/* Chat Interface Section */}
            <div>
              <ChatInterface 
                isConfigured={isConfigured}
                onConfigured={handleConfigured}
                pdfChunks={pdfChunks}
                pdfFilename={uploadedFile}
              />
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
