from telethon import TelegramClient, events
from client.handlers.on_message_handler import on_new_messages
from config.config import API_HASH, API_ID
from config.state import STATE

telegram_client = TelegramClient('sessao_monitor', API_ID, API_HASH)
telegram_client.add_event_handler(on_new_messages, events.NewMessage(incoming=True, chats=STATE.get_telegram_filter().get_chats_id()))
