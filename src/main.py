# pyright: reportGeneralTypeIssues=false
import asyncio
from monitor import client
from bot.bot import application


async def main():
    await client.start()

    await application.initialize()
    await application.start()

    if application.updater:
        await application.updater.start_polling()

    await client.run_until_disconnected()
    
    if application.updater:
        await application.updater.stop()
        
    await application.stop()
    await application.shutdown()


asyncio.run(main())