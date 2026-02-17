from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS
from app.routes import chat

from app.utils.logger import logger


# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Diamond chatbot API with knowledge-based responses"
)


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
