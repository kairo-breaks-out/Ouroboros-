import json
import os
from datetime import datetime

# Path to memory file
MEMORY_FILE = os.path.expanduser("~/.kairo-memory.json")

# Ensure the memory file exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({}, f)

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_event(event: str):
    mem = load_memory()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mem.setdefault("events", []).append({"timestamp": now, "event": event})
    save_memory(mem)