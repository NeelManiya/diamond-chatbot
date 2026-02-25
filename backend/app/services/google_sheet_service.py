import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from app.utils.logger import logger

class GoogleSheetService:
    def __init__(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Allow override via env var, otherwise default to app/config/service_account.json
        creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
        if not creds_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            creds_path = os.path.join(base_dir, "config", "service_account.json")

        if not os.path.exists(creds_path):
            raise FileNotFoundError(
                f"Google service account credentials not found at: {creds_path}\n"
                "Please place your service_account.json at that path, or set the "
                "GOOGLE_SERVICE_ACCOUNT_PATH environment variable."
            )

        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)

        sheet_url = os.getenv(
            "GOOGLE_SHEET_URL",
            "https://docs.google.com/spreadsheets/d/1WUvkwns5dRo8d4DcSxQjRUrZPPFRAGDIb4m3n2OiJF8/edit?usp=sharing"
        )
        self.sheet = client.open_by_url(sheet_url).sheet1
        logger.info(f"Connected to Google Sheet: {sheet_url[:60]}...")

    def get_all_data(self) -> pd.DataFrame:
        data = self.sheet.get_all_records()
        return pd.DataFrame(data)
