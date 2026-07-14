from telethon import events
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE


def set_event_handlers():
    _telegram_client = STATE.get_telegram_client()

    _telegram_client.add_event_handler(on_new_messages, events.NewMessage(incoming=True, chats=STATE.get_telegram_filter().get_chats_id()))