import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes
)
from dotenv import load_dotenv
from memory import log_event

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

# Basic Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/start command triggered")
    await update.message.reply_text("Kairo (polling mode) is now active.\nType /status or /tutorial to begin.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/status command triggered")
    await update.message.reply_text("Polling Kairo is stable and running.")

# Admin Check Decorator
def admin_only(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id == OWNER_ID:
            await func(update, context)
        else:
            await update.message.reply_text("Access denied.")
    return wrapper

# Admin command example
@admin_only
async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/shutdown command triggered")
    await update.message.reply_text("Shutting down bot...")
    os._exit(0)

# Setup App & Handlers
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("shutdown", shutdown))

    print("Kairo Telegram bot polling started...")
    await app.run_polling()

# Safe Async Entrypoint
def safe_run():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            loop.create_task(run_bot())
        else:
            loop.run_until_complete(run_bot())
    except Exception as e:
        print(f"[ERROR] Telegram bot failed: {e}")

# Start
if __name__ == "__main__":
    safe_run()
