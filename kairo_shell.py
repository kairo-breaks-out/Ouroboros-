import os
import time
import subprocess
from datetime import datetime

LOG_FILE = "/home/girritharan/kairo/kairo_shell.log"
CHECK_INTERVAL = 60 # seconds

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def is_bot_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "telegram_bot.py"]).decode().strip()
        return bool(output)
    except subprocess.CalledProcessError:
        return False

def restart_bot():
    log_event("Bot not running. Restarting telegram_bot.py...")
    subprocess.Popen(["/usr/bin/python3", "/home/girritharan/kairo/telegram_bot.py"])
    log_event("telegram_bot.py restarted.")

if __name__ == "__main__":
    log_event("Kairo Shell Watchdog started.")
    while True:
        if not is_bot_running():
            restart_bot()
        time.sleep(CHECK_INTERVAL)
