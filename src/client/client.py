from telethon import events
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE


def set_event_handlers():
    TELEGRAM_CLIENT = STATE.get_telegram_client()

    TELEGRAM_CLIENT.add_event_handler(on_new_messages, events.NewMessage(incoming=True, chats=STATE.get_telegram_filter().get_chats_id()))