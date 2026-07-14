from config.state import STATE

_application = STATE.get_application()

async def send_message(text: str):    
    await _application.bot.send_message(chat_id=STATE.get_chat_id(), text=text, parse_mode='HTML') # type: ignore