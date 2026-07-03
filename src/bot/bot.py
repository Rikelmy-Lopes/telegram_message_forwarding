from telegram.ext import Application
from config.config import CHAT_ID, TOKEN
from bot.handlers.words import words_handler

application = Application.builder().token(token=TOKEN).build()

application.add_handler(words_handler)

async def send_message(text: str):
    await application.bot.send_message(chat_id=CHAT_ID, text=text)
