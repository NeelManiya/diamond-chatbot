import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import os

class GoogleSheetService:
    def __init__(self):
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        base_dir = os.path.dirname(os.path.dirname(__file__))
        creds_path = os.path.join(base_dir, "config", "service_account.json")

        creds = Credentials.from_service_account_file(creds_path, scopes=scope)
        client = gspread.authorize(creds)

        # 🔥 PASTE YOUR GOOGLE SHEET URL HERE
        sheet_url = "https://docs.google.com/spreadsheets/d/1WUvkwns5dRo8d4DcSxQjRUrZPPFRAGDIb4m3n2OiJF8/edit?usp=sharing"
        self.sheet = client.open_by_url(sheet_url).sheet1

    def get_all_data(self):
        data = self.sheet.get_all_records()
        df = pd.DataFrame(data)
        return df