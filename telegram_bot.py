import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from memory import log_event # Persistent memory integration

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/start command triggered")
    await update.message.reply_text("Kairo (webhook mode) is now active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/status command triggered")
    await update.message.reply_text("Webhook Kairo is stable and running.")

async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot webhook mode started...")

    await app.initialize()
    await app.start()

    # Set webhook
    await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")

    # Start webhook listener
    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path="/webhook",
        webhook_url=f"{WEBHOOK_URL}/webhook"
    )

    await app.updater.idle()

# Run the bot
if __name__ == "__main__":
    asyncio.run(run_bot())



