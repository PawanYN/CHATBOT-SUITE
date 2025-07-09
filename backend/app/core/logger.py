import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE="log/app.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Basic logger setup
logger = logging.getLogger("chatbot")
logger.setLevel(logging.DEBUG) 

# File handler with rotation
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Console handler (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Format
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Attach handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)