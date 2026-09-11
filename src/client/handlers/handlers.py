from telethon import events
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE

_TELEGRAM_FILTER = STATE.get_telegram_filter()

async def _on_new_messages_callback(e: events.NewMessage.Event):
    await on_new_messages(e, _TELEGRAM_FILTER)


def update_on_new_messages_handler():
    telegram_client = STATE.get_telegram_client()

    new_message_event = events.NewMessage(chats=_TELEGRAM_FILTER.get_chats_id())

    telegram_client.remove_event_handler(_on_new_messages_callback)
    telegram_client.add_event_handler(_on_new_messages_callback, new_message_event)
