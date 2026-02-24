import google.generativeai as genai
from typing import List, Dict, Any, Optional
from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.utils.logger import logger

import PIL.Image

class GeminiClient:
    """Wrapper for Google Gemini API"""
    
    def __init__(self):
        self.configure()
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def configure(self):
        """Configure Gemini API with key"""
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {str(e)}")
            raise

    def create_chat_session(self, history: List[Dict[str, str]] = None) -> Any:
        """Create a new chat session with history"""
        gemini_history = []
        if history:
            for message in history:
                role = "user" if message["role"] == "user" else "model"
                gemini_history.append({
                    "role": role,
                    "parts": [message["content"]]
                })
        
        return self.model.start_chat(history=gemini_history)

    def generate_response(self, 
                         messages: List[Dict[str, str]], 
                         system_prompt: str = "") -> str:
        """
        Generate response using Gemini
        
        Args:
            messages: List of message dictionaries {"role": "user/assistant", "content": "..."}
            system_prompt: Context/System instructions
        """
        try:
            # Prepare history (excluding the last new message)
            history_messages = messages[:-1]
            last_message_content = messages[-1]["content"]
            
            # Create chat session with history
            chat_session = self.create_chat_session(history_messages)
            
            # Construct the final prompt with system instructions if needed
            # Since system instructions are often better placed in the first message or context
            # We will prepend it to the current message if it's the start, or just send it with the message
            
            final_prompt = last_message_content
            if system_prompt:
                 # simple approach: prepend system prompt to the user message for context
                 # for more complex flows, we might want to maintain it in history or use new system_instruction param in beta
                 final_prompt = f"Context: {system_prompt}\n\nUser Question: {last_message_content}"

            response = chat_session.send_message(final_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return "I apologize, but I'm having trouble connecting to my knowledge base right now. Please try again later."

    def generate_content(self, prompt: str) -> str:
        """Simple generation for single prompt"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """Analyze an image and return extracted text/data"""
        try:
            img = PIL.Image.open(image_path)
            response = self.model.generate_content([prompt, img])
            return response.text
        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {str(e)}")
            return ""

# Global instance
gemini_client = GeminiClient()


def ask_gemini(prompt: str) -> str:
    """Simple helper to generate a response from a prompt"""
    return gemini_client.generate_content(prompt)
