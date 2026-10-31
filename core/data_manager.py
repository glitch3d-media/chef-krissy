import json
import os
from datetime import datetime

# Constants
DATA_DIR = "data"
BACKUP_DIR = f"{DATA_DIR}/backups"
FILE_PATH = f"{DATA_DIR}/menu_data.json"
BACKUP_FILE_TEMPLATE = f"{BACKUP_DIR}/%Y%m%d%H%M%S.json"

# Ensure backup directory exists
os.makedirs(BACKUP_DIR, exist_ok=True)


def load_data() -> dict:
    """Loads data from the JSON file, returns default schema if file missing."""
    if not os.path.exists(FILE_PATH):
        return {
            "meta": {
                "title": "",
                "business_name": "",
                "contact_info": "",
                "design": {},
            },
            "schedule": {"Monday": {"breakfast": [], "lunch": []}},
        }
    with open(FILE_PATH, "r") as file:
        return json.load(file)


def save_data(data: dict) -> None:
    """Saves data to the JSON file atomically, creating parent directory if needed."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)


def backup_data() -> str:
    """Backups current data to a JSON file in the backups directory."""
    data = load_data()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = BACKUP_FILE_TEMPLATE % timestamp
    with open(backup_path, "w") as file:
        json.dump(data, file, indent=4)
    return backup_path


def restore_backup(path: str) -> dict:
    """Restores data from a backup JSON file."""
    with open(path, "r") as file:
        return json.load(file)
