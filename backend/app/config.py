import os
from dotenv import load_dotenv

load_dotenv()

# ── Gemini ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# ── Application ───────────────────────────────────────────────────────────────
APP_NAME = os.getenv("APP_NAME", "Diamond Chatbot")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

# ── Data sources ──────────────────────────────────────────────────────────────
EXCEL_FILE_PATH = os.getenv("EXCEL_FILE_PATH", "data/diamonds.xlsx")

# ── CORS ──────────────────────────────────────────────────────────────────────
cors_env = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ORIGINS = cors_env.split(",") if cors_env else []

# ── Supabase ──────────────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")

# Whether to persist conversations to Supabase (disabled if credentials missing)
ENABLE_CONVERSATION_STORAGE = bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)
