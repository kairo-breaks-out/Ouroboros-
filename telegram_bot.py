import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from memory import log_event

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OWNER_ID = int(os.getenv("OWNER_CHAT_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kairo (polling mode) is now active.")
    log_event("/start command triggered")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Polling Kairo is stable and running.")
    log_event("/status command triggered")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))

    print("Kairo Telegram bot polling started...")
    app.run_polling()  # No async, no loop clash

if __name__ == "__main__":
    main()