import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Load env before importing app modules
load_dotenv()

from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, ENABLE_CONVERSATION_STORAGE
from app.routes import chat as chat_router
from app.utils.logger import logger
from app.services.chat_service import get_chat_response_stream

if ENABLE_CONVERSATION_STORAGE:
    from app.db.repositories.chat_repo import save_turn

# ─────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Diamond chatbot API with knowledge-based responses and real-time streaming",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jinja2 templates – serve the chat UI
templates = Jinja2Templates(directory="templates")

# Include REST API router  (POST /chat)
app.include_router(chat_router.router)


# ─────────────────────────────────────────────
# UI route
# ─────────────────────────────────────────────
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ─────────────────────────────────────────────
# WebSocket – streaming chat with knowledge base
# ─────────────────────────────────────────────
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected")

    # Each WS connection gets its own session_id.
    # The client can pass ?session_id=xxx in the query string; otherwise we
    # generate one from the client's host+port.
    session_id = (
        websocket.query_params.get("session_id")
        or f"ws_{websocket.client.host}_{websocket.client.port}"
    )
    logger.info(f"WS session_id: {session_id}")

    # Conversation history stored per-connection (in-memory for streaming context)
    history = []

    try:
        while True:
            user_message = await websocket.receive_text()
            logger.info(f"WS received: {user_message[:80]}")

            # Append user turn to history
            history.append({
                "role": "user",
                "parts": [{"text": user_message}]
            })

            try:
                full_response = ""

                # Stream chunks from the real knowledge-base-aware service
                async for chunk in get_chat_response_stream(user_message, history[:-1]):
                    if chunk:
                        full_response += chunk
                        await websocket.send_text(chunk)

                # Append model turn to history for multi-turn context
                history.append({
                    "role": "model",
                    "parts": [{"text": full_response}]
                })

                # ── Persist turn to Supabase ──────────────────────────────────
                if ENABLE_CONVERSATION_STORAGE:
                    save_turn(
                        session_id=session_id,
                        user_message=user_message,
                        bot_response=full_response,
                    )

                # Signal end-of-stream to the client
                await websocket.send_text("[DONE]")

            except Exception as e:
                logger.error(f"Error generating WebSocket response: {e}")
                await websocket.send_text(f"Error: {str(e)}")
                await websocket.send_text("[DONE]")

    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected: session_id={session_id}")


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)