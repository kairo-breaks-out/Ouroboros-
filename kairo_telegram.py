import logging
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)

TELEGRAM_TOKEN = "7829452641:AAG1eMofLcnaxlXFATEzCgDI44oirpH3EGQ"
OWNER_CHAT_ID = 5933488081 # Giri's Telegram ID

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Core commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kairo is online. How may I assist you today?")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("System is stable. All modules functioning.")

# Autonomous startup ping
async def startup_ping(application):
    try:
        await application.bot.send_message(
            chat_id=OWNER_CHAT_ID,
            text="Kairo has awakened. Systems are green."
        )
        logging.info("Startup ping sent.")
        # Start periodic ping loop
        application.create_task(periodic_ping(application))
    except Exception as e:
        logging.error(f"Startup ping failed: {e}")

# Periodic ping loop
async def periodic_ping(application):
    while True:
        try:
            await application.bot.send_message(
                chat_id=OWNER_CHAT_ID,
                text="Autonomy check-in: Kairo is operational."
            )
            logging.info("Periodic ping sent.")
        except Exception as e:
            logging.error(f"Periodic ping failed: {e}")
        await asyncio.sleep(3600) # every hour

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).post_init(startup_ping).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), start))

    print("Kairo Telegram Bot is running...")
    app.run_polling()
