from app.services.google_sheet_service import GoogleSheetService

sheet_service = GoogleSheetService()

def get_excel_context():

    df = sheet_service.get_all_data()

    if df.empty:
        return "No data available in knowledge base."

    context = ""

    for _, row in df.iterrows():
        row_text = " | ".join([f"{col}: {row[col]}" for col in df.columns])
        context += row_text + "\n"

    return context