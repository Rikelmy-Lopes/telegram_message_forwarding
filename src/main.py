# pyright: reportGeneralTypeIssues=false
import asyncio
import logging
from bot.bot import set_application_handlers
from client.client import set_event_handlers
from client.utils.user import set_chat_id
from utils.text import format_chat_list, format_text_list
from config.state import STATE

_TELEGRAM_FILTER = STATE.get_telegram_filter()
_telegram_client = STATE.get_telegram_client()
_application = STATE.get_application()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Palavras sendo monitoradas:\n {format_text_list(_TELEGRAM_FILTER.get_words())}\n")
logger.info(f"Chats sendo monitorados:\n{format_chat_list(_TELEGRAM_FILTER.get_chats(), True)}\n")


async def main():
    set_application_handlers()
    set_event_handlers()
    
    await _telegram_client.start()

    await _application.initialize()
    await _application.start()

    await set_chat_id()

    if _application.updater:
        await _application.updater.start_polling()

    logger.info("Monitor iniciado... Pressione Ctrl+C para parar.")

    await _telegram_client.run_until_disconnected()
    
    if _application.updater:
        await _application.updater.stop()
        
    await _application.stop()
    await _application.shutdown()



try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.warning("Parando execução...")
    