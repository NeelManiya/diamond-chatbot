from typing import Dict, List, Any
from collections import defaultdict
from app.utils.logger import logger


# In-memory chat history store (session_id -> list of messages)
_chat_store: Dict[str, List[Dict[str, str]]] = defaultdict(list)


def save_message(session_id: str, role: str, content: str):
    """Save a message to the in-memory chat history"""
    _chat_store[session_id].append({
        "role": role,
        "content": content,
    })
    logger.info(f"Message saved for session {session_id}")


def get_chat_history(session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get chat history for a session from memory"""
    history = _chat_store.get(session_id, [])
    # Return the most recent `limit` messages
    return history[-limit:]
