import os
from dotenv import load_dotenv

load_dotenv()

print("TELEGRAM_TOKEN:", os.getenv("TELEGRAM_TOKEN"))
print("OWNER_CHAT_ID:", os.getenv("OWNER_CHAT_ID"))
print("WEBHOOK_URL:", os.getenv("WEBHOOK_URL"))
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY"))

