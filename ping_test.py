import asyncio
from telegram import Bot

TELEGRAM_TOKEN = "7829452641:AAG1eMofLcnaxlXFATEzCgDI44oirpH3EGQ"
CHAT_ID = 5933488081 # Giri

async def test_ping():
    bot = Bot(token=TELEGRAM_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text="Manual ping test from Kairo. Confirm receipt.")

if __name__ == "__main__":
    asyncio.run(test_ping())
