from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS
from app.api.routes import chat, insight

# ... other imports ...

# Include routers
# ... other imports ...

from app.utils.logger import logger


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Diamond chatbot API with knowledge-based responses"
)

@app.get("/")
def read_root():
    return {
        "message": "Diamond Chatbot API",
        "version": APP_VERSION,
        "status": "running"
    }

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(insight.router)
