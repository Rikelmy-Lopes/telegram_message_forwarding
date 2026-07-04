from telegram.ext import Application
from config.config import CHAT_ID, TOKEN
from bot.handlers.words import words_handler
from bot.handlers.start import start_handler
from bot.handlers.channels import channels_handler

application = Application.builder().token(token=TOKEN).build()

application.add_handler(start_handler)
application.add_handler(words_handler)
application.add_handler(channels_handler)

async def send_message(text: str):
    await application.bot.send_message(chat_id=CHAT_ID, text=text)
