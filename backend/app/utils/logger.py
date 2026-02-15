import logging
import sys
from pathlib import Path

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create logger
logger = logging.getLogger("diamond_chatbot")
logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
console_handler.setFormatter(console_formatter)

# File handler
file_handler = logging.FileHandler(log_dir / "app.log")
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
file_handler.setFormatter(file_formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)
