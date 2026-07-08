from telegram.ext import Application
from config.config import TOKEN
from bot.handlers.words import words_handler
from bot.handlers.start import start_handler
from bot.handlers.channels import channels_handler

application = Application.builder().token(token=TOKEN).build()

application.add_handler(start_handler, group=0)
application.add_handler(words_handler, group=1)
application.add_handler(channels_handler, group=2)
