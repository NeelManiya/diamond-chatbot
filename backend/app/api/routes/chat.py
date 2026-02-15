from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service
from app.utils.logger import logger

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat endpoint for diamond chatbot
    
    - **message**: User's message
    - **session_id**: Unique session identifier for conversation tracking
    """
    try:
        logger.info(f"Received chat request from session: {request.session_id}")
        
        # Process message and get response
        bot_response = chat_service.process_message(
            session_id=request.session_id,
            user_message=request.message
        )
        
        return ChatResponse(
            message=bot_response,
            session_id=request.session_id
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )


@router.get("/greeting/{session_id}", response_model=ChatResponse)
async def get_greeting(session_id: str) -> ChatResponse:
    """
    Get greeting message for a new session
    
    - **session_id**: Unique session identifier
    """
    try:
        logger.info(f"Getting greeting for session: {session_id}")
        
        greeting_message = chat_service.get_greeting(session_id)
        
        return ChatResponse(
            message=greeting_message,
            session_id=session_id
        )
        
    except Exception as e:
        logger.error(f"Error getting greeting: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting greeting: {str(e)}"
        )
