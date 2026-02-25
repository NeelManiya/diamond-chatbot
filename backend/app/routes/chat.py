from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import get_chat_response
from app.utils.logger import logger
from app.config import ENABLE_CONVERSATION_STORAGE

if ENABLE_CONVERSATION_STORAGE:
    from app.db.repositories.chat_repo import save_turn, get_messages

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for diamond chatbot.

    - **message**: User's message
    - **session_id**: Unique session identifier for conversation tracking
    """
    try:
        logger.info(f"Received chat request from session: {request.session_id}")

        # Generate bot response
        bot_response = get_chat_response(user_message=request.message)

        # Persist the turn to Supabase (non-blocking — errors are caught inside)
        if ENABLE_CONVERSATION_STORAGE:
            save_turn(
                session_id=request.session_id,
                user_message=request.message,
                bot_response=bot_response,
            )

        return ChatResponse(
            message=bot_response,
            session_id=request.session_id,
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}",
        )


@router.get("/{session_id}/history")
async def get_history(session_id: str, limit: int = 100):
    """
    Retrieve the full message history for a session.
    Returns an empty list if Supabase is not configured.
    """
    if not ENABLE_CONVERSATION_STORAGE:
        return {"session_id": session_id, "messages": [], "warning": "Supabase not configured."}

    try:
        messages = get_messages(session_id=session_id, limit=limit)
        return {"session_id": session_id, "messages": messages}
    except Exception as e:
        logger.error(f"Error fetching history for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
