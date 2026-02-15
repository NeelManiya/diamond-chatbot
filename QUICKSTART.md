# 🚀 Quick Setup Guide

## Prerequisites
- Python 3.8+ installed
- Node.js 18+ and npm installed
- OpenAI API key

## Backend Setup (5 minutes)

1. **Navigate to backend**:
   ```bash
   cd backend
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   ```

4. **Edit `.env` and add your OpenAI API key**:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

5. **Generate sample diamond data**:
   ```bash
   python create_sample_data.py
   ```

6. **Start the backend server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   ✅ Backend running at: http://localhost:8000
   📚 API docs at: http://localhost:8000/docs

## Frontend Setup (5 minutes)

1. **Open a new terminal and navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   ```
   (Default settings should work if backend is on localhost:8000)

4. **Start the frontend dev server**:
   ```bash
   npm run dev
   ```

   ✅ Frontend running at: http://localhost:5173

## Test the Chatbot

1. Open browser to http://localhost:5173
2. You should see a WhatsApp-style chat interface
3. The bot will greet you automatically
4. Try asking:
   - "What diamonds do you have?"
   - "Show me diamonds under $10,000"
   - "Do you have any round cut diamonds?"

## Troubleshooting

**Backend won't start?**
- Make sure Python 3.8+ is installed: `python --version`
- Check if all dependencies installed: `pip list`
- Verify OpenAI API key is set in `.env`

**Frontend won't start?**
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if backend is running on port 8000

**Can't connect to chatbot?**
- Ensure backend is running (check http://localhost:8000/health)
- Check browser console for errors
- Verify CORS settings in backend allow localhost:5173

## Next Steps

- Customize the Excel file with your own diamond data
- Modify the UI colors in `frontend/src/styles/chat.css`
- Deploy to production (see main README.md)

---

For detailed documentation, see:
- Main README: `README.md`
- Backend docs: `backend/README.md`
- Frontend docs: `frontend/README.md`
