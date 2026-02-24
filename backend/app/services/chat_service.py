from app.services.knowledge_base import get_excel_context
from app.services.gemini_client import gemini_client

def get_chat_response(user_message: str):

    sheet_context = get_excel_context()

    final_prompt = f"""
                    You are a diamond assistant chatbot.

                    Here is product database:
                    {sheet_context}

                    User question:
                    {user_message}

                    Answer only from provided data.
                    If not found say: Not available.
                    """

    response = gemini_client.generate_content(final_prompt)
    return response