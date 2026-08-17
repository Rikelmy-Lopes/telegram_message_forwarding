import logging
from config.state import STATE

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_APPLICATION = STATE.get_application()


async def send_message(text: str):
    try:
        await _APPLICATION.bot.send_message(chat_id=STATE.get_chat_id(), text=text, parse_mode='HTML') # type: ignore
    except Exception as e:
        logger.error(f"Error sending the message to the user: {str(e)}")
