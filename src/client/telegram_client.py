from telethon import TelegramClient, events
from client.on_message_handler import on_new_messages
from config.config import API_HASH, API_ID
from config.state import TELEGRAM_FILTER
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Palavras sendo monitoradas: {TELEGRAM_FILTER.get_words()}\n")
logger.info(f"Canais sendo monitorados: {TELEGRAM_FILTER.get_channels()}\n")

telegram_client = TelegramClient('sessao_monitor', API_ID, API_HASH)
telegram_client.add_event_handler(on_new_messages, events.NewMessage(chats=TELEGRAM_FILTER.get_channels()))

logger.info("Monitor iniciado... Pressione Ctrl+C para parar.")