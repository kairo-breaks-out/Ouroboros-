import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from memory import log_event

load_dotenv()
nest_asyncio.apply() # Patch for environments with active event loops

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/start command triggered")
    await update.message.reply_text("Kairo (polling mode) is now active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/status command triggered")
    await update.message.reply_text("Polling Kairo is stable and running.")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot polling started...")
    await app.run_polling()

# Safe startup
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_bot())
