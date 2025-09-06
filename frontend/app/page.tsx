'use client'

import { useState } from 'react'
import ChatInterface from '@/components/ChatInterface'
import Header from '@/components/Header'

export default function Home() {
  const [isConfigured, setIsConfigured] = useState(false)

  return (
    <main className="min-h-screen">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-earth-800 mb-4">
              AI Chat Assistant
            </h1>
            <p className="text-lg text-earth-600 max-w-2xl mx-auto">
              Experience intelligent conversations with our AI-powered chat interface. 
              Built with beautiful earth tones and designed for clarity and comfort.
            </p>
          </div>
          
          <ChatInterface 
            isConfigured={isConfigured}
            onConfigured={() => setIsConfigured(true)}
          />
        </div>
      </div>
    </main>
  )
}
