import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from app.utils.logger import logger
from app.config import get_settings


class KnowledgeBase:
    """Manages diamond knowledge base from Excel file"""
    
    def __init__(self):
        self.settings = get_settings()
        self.data: pd.DataFrame = None
        self.knowledge_text: str = ""
        self.load_data()
    
    def load_data(self) -> None:
        """Load and parse Excel data"""
        try:
            excel_path = Path(self.settings.EXCEL_FILE_PATH)
            
            if not excel_path.exists():
                logger.error(f"Excel file not found: {excel_path}")
                raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
            # Read Excel file
            self.data = pd.read_excel(excel_path)
            logger.info(f"Loaded {len(self.data)} records from {excel_path}")
            
            # Convert to structured knowledge text
            self.knowledge_text = self._create_knowledge_text()
            logger.info("Knowledge base initialized successfully")
            
        except Exception as e:
            logger.error(f"Error loading Excel data: {str(e)}")
            raise
    
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
