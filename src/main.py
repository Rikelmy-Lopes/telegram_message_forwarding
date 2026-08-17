# pyright: reportGeneralTypeIssues=false
import asyncio
import logging
from bot.bot import set_application_handlers
from client.client import set_event_handlers
from client.utils.user import set_chat_id
from utils.text import format_chat_list, format_word_filter
from config.state import STATE
from utils.utils import error_handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


async def main():
    TELEGRAM_FILTER = STATE.get_telegram_filter()
    TELEGRAM_CLIENT = STATE.get_telegram_client()
    APPLICATION = STATE.get_application()

    logger.info(f"Palavras sendo monitoradas:\n{format_word_filter(TELEGRAM_FILTER.get_word_filters())}\n")
    logger.info(f"Chats sendo monitorados:\n{format_chat_list(TELEGRAM_FILTER.get_chats(), True)}\n")

    set_application_handlers()
    set_event_handlers()
    
    await TELEGRAM_CLIENT.start()

    await APPLICATION.initialize()
    await APPLICATION.start()

    await set_chat_id()

    if APPLICATION.updater:
        await APPLICATION.updater.start_polling(error_callback=error_handler, bootstrap_retries=120)

    logger.info("Monitor iniciado... Pressione Ctrl+C para parar.")

    await TELEGRAM_CLIENT.run_until_disconnected()
    
    if APPLICATION.updater:
        await APPLICATION.updater.stop()
        
    await APPLICATION.stop()
    await APPLICATION.shutdown()




try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.warning("Parando execução...")