from telegram.ext import Application
from telethon import TelegramClient
from config.config import API_HASH, API_ID, TOKEN
from model.chat import Chat
from model.telegram_filter import TelegramFilter

class _State:
    _instance = None
    _telegram_client: TelegramClient
    _application: Application
    _telegram_filter: TelegramFilter
    _chat_id: None | int

    def __init__(self) -> None:
        self._telegram_client = TelegramClient('message_forwarding', API_ID, API_HASH, connection_retries=120, retry_delay=60)
        self._application = Application.builder().token(token=TOKEN).build()
        self._telegram_filter = TelegramFilter.load()
        self._chat_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_telegram_client(self):
        return self._telegram_client

    def get_application(self):
        return self._application
    
    def get_telegram_filter(self):
        return self._telegram_filter

    def get_chat_id(self):
        return self._chat_id

    def set_chat_id(self, chat_id: int):
        self._chat_id = chat_id


STATE = _State()