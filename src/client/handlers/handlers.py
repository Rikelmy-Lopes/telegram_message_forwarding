from telethon import events

from client.client import telegram_client
from client.handlers.on_message_handler import on_new_messages
from config.state import STATE

def update_on_new_messages_handler():
    event = events.NewMessage(incoming=True, chats=STATE.get_telegram_filter().get_chats_id())
                              
    telegram_client.remove_event_handler(on_new_messages, event)
    telegram_client.add_event_handler(on_new_messages, event)