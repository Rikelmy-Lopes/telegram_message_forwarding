# pyright: reportGeneralTypeIssues=false
import asyncio
import logging
from client.client import telegram_client
from bot.bot import application
from config.state import TELEGRAM_FILTER

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Palavras sendo monitoradas: {TELEGRAM_FILTER.get_words()}\n")
logger.info(f"Canais sendo monitorados: {TELEGRAM_FILTER.get_channels()}\n")


async def main():
    await telegram_client.start()

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


asyncio.run(main())