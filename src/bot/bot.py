from bot.handlers.words import words_handler
from bot.handlers.start import start_handler
from bot.handlers.channels import channels_handler
from config.state import STATE


def set_application_handlers():
    _application = STATE.get_application()

    _application.add_handler(start_handler, group=0)
    _application.add_handler(words_handler, group=1)
    _application.add_handler(channels_handler, group=2)