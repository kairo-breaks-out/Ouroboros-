import json
import os
from datetime import datetime

MEMORY_FILE = os.path.expanduser("~/kairo/.kairo-memory.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_event(message):
    mem = load_memory()
    mem.setdefault("logs", []).append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "message": message
    })
    mem["last_sync"] = datetime.utcnow().isoformat() + "Z"
    save_memory(mem)