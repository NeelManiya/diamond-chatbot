from typing import AsyncGenerator, List, Dict, Any

from app.services.knowledge_base import get_excel_context
from app.services.gemini_client import gemini_client
from app.prompts import format_chat_system_prompt
from app.utils.logger import logger

from google.genai import types
from app.config import GEMINI_MODEL


# ────────────────────────────────────────────────────────────────
# REST endpoint helper  (used by POST /chat)
# ────────────────────────────────────────────────────────────────
def get_chat_response(user_message: str) -> str:
    """Return a complete (non-streaming) response grounded in the knowledge base."""
    sheet_context = get_excel_context()
    system_prompt = format_chat_system_prompt(sheet_context)

    final_prompt = (
        f"{system_prompt}\n\n"
        f"User question:\n{user_message}\n\n"
        "Answer only from the provided data. "
        "If the answer is not available, say: 'Not available.'"
    )

    response = gemini_client.generate_content(final_prompt)
    return response


# ────────────────────────────────────────────────────────────────
# WebSocket streaming helper  (used by /ws)
# ────────────────────────────────────────────────────────────────
async def get_chat_response_stream(
    user_message: str,
    history: List[Dict[str, Any]] = None,
) -> AsyncGenerator[str, None]:
    """
    Async generator that yields text chunks from Gemini with streaming.
    The knowledge-base context + system instruction is prepended to the
    very first turn so every subsequent turn still benefits from it.
    """
    sheet_context = get_excel_context()
    system_prompt = format_chat_system_prompt(sheet_context)

    # Build the contents list  (history + current user message)
    contents = []

    # If this is the first turn, prepend the system context as a user/model
    # "primer" so Gemini always has the knowledge base in scope.
    if not history:
        contents.append({
            "role": "user",
            "parts": [{"text": system_prompt + "\n\nFor this session, answer only from the product data above."}]
        })
        contents.append({
            "role": "model",
            "parts": [{"text": "Understood! I'm ready to help with diamond queries based on the provided data."}]
        })
    else:
        # For subsequent turns, include existing history
        contents.extend(history)

    # Append the current user message
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Convert contents dicts to google.genai types
    genai_contents = [
        types.Content(
            role=msg["role"],
            parts=[types.Part(text=p["text"]) for p in msg["parts"]]
        )
        for msg in contents
    ]

    try:
        stream = gemini_client.client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=genai_contents,
        )

        for chunk in stream:
            if chunk.text:
                yield chunk.text

    except Exception as e:
        logger.error(f"Streaming error: {e}")
        yield f"Error: {str(e)}"