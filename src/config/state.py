from telegram.ext import Application
from telethon import TelegramClient
from config.config import API_HASH, API_ID, TOKEN
from model.chat import Chat
from model.telegram_filter import TelegramFilter

_words = [
    'stick tv',
    'tv stick',
    'mi tv stick',
    'xiaomi tv stick',
    'mi tv stick 4k',
    'playstation 5',
    'play station 5',
    'ps5',
    'playstation',
]

_chats = [
    Chat(-1001429192579, '🛒 Canal Garimpeiros 💸 Promoções, Ofertas, BUGs e Cupons'),
    Chat(-1001237760290, 'Economizanderson'),
    Chat(-1001518448659, 'Garimpo Ofertas- Cupons e Promoções'),
    Chat(-1001272487537, 'Terabyte Ofertas'),
    Chat(-1001443115288, 'BROTHERS OFERTAS OFICIAL'),
    Chat(-1001197236241, 'gt.OFERTAS'),
    Chat(-1002022913925, 'OFERTAS - TO SEM KIT'),
    Chat(-1002066258145, 'PC Build Wizard')
]

class _State:
    _instance = None
    _telegram_client: TelegramClient
    _application: Application
    _telegram_filter: TelegramFilter
    _chat_id: None | int

    def __init__(self) -> None:
        self._telegram_client = TelegramClient('sessao_monitor', API_ID, API_HASH)
        self._application = Application.builder().token(token=TOKEN).build()
        self._telegram_filter = TelegramFilter(_words, _chats)
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