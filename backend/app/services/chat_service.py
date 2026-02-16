from typing import Dict, List
from app.services.knowledge_base import knowledge_base
from app.services.gemini_client import gemini_client
from app.database import save_message, get_chat_history as db_get_chat_history
from app.utils.logger import logger


class ChatService:
    """Manages chat sessions and conversation history"""
    
    def __init__(self):
        # System prompt is now just text context for Gemini
        self.system_prompt = knowledge_base.get_knowledge_context()
    
    def get_or_create_session(self, session_id: str) -> List[Dict[str, str]]:
        """Get existing session or create new one with greeting"""
        history = self.get_chat_history(session_id)
        
        if not history:
            logger.info(f"Creating new session: {session_id}")
            # Generate greeting for new session
            greeting = self._generate_greeting()
            self.add_message(session_id, "assistant", greeting)
            return self.get_chat_history(session_id)
        
        return history
    
    def _generate_greeting(self) -> str:
        """Generate initial greeting message"""
        try:
            greeting_messages = [{
                "role": "user",
                "content": "Please greet me as a new customer visiting your diamond store."
            }]
            
            # specific instructions for the chat flow
            from app.prompts import format_chat_system_prompt
            system_instruction = format_chat_system_prompt(self.system_prompt)

            greeting = gemini_client.generate_response(
                messages=greeting_messages,
                system_prompt=system_instruction
            )
            
            return greeting
            
        except Exception as e:
            logger.error(f"Error generating greeting: {str(e)}")
            # Fallback greeting
            return "Hello! Welcome to our diamond store. I'm here to help you find the perfect diamond. How can I assist you today?"
    
    def add_message(self, session_id: str, role: str, content: str) -> None:
        """Add message to session history"""
        save_message(session_id, role, content)
    
    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for session"""
        # Retrieve history from DB, removing timestamp/id if needed to match expected format
        db_history = db_get_chat_history(session_id)
        # Convert to format expected by Gemini client (role, content)
        return [{"role": msg["role"], "content": msg["content"]} for msg in db_history]
    
    def process_message(self, session_id: str, user_message: str) -> str:
        """Process user message and generate response"""
        try:
            # Ensure session exists (creates greeting if new)
            self.get_or_create_session(session_id)
            
            # Add user message to history
            self.add_message(session_id, "user", user_message)
            
            # Get updated history for API call
            current_history = self.get_chat_history(session_id)
            
            # specific instructions for the chat flow
            from app.prompts import format_chat_system_prompt
            system_instruction = format_chat_system_prompt(self.system_prompt)

            # Generate response
            assistant_response = gemini_client.generate_response(
                messages=current_history,
                system_prompt=system_instruction
            )
            
            # Add assistant response to history
            self.add_message(session_id, "assistant", assistant_response)
            
            logger.info(f"Processed message for session {session_id}")
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise
    
    def get_greeting(self, session_id: str) -> str:
        """Get greeting message for a session"""
        session_history = self.get_or_create_session(session_id)
        # Return the first assistant message (greeting)
        for msg in session_history:
            if msg["role"] == "assistant":
                return msg["content"]
        return "Hello! How can I help you today?"


# Global instance
chat_service = ChatService()
