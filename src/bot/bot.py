from bot.handlers.words import WORDS_HANDLER
from bot.handlers.start import START_HANDLER
from bot.handlers.chats import CHATS_HANDLER
from config.state import STATE


def set_application_handlers():
    APPLICATION = STATE.get_application()

    APPLICATION.add_handler(START_HANDLER, group=0)
    APPLICATION.add_handler(WORDS_HANDLER, group=1)
    APPLICATION.add_handler(CHATS_HANDLER, group=2)