
# Common Utilities
# A library of helper functions for simple, robust tool creation.

import json
import logging
from pathlib import Path
from datetime import datetime

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("antigravity")

def load_json(path: str) -> dict:
    """"Safely load a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON: {path}")
        return {}

def save_json(path: str, data: dict):
    """Safely save a dictionary to JSON."""
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved: {path}")
    except Exception as e:
        logger.error(f"Failed to save {path}: {str(e)}")

def timestamp() -> str:
    """Returns ISO 8601 timestamp."""
    return datetime.now().isoformat()
