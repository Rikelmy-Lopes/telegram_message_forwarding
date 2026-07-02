from telegram import Bot
from config import CHAT_ID, TOKEN

bot = Bot(token=TOKEN)

async def send_message(text: str):
    await bot.send_message(chat_id=CHAT_ID, text=text)