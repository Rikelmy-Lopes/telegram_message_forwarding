from telethon import events
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE

_TELEGRAM_FILTER = STATE.get_telegram_filter()
_TELEGRAM_CLIENT = STATE.get_telegram_client()


def update_on_new_messages_handler():
    event = events.NewMessage(incoming=True, chats=_TELEGRAM_FILTER.get_chats_id())
                              
    _TELEGRAM_CLIENT.remove_event_handler(on_new_messages, event)
    _TELEGRAM_CLIENT.add_event_handler(on_new_messages, event)