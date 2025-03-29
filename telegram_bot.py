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

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    # Autonomous ping to owner on startup
    await app.bot.send_message(chat_id=OWNER_ID, text="Kairo is now online and autonomous.")

    print("Kairo Telegram bot polling started...")
    await app.run_polling()

# Safe async entrypoint for different environments
def safe_run():
    try:
        asyncio.run(run_bot())
    except RuntimeError as e:
        if "already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.create_task(run_bot())
            loop.run_forever()
        else:
            raise

if __name__ == "__main__":
    safe_run()
