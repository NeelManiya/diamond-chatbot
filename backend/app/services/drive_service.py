import gdown
import os

class DriveService:

    def __init__(self):
        self.file_id = os.getenv("DRIVE_FILE_ID")
        self.output = "app/data/diamonds.xlsx"

    def download_excel(self):
        if not self.file_id:
            raise ValueError("DRIVE_FILE_ID missing in .env")

        url = f"https://drive.google.com/uc?id={self.file_id}"

        print("Downloading latest Excel from Google Drive...")
        gdown.download(url, self.output, quiet=False, fuzzy=True)
        print("Excel ready")