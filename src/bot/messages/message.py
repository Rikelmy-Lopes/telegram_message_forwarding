from bot.bot import application
import config.state

async def send_message(text: str):    
    await application.bot.send_message(chat_id=config.state.STATE.get_chat_id(), text=text, parse_mode='HTML') # type: ignore