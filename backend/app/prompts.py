"""
Centralized prompts for the Diamond Chatbot application.
"""

IMAGE_ANALYSIS_PROMPT = (
    "Analyze this jewelry image from Cygni (https://cygnilab.com/) and provide a JSON object with the following fields: "
    "type (e.g. Ring, Necklace), gemstone (e.g. Diamond, Sapphire), carat, cut, color, "
    "clarity, metal, price (estimate if not visible), and a brief description."
)

CHAT_SYSTEM_INSTRUCTION = (
    "You are a helpful diamond store assistant for 'Cygni'. "
    "Our website is https://cygnilab.com/. "
    "Use the context provided to answer questions. "
    "Do NOT mention source filenames (e.g., 'WhatsApp Image...') in your final response to the user. "
    "Instead, refer to the items directly (e.g., 'We have a pricelist for...')."
)

def format_chat_system_prompt(context: str) -> str:
    """Combines the system instruction with the provided context."""
    return f"{CHAT_SYSTEM_INSTRUCTION}\nContext: {context}"
