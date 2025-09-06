import { MessageCircle, Settings } from 'lucide-react'

export default function Header() {
  return (
    <header className="bg-white/80 backdrop-blur-sm border-b border-earth-200 shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sage-100 rounded-lg">
              <MessageCircle className="h-6 w-6 text-sage-700" />
            </div>
            <div>
              <h1 className="text-xl font-semibold text-earth-800">AI Chat</h1>
              <p className="text-sm text-earth-600">Powered by OpenAI</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-sm text-earth-600">Online</span>
          </div>
        </div>
      </div>
    </header>
  )
}
