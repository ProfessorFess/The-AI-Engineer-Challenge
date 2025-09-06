# AI Chat Frontend

A beautiful, responsive chat interface built with Next.js and styled with earth tones. This frontend connects to the FastAPI backend to provide a seamless AI chat experience.

## Features

- 🌿 **Earth Tone Design**: Beautiful color palette featuring browns, greens, and tans
- 💬 **Real-time Chat**: Streaming responses from OpenAI's API
- 🔐 **Secure API Key Management**: Local storage with password input fields
- ⚙️ **Advanced Settings**: Customizable system messages and model selection
- 📱 **Responsive Design**: Works perfectly on desktop and mobile devices
- ♿ **Accessibility**: Focus management and keyboard navigation support

## Prerequisites

- Node.js 18+ 
- npm or yarn
- The FastAPI backend running on `http://localhost:8000`
- An OpenAI API key

## Quick Start

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the Development Server**
   ```bash
   npm run dev
   ```

3. **Open Your Browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

4. **Configure Your API Key**
   - Enter your OpenAI API key when prompted
   - Optionally adjust the system message and model settings
   - Click "Start Chatting" to begin

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles with earth tone theme
│   ├── layout.tsx         # Root layout component
│   └── page.tsx           # Main page component
├── components/            # React components
│   ├── ApiKeyModal.tsx    # API key configuration modal
│   ├── ChatInterface.tsx  # Main chat interface
│   ├── Header.tsx         # Application header
│   └── MessageBubble.tsx  # Individual message component
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Design Philosophy

This frontend follows a **comfy earth tone** design philosophy:

- **Primary Colors**: Sage greens and warm earth browns
- **Accent Colors**: Soft tans and forest greens
- **Typography**: Clean, readable Inter font
- **Spacing**: Generous whitespace for visual comfort
- **Interactions**: Smooth transitions and hover effects

## API Integration

The frontend communicates with the FastAPI backend through:

- **POST** `/api/chat` - Send chat messages and receive streaming responses
- **GET** `/api/health` - Health check endpoint

## Security Features

- API keys are stored locally in the browser
- Password-style input fields for sensitive information
- No API keys are sent to external servers
- CORS configured for local development

## Customization

### Colors
Edit `tailwind.config.js` to modify the earth tone color palette:

```javascript
colors: {
  earth: { /* brown tones */ },
  sage: { /* green tones */ },
  tan: { /* tan tones */ },
  forest: { /* dark green tones */ }
}
```

### Models
Add new OpenAI models in the `ApiKeyModal.tsx` component:

```jsx
<option value="gpt-4-turbo">GPT-4 Turbo</option>
```

## Troubleshooting

### Common Issues

1. **API Connection Error**
   - Ensure the FastAPI backend is running on port 8000
   - Check that CORS is properly configured

2. **API Key Issues**
   - Verify your OpenAI API key is valid
   - Ensure you have sufficient credits in your OpenAI account

3. **Build Errors**
   - Run `npm install` to ensure all dependencies are installed
   - Check that you're using Node.js 18+

## Deployment

This frontend is optimized for Vercel deployment:

1. Connect your GitHub repository to Vercel
2. Set the build command to `npm run build`
3. Set the output directory to `.next`
4. Deploy!

## Contributing

1. Follow the existing code style and patterns
2. Maintain the earth tone color scheme
3. Ensure accessibility standards are met
4. Test on both desktop and mobile devices

## License

This project is part of The AI Engineer Challenge.