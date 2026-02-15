import pandas as pd
from pathlib import Path

# Sample diamond data
diamonds_data = {
    "diamond_id": ["D001", "D002", "D003", "D004", "D005", "D006", "D007", "D008", "D009", "D010"],
    "carat": [0.5, 1.0, 1.5, 2.0, 0.75, 1.25, 0.9, 1.8, 2.5, 1.1],
    "cut": ["Ideal", "Premium", "Very Good", "Ideal", "Good", "Ideal", "Premium", "Ideal", "Premium", "Very Good"],
    "color": ["D", "E", "F", "D", "G", "E", "F", "D", "E", "F"],
    "clarity": ["VVS1", "VVS2", "VS1", "IF", "VS2", "VVS1", "VS1", "IF", "VVS2", "VS1"],
    "price_usd": [2500, 5800, 9200, 15000, 3200, 7500, 4100, 12500, 22000, 6300],
    "shape": ["Round", "Round", "Princess", "Round", "Cushion", "Round", "Oval", "Round", "Emerald", "Princess"],
    "certification": ["GIA", "GIA", "AGS", "GIA", "IGI", "GIA", "GIA", "GIA", "AGS", "GIA"],
    "availability": ["In Stock", "In Stock", "Reserved", "In Stock", "In Stock", "In Stock", "Reserved", "In Stock", "In Stock", "In Stock"]
}

# Create DataFrame
df = pd.DataFrame(diamonds_data)

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Save to Excel
output_path = data_dir / "diamonds.xlsx"
df.to_excel(output_path, index=False, engine='openpyxl')

print(f"Sample diamond data created at: {output_path}")
print(f"Total diamonds: {len(df)}")
print("\nFirst few records:")
print(df.head())
