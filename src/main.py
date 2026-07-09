# pyright: reportGeneralTypeIssues=false
import asyncio
import logging
from utils.text import format_chat_list
import client.utils.user
from client.client import telegram_client
from bot.bot import application
from config.state import STATE

_TELEGRAM_FILTER = STATE.get_telegram_filter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Palavras sendo monitoradas: {_TELEGRAM_FILTER.get_words()}\n")
logger.info(f"Canais sendo monitorados:\n{format_chat_list(_TELEGRAM_FILTER.get_chats(), True)}\n")


async def main():
    await telegram_client.start()

    await client.utils.user.set_chat_id()

    await application.initialize()
    await application.start()

    if application.updater:
        await application.updater.start_polling()

    logger.info("Monitor iniciado... Pressione Ctrl+C para parar.")

    await telegram_client.run_until_disconnected()
    
    if application.updater:
        await application.updater.stop()
        
    await application.stop()
    await application.shutdown()



try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.warning("Parando execução...")
    