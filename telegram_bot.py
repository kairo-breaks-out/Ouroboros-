import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kairo (webhook mode) is now active.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Webhook Kairo is stable and running.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    await app.initialize()
    await app.start()
    
    webhook_url = os.getenv("WEBHOOK_URL", "") + "/webhook"
    await app.bot.set_webhook(webhook_url)

    await app.updater.start_webhook(
        listen="0.0.0.0",
        port=10000,
        url_path="/webhook",
        webhook_url=webhook_url
    )

    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())

