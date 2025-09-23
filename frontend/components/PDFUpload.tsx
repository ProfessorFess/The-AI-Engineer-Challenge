'use client'

import { useState, useRef } from 'react'
import { Upload, FileText, X, CheckCircle, AlertCircle } from 'lucide-react'

interface PDFUploadProps {
  apiKey: string
  onUploadSuccess: (filename: string, chunksCount: number) => void
  onUploadError: (error: string) => void
  currentFile?: string
}

export default function PDFUpload({ 
  apiKey, 
  onUploadSuccess, 
  onUploadError, 
  currentFile 
}: PDFUploadProps) {
  const [isUploading, setIsUploading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFile = async (file: File) => {
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      onUploadError('Please select a PDF file')
      return
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
      onUploadError('File size must be less than 10MB')
      return
    }

    setIsUploading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('api_key', apiKey)

      console.log('Uploading PDF:', file.name, 'API key length:', apiKey?.length || 0)

      const response = await fetch('/api/upload-pdf', {
        method: 'POST',
        body: formData,
      })

      console.log('Upload response status:', response.status, response.statusText)

      if (!response.ok) {
        let errorMessage = 'Upload failed'
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || `HTTP ${response.status}: ${response.statusText}`
        } catch (jsonError) {
          // If JSON parsing fails, the server likely returned HTML (error page)
          const textError = await response.text()
          errorMessage = `Server error (${response.status}): ${textError.substring(0, 100)}...`
        }
        throw new Error(errorMessage)
      }

      const result = await response.json()
      onUploadSuccess(result.filename, result.chunks_processed)
    } catch (error) {
      onUploadError(error instanceof Error ? error.message : 'Upload failed')
    } finally {
      setIsUploading(false)
    }
  }

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }

  const openFileDialog = () => {
    fileInputRef.current?.click()
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-earth-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-sage-100 to-earth-100 px-6 py-4 border-b border-earth-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-white rounded-lg shadow-sm">
            <FileText className="h-5 w-5 text-sage-700" />
          </div>
          <div>
            <h2 className="font-semibold text-earth-800">PDF Document</h2>
            <p className="text-sm text-earth-600">Upload a PDF to chat with its content</p>
          </div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="p-6">
        {currentFile ? (
          /* Current File Display */
          <div className="flex items-center justify-between p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div>
                <p className="font-medium text-green-800">{currentFile}</p>
                <p className="text-sm text-green-600">Ready for questions</p>
              </div>
            </div>
            <button
              onClick={openFileDialog}
              className="px-4 py-2 text-green-700 hover:text-green-800 hover:bg-green-100 rounded-lg transition-colors text-sm font-medium"
            >
              Replace
            </button>
          </div>
        ) : (
          /* Upload Interface */
          <div
            className={`relative border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
              dragActive
                ? 'border-sage-400 bg-sage-50'
                : isUploading
                ? 'border-earth-300 bg-earth-50'
                : 'border-earth-300 hover:border-sage-400 hover:bg-sage-50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              className="hidden"
              disabled={isUploading}
            />

            <div className="space-y-4">
              <div className="mx-auto w-12 h-12 bg-sage-100 rounded-full flex items-center justify-center">
                {isUploading ? (
                  <div className="animate-spin rounded-full h-6 w-6 border-2 border-sage-300 border-t-sage-600"></div>
                ) : (
                  <Upload className="h-6 w-6 text-sage-600" />
                )}
              </div>

              <div>
                <h3 className="text-lg font-medium text-earth-700 mb-2">
                  {isUploading ? 'Processing PDF...' : 'Upload a PDF document'}
                </h3>
                <p className="text-earth-600 mb-4">
                  {isUploading 
                    ? 'Extracting text and creating vector embeddings...'
                    : 'Drag and drop your PDF file here, or click to browse'
                  }
                </p>
                
                {!isUploading && (
                  <button
                    onClick={openFileDialog}
                    className="px-6 py-3 bg-sage-600 text-white rounded-xl hover:bg-sage-700 transition-colors font-medium"
                  >
                    Choose PDF File
                  </button>
                )}
              </div>

              <div className="text-sm text-earth-500">
                <p>Maximum file size: 10MB</p>
                <p>Supported format: PDF</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
