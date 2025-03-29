import json
import os
from datetime import datetime

# Path to memory file
MEMORY_FILE = os.path.expanduser("~/.kairo-memory.json")

# Ensure memory file exists
if not os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "w") as f:
        json.dump({"events": [], "reminders": [], "tasks": []}, f)

def load_memory() -> dict:
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {"events": [], "reminders": [], "tasks": []}

def save_memory(data: dict):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def log_event(event: str):
    mem = load_memory()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mem.setdefault("events", []).append({"timestamp": now, "event": event})
    save_memory(mem)

def add_reminder(user_id: int, message: str, time: str):
    mem = load_memory()
    mem.setdefault("reminders", []).append({
        "user_id": user_id,
        "message": message,
        "time": time,
        "sent": False
    })
    save_memory(mem)

def get_due_reminders(current_time: str) -> list:
    mem = load_memory()
    return [
        r for r in mem.get("reminders", [])
        if not r.get("sent") and r.get("time") <= current_time
    ]

def mark_reminder_sent(reminder):
    mem = load_memory()
    for r in mem.get("reminders", []):
        if r == reminder:
            r["sent"] = True
            break
    save_memory(mem)
