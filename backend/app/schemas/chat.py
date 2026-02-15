from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """Request schema for chat endpoint"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    session_id: str = Field(..., min_length=1, description="Unique session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What diamonds do you have available?",
                "session_id": "user_123_session"
            }
        }


class ChatResponse(BaseModel):
    """Response schema for chat endpoint"""
    message: str = Field(..., description="Bot response message")
    session_id: str = Field(..., description="Session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "We have a variety of diamonds available. Could you tell me what you're looking for?",
                "session_id": "user_123_session"
            }
        }
