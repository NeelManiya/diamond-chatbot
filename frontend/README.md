# Diamond Chatbot - Frontend

WhatsApp-style React frontend for the diamond chatbot with beautiful UI and seamless API integration.

## Features

- 💬 **WhatsApp-Style UI** - Familiar and intuitive chat interface
- 🎨 **Premium Design** - Gradient backgrounds, smooth animations, glassmorphism
- 📱 **Fully Responsive** - Works perfectly on desktop, tablet, and mobile
- ⚡ **Real-time Updates** - Instant message delivery with typing indicators
- 🎯 **Auto-scroll** - Automatically scrolls to latest messages
- ✨ **Smooth Animations** - Message slide-ins, typing dots, and micro-interactions

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChatContainer.jsx    # Main chat component
│   │   ├── ChatHeader.jsx       # Header with bot info
│   │   ├── MessageList.jsx      # Message container
│   │   ├── Message.jsx          # Individual message bubble
│   │   ├── MessageInput.jsx     # Input field
│   │   └── TypingIndicator.jsx  # Animated typing dots
│   ├── services/
│   │   └── api.js               # API client
│   ├── styles/
│   │   └── chat.css             # WhatsApp-style CSS
│   ├── App.jsx                  # Main app component
│   └── main.jsx                 # React entry point
├── index.html                   # HTML template
├── package.json                 # Dependencies
└── vite.config.js               # Vite configuration
```

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm installed
- Backend server running on `http://localhost:8000`

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` if your backend is on a different URL:

```env
VITE_API_URL=http://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at: `http://localhost:5173`

### 4. Build for Production

```bash
npm run build
```

The production build will be in the `dist/` folder.

### 5. Preview Production Build

```bash
npm run preview
```

## Features Breakdown

### Chat Interface

- **Auto-greeting**: Bot automatically greets users when they start a conversation
- **Session Management**: Each user gets a unique session ID for conversation tracking
- **Message History**: All messages are displayed with timestamps
- **Typing Indicator**: Shows when the bot is processing a response
- **Error Handling**: Graceful error messages if backend is unavailable

### UI Components

1. **ChatHeader**: Displays bot avatar, name, and online status
2. **MessageList**: Scrollable container with auto-scroll to latest message
3. **Message**: Individual message bubbles with different styles for bot/user
4. **MessageInput**: Text input with send button and keyboard shortcuts
5. **TypingIndicator**: Animated dots showing bot is typing

### Styling Highlights

- **Gradient Backgrounds**: Purple gradient theme throughout
- **Message Bubbles**: WhatsApp-style bubbles with shadows
- **Smooth Animations**: Slide-in effects for messages
- **Glassmorphism**: Frosted glass effect on avatar
- **Responsive Design**: Adapts to all screen sizes
- **Custom Scrollbar**: Styled scrollbar for message list

## API Integration

The frontend communicates with the backend via REST API:

### Endpoints Used

- `POST /chat` - Send user message and receive bot response
- `GET /chat/greeting/{session_id}` - Get initial greeting message

### API Client

Located in `src/services/api.js`, provides:
- `sendMessage(message, sessionId)` - Send chat message
- `getGreeting(sessionId)` - Get greeting for new session
- `healthCheck()` - Check backend health

## Customization

### Change Colors

Edit `src/styles/chat.css`:

```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* User message bubble */
.user-message {
  background: linear-gradient(135deg, #your-color-1 0%, #your-color-2 100%);
}
```

### Change Bot Avatar

Edit `src/components/ChatHeader.jsx` and replace the SVG icon.

### Modify Message Bubble Style

Edit `.bot-message` and `.user-message` classes in `chat.css`.

## Keyboard Shortcuts

- **Enter**: Send message
- **Shift + Enter**: New line (not implemented, single line input)

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Troubleshooting

### Backend Connection Error

If you see "Failed to connect to the chatbot":
1. Ensure backend is running on `http://localhost:8000`
2. Check CORS settings in backend allow `http://localhost:5173`
3. Verify `.env` file has correct `VITE_API_URL`

### Styling Issues

If styles don't load:
1. Clear browser cache
2. Restart dev server
3. Check browser console for errors

### Build Errors

If build fails:
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again
3. Ensure Node.js version is 18+

## Production Deployment

### Static Hosting (Netlify, Vercel, etc.)

1. Build the project: `npm run build`
2. Upload `dist/` folder to your hosting provider
3. Set environment variable: `VITE_API_URL=https://your-backend-url.com`

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
```

Build and run:

```bash
docker build -t diamond-chatbot-frontend .
docker run -p 3000:3000 diamond-chatbot-frontend
```

## Notes

- Session IDs are generated client-side using timestamp + random string
- Messages are stored in component state (not persisted)
- For production, consider adding message persistence
- The UI is optimized for modern browsers with CSS Grid and Flexbox
