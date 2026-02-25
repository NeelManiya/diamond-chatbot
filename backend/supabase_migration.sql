-- ============================================================
-- Diamond Chatbot – Supabase Migration
-- Run this in the Supabase SQL Editor (or psql)
-- ============================================================

-- 1. Conversations table
--    One row per user session (identified by session_id string)
CREATE TABLE IF NOT EXISTS conversations (
    id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  TEXT        NOT NULL UNIQUE,
    started_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for fast look-up by session_id
CREATE INDEX IF NOT EXISTS idx_conversations_session_id
    ON conversations (session_id);

-- Index for ordering by most-recent activity
CREATE INDEX IF NOT EXISTS idx_conversations_updated_at
    ON conversations (updated_at DESC);


-- 2. Messages table
--    One row per message in a conversation
CREATE TABLE IF NOT EXISTS messages (
    id              UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID        NOT NULL
                                REFERENCES conversations (id)
                                ON DELETE CASCADE,
    role            TEXT        NOT NULL CHECK (role IN ('user', 'model')),
    content         TEXT        NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Index for fetching all messages of a conversation quickly
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
    ON messages (conversation_id, created_at ASC);


-- ============================================================
-- Optional: Row-Level Security (RLS)
-- Enable if you want per-user data isolation via Supabase Auth
-- ============================================================
-- ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
