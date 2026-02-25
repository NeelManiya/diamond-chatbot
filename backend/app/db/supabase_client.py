"""
Singleton Supabase client.
Reads SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY from environment.
"""
import os
from supabase import create_client, Client
from app.utils.logger import logger

_supabase_client: Client | None = None


def get_supabase() -> Client:
    """Return (and lazily create) the global Supabase client."""
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    url = os.getenv("SUPABASE_URL", "").strip()
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env "
            "to use Supabase features."
        )

    _supabase_client = create_client(url, key)
    logger.info("Supabase client initialised successfully.")
    return _supabase_client
