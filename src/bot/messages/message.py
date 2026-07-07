from bot.bot import application
from config.config import CHAT_ID

async def send_message(text: str):
    await application.bot.send_message(chat_id=CHAT_ID, text=text, parse_mode='HTML')