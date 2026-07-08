import client.client
import config.state

async def set_chat_id():
    user = await client.client.telegram_client.get_me()

    if not user or not user.id: # type: ignore
        raise Exception("User id cannot be None!")

    config.state.CHAT_ID = user.id # type: ignore