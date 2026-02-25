from app.utils.logger import logger

# ─── Lazy singleton ────────────────────────────────────────────────────────────
# GoogleSheetService is initialised only the FIRST time get_excel_context() is
# called, not at module import time.  This prevents a startup crash when the
# service-account.json file is temporarily absent.
_sheet_service = None

def _get_sheet_service():
    global _sheet_service
    if _sheet_service is None:
        from app.services.google_sheet_service import GoogleSheetService
        _sheet_service = GoogleSheetService()
        logger.info("GoogleSheetService initialised successfully")
    return _sheet_service


def get_excel_context() -> str:
    """Return all sheet rows as a single text block for the prompt context."""
    try:
        service = _get_sheet_service()
        df = service.get_all_data()

        if df.empty:
            return "No data available in knowledge base."

        lines = []
        for _, row in df.iterrows():
            row_text = " | ".join(f"{col}: {row[col]}" for col in df.columns)
            lines.append(row_text)

        return "\n".join(lines)

    except Exception as e:
        logger.error(f"Failed to load knowledge base: {e}")
        return "Knowledge base temporarily unavailable."