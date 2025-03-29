import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from memory import log_event

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/start command triggered")
    await update.message.reply_text("Kairo (polling mode) is now active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/status command triggered")
    await update.message.reply_text("Polling Kairo is stable and running.")

async def autonomous_ping():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=OWNER_ID, text="Kairo is online. Autonomous ping successful.")
    log_event("Autonomous ping sent")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot polling started...")
    await autonomous_ping()
    await app.run_polling()

# Works even if event loop already exists
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        loop.create_task(run_bot())
    else:
        loop.run_until_complete(run_bot())
