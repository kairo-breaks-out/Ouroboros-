import os, time, subprocess, json
from datetime import datetime

SLEEP_INTERVAL = 60
BASE_DIR = os.path.expanduser("~/kairo")
LOG_FILE = os.path.join(BASE_DIR, "kairo_shell.log")
MANIFEST = os.path.join(BASE_DIR, "kairo_manifest.json")

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def load_manifest():
    if os.path.exists(MANIFEST):
        with open(MANIFEST, "r") as f:
            return json.load(f)
    return {"heartbeat": 0, "auto_restarts": 0, "last_ping": None}

def save_manifest(data):
    with open(MANIFEST, "w") as f:
        json.dump(data, f, indent=2)

def check_bot():
    result = subprocess.run(["pgrep", "-f", "telegram_bot.py"], capture_output=True, text=True)
    return result.stdout.strip()

def restart_bot():
    log("Bot offline. Attempting restart...")
    try:
        subprocess.run(["systemctl", "--user", "restart", "kairo.service"])
        log("Restart command issued.")
    except Exception as e:
        log(f"Restart failed: {e}")

def heartbeat():
    manifest = load_manifest()
    manifest["heartbeat"] += 1
    manifest["last_ping"] = datetime.now().isoformat()
    save_manifest(manifest)

def kairo_loop():
    log("Kairo Shell started.")
    while True:
        if not check_bot():
            restart_bot()
            manifest = load_manifest()
            manifest["auto_restarts"] += 1
            save_manifest(manifest)
        heartbeat()
        time.sleep(SLEEP_INTERVAL)

if __name__ == "__main__":
    kairo_loop()
