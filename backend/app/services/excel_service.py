import pandas as pd
import numpy as np
import faiss
import google.generativeai as genai
import os
from app.services.drive_service import DriveService

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class ExcelAIService:

    def __init__(self):
        self.file_path = "app/data/diamonds.xlsx"
        self.text_rows = []
        self.index = None

        # download latest file
        DriveService().download_excel()

        # load + build search
        self.load_excel()
        self.create_embeddings()

    def load_excel(self):
        df = pd.read_excel(self.file_path)

        df["combined"] = (
            "Shape: " + df["Shape"].astype(str) +
            ", Size: " + df["MM (Size)"].astype(str) +
            ", Pointer: " + df["Pointer"].astype(str) +
            ", Price: " + df["Price per CT (USD)"].astype(str)
        )

        self.text_rows = df["combined"].tolist()
        print(f"Loaded {len(self.text_rows)} diamond rows")

    def embed(self, text):
        res = genai.embed_content(
            model="models/embedding-001",
            content=text
        )
        return res["embedding"]

    def create_embeddings(self):
        print("Creating embeddings...")

        embeddings = [self.embed(row) for row in self.text_rows]

        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings).astype("float32"))

        print("Search index ready")

    def search(self, query, k=5):
        q_emb = self.embed(query)
        D, I = self.index.search(np.array([q_emb]).astype("float32"), k)

        return [self.text_rows[i] for i in I[0]]    