import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
import json
import os
import glob
from app.utils.logger import logger
from app.config import EXCEL_FILE_PATH, IMAGE_DATA_DIR, DATA_CACHE_FILE
from app.services.gemini_client import gemini_client


class KnowledgeBase:
    """Manages diamond knowledge base from Excel file"""
    
    def __init__(self):
        self.data: pd.DataFrame = None
        self.knowledge_text: str = ""
        self.load_data()
        self.load_image_data()
    
    def load_data(self) -> None:
        """Load and parse Excel data"""
        try:
            excel_path = Path(EXCEL_FILE_PATH)
            
            if not excel_path.exists():
                logger.error(f"Excel file not found: {excel_path}")
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
            # Read Excel file
            self.data = pd.read_excel(excel_path)
            logger.info(f"Loaded {len(self.data)} records from {excel_path}")
            
            # Convert to structured knowledge text
            self.knowledge_text = self._create_knowledge_text()
            logger.info("Knowledge base initialized successfully with Excel data")
            
        except Exception as e:
            logger.error(f"Error loading Excel data: {str(e)}")
            # Don't raise here, allow continuing with just image data if excel fails
            # raise 

    def load_image_data(self) -> None:
        """Load and process image data"""
        try:
            image_dir = Path(IMAGE_DATA_DIR)
            cache_file = Path(DATA_CACHE_FILE)
            
            if not image_dir.exists():
                logger.warning(f"Image directory not found: {image_dir}")
                return

            # Load cache
            cache = {}
            if cache_file.exists():
                try:
                    with open(cache_file, "r") as f:
                        cache = json.load(f)
                except Exception as e:
                    logger.error(f"Error loading cache: {e}")

            # Process images
            image_files = list(image_dir.glob("*.jpeg")) + list(image_dir.glob("*.jpg")) + list(image_dir.glob("*.png"))
            updates_made = False
            
            new_data_text = "\n\nIMAGE INVENTORY:\n"
            
            for img_path in image_files:
                filename = img_path.name
                if filename in cache:
                    logger.info(f"Using cached data for {filename}")
                    data = cache[filename]
                else:
                    logger.info(f"Analyzing image: {filename}")
                    from app.prompts import IMAGE_ANALYSIS_PROMPT
                    response_text = gemini_client.analyze_image(str(img_path), IMAGE_ANALYSIS_PROMPT)
                    
                    # Clean up response to get JSON
                    try:
                        # Find JSON part
                        start = response_text.find('{')
                        end = response_text.rfind('}') + 1
                        if start != -1 and end != -1:
                            json_str = response_text[start:end]
                            data = json.loads(json_str)
                            cache[filename] = data
                            updates_made = True
                        else:
                            logger.warning(f"Could not parse JSON from image analysis for {filename}")
                            data = {"description": response_text}
                    except Exception as e:
                         logger.error(f"Error parsing image analysis for {filename}: {e}")
                         data = {"description": response_text}

                # Format for context
                # Use a generic identifier to prevent the LLM from citing filenames unless necessary
                new_data_text += f"\nInventory Item (Source: {filename}):\n"
                for k, v in data.items():
                    new_data_text += f"  - {k}: {v}\n"

            # Update cache if needed
            if updates_made:
                cache_file.parent.mkdir(exist_ok=True)
                with open(cache_file, "w") as f:
                    json.dump(cache, f, indent=2)

            # Append to knowledge text
            self.knowledge_text += new_data_text
            logger.info(f"Processed {len(image_files)} images")

        except Exception as e:
            logger.error(f"Error loading image data: {str(e)}")
    
    def _create_knowledge_text(self) -> str:
        """Convert DataFrame to structured text for LLM context"""
        if self.data is None or self.data.empty:
            return "No diamond data available."
        
        knowledge_parts = ["DIAMOND INVENTORY:\n"]
        
        for idx, row in self.data.iterrows():
            diamond_info = f"\nDiamond #{idx + 1}:\n"
            for col in self.data.columns:
                value = row[col]
                # Handle NaN values
                if pd.isna(value):
                    value = "Not specified"
                diamond_info += f"  - {col}: {value}\n"
            knowledge_parts.append(diamond_info)
        
        return "".join(knowledge_parts)
    
    def get_knowledge_context(self) -> str:
        """Get formatted knowledge for LLM context"""
        return self.knowledge_text
    
    def search_diamonds(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search diamonds based on criteria (for future enhancements)"""
        if self.data is None:
            return []
        
        filtered_data = self.data.copy()
        
        for key, value in criteria.items():
            if key in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[key] == value]
        
        return filtered_data.to_dict('records')
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Get summary statistics of diamond inventory"""
        if self.data is None or self.data.empty:
            return {}
        
        stats = {
            "total_diamonds": len(self.data),
            "columns": list(self.data.columns)
        }
        
        # Add numeric column stats if available
        numeric_cols = self.data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            stats[f"{col}_range"] = {
                "min": float(self.data[col].min()),
                "max": float(self.data[col].max()),
                "avg": float(self.data[col].mean())
            }
        
        return stats


# Global instance
knowledge_base = KnowledgeBase()
