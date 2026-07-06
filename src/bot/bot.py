from telegram.ext import Application
from config.config import TOKEN
from bot.handlers.words import words_handler
from bot.handlers.start import start_handler
from bot.handlers.channels import channels_handler

application = Application.builder().token(token=TOKEN).build()

application.add_handlers([start_handler, words_handler, channels_handler])
