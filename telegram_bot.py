import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kairo (polling mode) is now active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Polling Kairo is stable and running.")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot polling started...")
    await app.run_polling()

# Safe bootloader — compatible with Render
def safe_start():
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Inside existing loop (Render), spawn task
            loop.create_task(run_bot())
        else:
            loop.run_until_complete(run_bot())
    except RuntimeError:
        asyncio.run(run_bot())

# Run it
if __name__ == "__main__":
    safe_start()


