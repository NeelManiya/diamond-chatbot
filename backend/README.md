# Diamond Chatbot - Backend

Production-ready FastAPI backend for the diamond chatbot with OpenAI integration and Excel-based knowledge base.

## Features

- 🤖 **OpenAI Integration** - GPT-4 Turbo powered responses
- 📊 **Excel Knowledge Base** - Diamond inventory from Excel file
- 💬 **Session Management** - Maintains conversation context
- 🎯 **Knowledge-Based Responses** - Answers strictly from Excel data
- 🚀 **Production Ready** - Proper logging, error handling, and CORS
- 📝 **API Documentation** - Auto-generated Swagger/OpenAPI docs

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py          # Chat endpoints
│   ├── schemas/
│   │   └── chat.py              # Pydantic models
│   ├── services/
│   │   ├── knowledge_base.py    # Excel data loader
│   │   ├── openai_client.py     # OpenAI API wrapper
│   │   └── chat_service.py      # Chat orchestration
│   ├── utils/
│   │   └── logger.py            # Logging configuration
│   ├── config.py                # Settings management
│   └── main.py                  # FastAPI app
├── data/
│   └── diamonds.xlsx            # Diamond inventory
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables
```

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

### 3. Generate Sample Data (Optional)

If you don't have a diamond Excel file, generate sample data:

```bash
python create_sample_data.py
```

Or provide your own `data/diamonds.xlsx` file.

### 4. Run the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Endpoints

### POST /chat

Send a message to the chatbot.

**Request:**
```json
{
  "message": "What diamonds do you have?",
  "session_id": "user_123"
}
```

**Response:**
```json
{
  "message": "We have 10 beautiful diamonds in our inventory...",
  "session_id": "user_123",
  "timestamp": "2026-02-10T05:13:52Z"
}
```

### GET /chat/greeting/{session_id}

Get the greeting message for a session.

**Response:**
```json
{
  "message": "Hello! Welcome to our diamond store...",
  "session_id": "user_123",
  "timestamp": "2026-02-10T05:13:52Z"
}
```

### GET /docs

Interactive API documentation (Swagger UI)

### GET /health

Health check endpoint

## Excel File Format

The Excel file should contain diamond inventory data. Example columns:

| diamond_id | carat | cut      | color | clarity | price_usd | shape    | certification | availability |
|------------|-------|----------|-------|---------|-----------|----------|---------------|--------------|
| D001       | 0.5   | Ideal    | D     | VVS1    | 2500      | Round    | GIA           | In Stock     |
| D002       | 1.0   | Premium  | E     | VVS2    | 5800      | Round    | GIA           | In Stock     |

You can customize the columns based on your needs. The knowledge base will automatically parse all columns.

## Configuration

All settings are managed in `app/config.py` and can be overridden via environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: gpt-4-turbo-preview)
- `EXCEL_FILE_PATH` - Path to Excel file (default: data/diamonds.xlsx)
- `MAX_CHAT_HISTORY` - Number of messages to keep in context (default: 10)
- `CORS_ORIGINS` - Allowed CORS origins for frontend

## Production Deployment

### Using Uvicorn

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn + Uvicorn

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Environment Variables for Production

```env
OPENAI_API_KEY=your_production_key
OPENAI_MODEL=gpt-4-turbo-preview
EXCEL_FILE_PATH=/app/data/diamonds.xlsx
CORS_ORIGINS=https://yourdomain.com
```

## Testing

Test the chat endpoint:

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me diamonds under $10000", "session_id": "test_session"}'
```

## Logging

Logs are written to:
- Console (stdout)
- `logs/app.log` file

Log format: `YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message`

## Notes

- Session data is stored in-memory. For production, use Redis or a database.
- The chatbot will ONLY answer based on the Excel data provided.
- First message in each session automatically includes a greeting.
- Chat history is maintained for natural conversations.
