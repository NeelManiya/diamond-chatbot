"""
Chat repository — CRUD operations for conversations & messages in Supabase.

Supabase tables required (run the SQL in README / migrations):

    conversations
        id          uuid  PRIMARY KEY DEFAULT gen_random_uuid()
        session_id  text  NOT NULL UNIQUE
        started_at  timestamptz NOT NULL DEFAULT now()
        updated_at  timestamptz NOT NULL DEFAULT now()

    messages
        id              uuid  PRIMARY KEY DEFAULT gen_random_uuid()
        conversation_id uuid  NOT NULL REFERENCES conversations(id) ON DELETE CASCADE
        role            text  NOT NULL  -- 'user' | 'model'
        content         text  NOT NULL
        created_at      timestamptz NOT NULL DEFAULT now()
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from app.db.supabase_client import get_supabase
from app.utils.logger import logger


# ──────────────────────────────────────────────────────────────────────────────
# Conversations
# ──────────────────────────────────────────────────────────────────────────────

def get_or_create_conversation(session_id: str) -> dict[str, Any]:
    """
    Return the existing conversation row for *session_id*, or insert a new one.
    Always returns the full row dict.
    """
    db = get_supabase()

    # Try to fetch existing
    result = (
        db.table("conversations")
        .select("*")
        .eq("session_id", session_id)
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    # Create new conversation
    now = datetime.now(timezone.utc).isoformat()
    insert_result = (
        db.table("conversations")
        .insert({"session_id": session_id, "started_at": now, "updated_at": now})
        .execute()
    )

    row = insert_result.data[0]
    logger.info(f"New conversation created: session_id={session_id}, id={row['id']}")
    return row


def touch_conversation(conversation_id: str) -> None:
    """Update the updated_at timestamp on a conversation."""
    db = get_supabase()
    db.table("conversations").update(
        {"updated_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", conversation_id).execute()


def list_conversations(limit: int = 50) -> list[dict[str, Any]]:
    """Return the most recent conversations, newest first."""
    db = get_supabase()
    result = (
        db.table("conversations")
        .select("*")
        .order("updated_at", desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


def delete_conversation(session_id: str) -> bool:
    """Delete a conversation (and all its messages via CASCADE). Returns True if deleted."""
    db = get_supabase()
    result = (
        db.table("conversations")
        .delete()
        .eq("session_id", session_id)
        .execute()
    )
    deleted = bool(result.data)
    if deleted:
        logger.info(f"Conversation deleted: session_id={session_id}")
    return deleted


# ──────────────────────────────────────────────────────────────────────────────
# Messages
# ──────────────────────────────────────────────────────────────────────────────

def save_message(
    conversation_id: str,
    role: str,
    content: str,
) -> dict[str, Any]:
    """
    Persist a single message and return the inserted row.

    Args:
        conversation_id: UUID of the parent conversation.
        role: 'user' or 'model'.
        content: The message text.
    """
    db = get_supabase()
    now = datetime.now(timezone.utc).isoformat()
    result = (
        db.table("messages")
        .insert(
            {
                "conversation_id": conversation_id,
                "role": role,
                "content": content,
                "created_at": now,
            }
        )
        .execute()
    )
    return result.data[0]


def save_turn(
    session_id: str,
    user_message: str,
    bot_response: str,
) -> None:
    """
    Convenience helper: get/create conversation, save both user and bot messages,
    and update the conversation's updated_at timestamp — all in one call.
    """
    try:
        conv = get_or_create_conversation(session_id)
        conv_id = conv["id"]
        save_message(conv_id, "user", user_message)
        save_message(conv_id, "model", bot_response)
        touch_conversation(conv_id)
        logger.debug(f"Turn saved for session={session_id}")
    except Exception as exc:
        # Never let DB errors break the chat response
        logger.error(f"[chat_repo] Failed to save turn for session={session_id}: {exc}")


def get_messages(session_id: str, limit: int = 100) -> list[dict[str, Any]]:
    """
    Return all messages for a given session_id, ordered oldest → newest.
    """
    db = get_supabase()

    # Look up the conversation
    conv_result = (
        db.table("conversations")
        .select("id")
        .eq("session_id", session_id)
        .limit(1)
        .execute()
    )
    if not conv_result.data:
        return []

    conv_id = conv_result.data[0]["id"]

    msg_result = (
        db.table("messages")
        .select("*")
        .eq("conversation_id", conv_id)
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )
    return msg_result.data or []
