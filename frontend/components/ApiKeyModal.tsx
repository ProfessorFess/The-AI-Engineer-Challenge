'use client'

import { useState } from 'react'
import { X, Key, Settings, Bot } from 'lucide-react'

interface ApiKeyModalProps {
  isOpen: boolean
  onClose: () => void
  onSubmit: (apiKey: string) => void
  developerMessage: string
  setDeveloperMessage: (message: string) => void
  model: string
  setModel: (model: string) => void
}

export default function ApiKeyModal({ 
  isOpen, 
  onClose, 
  onSubmit, 
  developerMessage, 
  setDeveloperMessage, 
  model, 
  setModel 
}: ApiKeyModalProps) {
  const [apiKey, setApiKey] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)

  if (!isOpen) return null

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (apiKey.trim()) {
      onSubmit(apiKey.trim())
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="bg-gradient-to-r from-sage-100 to-earth-100 px-6 py-4 border-b border-earth-200 rounded-t-2xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-white rounded-lg shadow-sm">
                <Key className="h-5 w-5 text-sage-700" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-earth-800">Setup Required</h2>
                <p className="text-sm text-earth-600">Configure your OpenAI API key</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 text-earth-600 hover:text-earth-800 hover:bg-white/50 rounded-lg transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* API Key Input */}
            <div>
              <label htmlFor="apiKey" className="block text-sm font-medium text-earth-700 mb-2">
                OpenAI API Key *
              </label>
              <div className="relative">
                <input
                  type="password"
                  id="apiKey"
                  value={apiKey}
                  onChange={(e) => setApiKey(e.target.value)}
                  placeholder="sk-..."
                  className="w-full px-4 py-3 pr-10 border border-earth-300 rounded-xl focus:ring-2 focus:ring-sage-500 focus:border-sage-500 bg-white text-earth-800 placeholder-earth-400"
                  required
                />
                <Key className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-earth-400" />
              </div>
              <p className="mt-2 text-xs text-earth-600">
                Your API key is stored locally and never sent to our servers.
              </p>
            </div>

            {/* Advanced Settings Toggle */}
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="flex items-center space-x-2 text-sage-600 hover:text-sage-700 transition-colors"
            >
              <Settings className="h-4 w-4" />
              <span className="text-sm font-medium">Advanced Settings</span>
            </button>

            {/* Advanced Settings */}
            {showAdvanced && (
              <div className="space-y-4 p-4 bg-earth-50 rounded-xl border border-earth-200">
                {/* Model Selection */}
                <div>
                  <label htmlFor="model" className="block text-sm font-medium text-earth-700 mb-2">
                    Model
                  </label>
                  <select
                    id="model"
                    value={model}
                    onChange={(e) => setModel(e.target.value)}
                    className="w-full px-4 py-3 border border-earth-300 rounded-xl focus:ring-2 focus:ring-sage-500 focus:border-sage-500 bg-white text-earth-800"
                  >
                    <option value="gpt-4o-mini">GPT-4o Mini</option>
                    <option value="gpt-4o">GPT-4o</option>
                    <option value="gpt-4-turbo">GPT-4 Turbo</option>
                    <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                  </select>
                </div>

                {/* Developer Message */}
                <div>
                  <label htmlFor="developerMessage" className="block text-sm font-medium text-earth-700 mb-2">
                    System Message
                  </label>
                  <textarea
                    id="developerMessage"
                    value={developerMessage}
                    onChange={(e) => setDeveloperMessage(e.target.value)}
                    placeholder="You are a helpful AI assistant."
                    rows={3}
                    className="w-full px-4 py-3 border border-earth-300 rounded-xl focus:ring-2 focus:ring-sage-500 focus:border-sage-500 bg-white text-earth-800 placeholder-earth-400 resize-none"
                  />
                  <p className="mt-1 text-xs text-earth-600">
                    This message sets the context for how the AI should behave.
                  </p>
                </div>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={!apiKey.trim()}
              className="w-full px-6 py-3 bg-sage-600 text-white rounded-xl hover:bg-sage-700 disabled:bg-earth-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center space-x-2"
            >
              <Bot className="h-4 w-4" />
              <span>Start Chatting</span>
            </button>
          </form>

          {/* Help Text */}
          <div className="mt-6 p-4 bg-sage-50 rounded-xl border border-sage-200">
            <h3 className="text-sm font-medium text-sage-800 mb-2">Need help?</h3>
            <ul className="text-xs text-sage-700 space-y-1">
              <li>• Get your API key from <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" className="text-sage-600 hover:text-sage-800 underline">OpenAI Platform</a></li>
              <li>• Make sure your API key has sufficient credits</li>
              <li>• The key is stored in your browser's local storage</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
