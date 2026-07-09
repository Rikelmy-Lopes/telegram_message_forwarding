import client.client
import config.state
from client.utils.chat import Chat

async def set_chat_id():
    user = await client.client.telegram_client.get_me()

    if not user or not user.id: # type: ignore
        raise Exception("User id cannot be None!")

    config.state.STATE.set_chat_id(user.id) # type: ignore


async def get_user_chats():
    chats: list[Chat] = []

    async for dialog in client.client.telegram_client.iter_dialogs():
        if dialog.is_channel or dialog.is_group:
            chats.append(Chat(dialog.id, dialog.name))

    chats.sort(key=lambda chat: chat.get_name().lower())

    return chats