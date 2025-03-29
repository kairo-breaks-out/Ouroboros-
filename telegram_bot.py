import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kairo (polling mode) is now active.")

# Status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Polling Kairo is stable and running.")

# Main loop
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot polling started...")
    await app.run_polling()

# Start bot
if __name__ == "__main__":
    asyncio.run(main())
