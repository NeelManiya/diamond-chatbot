# Diamond Chatbot

A production-ready chatbot system for diamond-related queries with FastAPI backend and WhatsApp-style React frontend.

## 🌟 Features

### Backend
- 🤖 **OpenAI GPT-4 Integration** - Intelligent, context-aware responses
- 📊 **Excel Knowledge Base** - Easy-to-update diamond inventory
- 💬 **Session Management** - Maintains conversation context
- 🎯 **Knowledge-Based Responses** - Strictly answers from provided data
- 🚀 **Production Ready** - Logging, error handling, CORS configured
- 📝 **Auto-generated API Docs** - Swagger/OpenAPI documentation

### Frontend
- 💬 **WhatsApp-Style UI** - Familiar and intuitive interface
- 🎨 **Premium Design** - Gradients, animations, glassmorphism
- 📱 **Fully Responsive** - Works on all devices
- ⚡ **Real-time Updates** - Typing indicators and instant messaging
- ✨ **Smooth Animations** - Professional micro-interactions

## 📁 Project Structure

```
Diamond-chatbot/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/routes/        # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── schemas/           # Pydantic models
│   │   ├── utils/             # Utilities
│   │   ├── config.py          # Configuration
│   │   └── main.py            # FastAPI app
│   ├── data/
│   │   └── diamonds.xlsx      # Diamond inventory
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── styles/            # CSS styles
│   ├── package.json
│   └── README.md
│
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

4. **Generate sample data** (optional)
   ```bash
   python create_sample_data.py
   ```

5. **Run the server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: `http://localhost:8000`
   API docs at: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   The default configuration should work if backend is on `localhost:8000`

4. **Run development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: `http://localhost:5173`

## 📊 Excel Data Format

The chatbot reads diamond inventory from an Excel file. Example structure:

| diamond_id | carat | cut      | color | clarity | price_usd | shape    | certification | availability |
|------------|-------|----------|-------|---------|-----------|----------|---------------|--------------|
| D001       | 0.5   | Ideal    | D     | VVS1    | 2500      | Round    | GIA           | In Stock     |
| D002       | 1.0   | Premium  | E     | VVS2    | 5800      | Round    | GIA           | In Stock     |

You can customize columns based on your needs. The system automatically parses all columns.

## 🎯 Usage

1. **Start both backend and frontend servers**
2. **Open browser** to `http://localhost:5173`
3. **Chat with the bot** - It will greet you automatically
4. **Ask questions** about diamonds in the inventory
5. **Get accurate responses** based only on the Excel data

### Example Queries

- "What diamonds do you have?"
- "Show me diamonds under $10,000"
- "Do you have any round cut diamonds?"
- "What's the price of diamond D001?"
- "Tell me about diamonds with VVS1 clarity"

## 🔧 Configuration

### Backend Configuration

Edit `backend/.env`:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4-turbo-preview    # or gpt-3.5-turbo for cost savings
EXCEL_FILE_PATH=data/diamonds.xlsx
MAX_CHAT_HISTORY=10
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend Configuration

Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 🌐 Production Deployment

### Backend Deployment

**Using Gunicorn:**
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Environment variables for production:**
- Set `OPENAI_API_KEY` to your production key
- Update `CORS_ORIGINS` to your frontend domain
- Update `EXCEL_FILE_PATH` to absolute path

### Frontend Deployment

**Build for production:**
```bash
cd frontend
npm run build
```

**Deploy `dist/` folder to:**
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

**Set environment variable:**
```env
VITE_API_URL=https://your-backend-domain.com
```

## 📝 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /chat` - Send message to chatbot
- `GET /chat/greeting/{session_id}` - Get greeting message
- `GET /health` - Health check
- `GET /` - API info

## 🎨 Customization

### Change UI Colors

Edit `frontend/src/styles/chat.css`:

```css
/* Main gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Modify System Prompt

Edit `backend/app/services/openai_client.py` in the `create_system_prompt` method.

### Add More Diamond Data

Simply update `backend/data/diamonds.xlsx` with your inventory. The system will automatically load it on startup.

## 🐛 Troubleshooting

### Backend Issues

**"Excel file not found"**
- Run `python create_sample_data.py` to generate sample data
- Or provide your own `data/diamonds.xlsx` file

**"OpenAI API error"**
- Check your API key in `.env`
- Ensure you have credits in your OpenAI account
- Verify the model name is correct

### Frontend Issues

**"Failed to connect to chatbot"**
- Ensure backend is running on `http://localhost:8000`
- Check CORS settings in backend
- Verify `VITE_API_URL` in frontend `.env`

**Styling not loading**
- Clear browser cache
- Restart dev server
- Check browser console for errors

## 📦 Dependencies

### Backend
- FastAPI - Web framework
- OpenAI - LLM integration
- Pandas - Excel processing
- Pydantic - Data validation
- Uvicorn - ASGI server

### Frontend
- React - UI library
- Vite - Build tool
- Axios - HTTP client

## 🔒 Security Notes

- Never commit `.env` files to version control
- Keep OpenAI API keys secure
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting for production APIs

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Support

For issues or questions:
1. Check the README files in `backend/` and `frontend/`
2. Review API documentation at `/docs`
3. Check browser console and server logs for errors

## 🎉 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI for the excellent web framework
- React team for the UI library
- WhatsApp for UI inspiration
