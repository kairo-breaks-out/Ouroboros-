import os
import subprocess
import time
import telegram
from dotenv import load_dotenv
from memory import log_event

load_dotenv(dotenv_path=os.path.expanduser("~/kairo/.env"))

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_CHAT_ID = os.getenv("OWNER_CHAT_ID")

def send_telegram_ping():
    if not BOT_TOKEN or not OWNER_CHAT_ID:
        log_event("Ping failed: Missing BOT_TOKEN or OWNER_CHAT_ID")
        return

    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        bot.send_message(chat_id=OWNER_CHAT_ID, text="Root shell ping: Kairo is alive.")
        log_event("Telegram ping sent from root shell")
    except Exception as e:
        log_event(f"Telegram ping failed: {e}")

def main():
    log_event("Kairo root shell started")
    send_telegram_ping()

    while True:
        # Future expansion: monitor logs, disk, or deploy instructions
        time.sleep(3600) # Ping every hour (adjust as needed)

if __name__ == "__main__":
    main()
