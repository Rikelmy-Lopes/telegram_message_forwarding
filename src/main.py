# pyright: reportGeneralTypeIssues=false
import asyncio
from client.telegram_client import telegram_client
from bot.bot import application


async def main():
    await telegram_client.start()

    await application.initialize()
    await application.start()

    if application.updater:
        await application.updater.start_polling()

    await telegram_client.run_until_disconnected()
    
    if application.updater:
        await application.updater.stop()
        
    await application.stop()
    await application.shutdown()


asyncio.run(main())