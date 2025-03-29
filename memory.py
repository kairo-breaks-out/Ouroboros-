import os
import json

# Store memory in the current project directory
MEMORY_FILE = ".kairo-memory.json"

def ensure_memory_file():
    os.makedirs(os.path.dirname(MEMORY_FILE) or ".", exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w") as f:
            json.dump({"events": []}, f)

def load_memory():
    ensure_memory_file()
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(data):
    ensure_memory_file()
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def log_event(event):
    mem = load_memory()
    mem.setdefault("events", []).append({"event": event})
    save_memory(mem)