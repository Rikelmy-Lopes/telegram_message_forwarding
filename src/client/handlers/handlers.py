from telethon import events
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE

_telegram_filter = STATE.get_telegram_filter()
_telegram_client = STATE.get_telegram_client()


def update_on_new_messages_handler():
    event = events.NewMessage(incoming=True, chats=_telegram_filter.get_chats_id())
                              
    _telegram_client.remove_event_handler(on_new_messages, event)
    _telegram_client.add_event_handler(on_new_messages, event)