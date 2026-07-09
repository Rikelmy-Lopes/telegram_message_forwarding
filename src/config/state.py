from client.utils.chat import Chat
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
    'a'
]

_chats = [
     Chat(-1001429192579, '🛒 Canal Garimpeiros 💸 Promoções, Ofertas, BUGs e Cupons'),
     Chat(-1001237760290, 'Economizanderson'),
     Chat(-1001518448659, 'Garimpo Ofertas- Cupons e Promoções'),
     Chat(-1001272487537, 'Terabyte Ofertas'),
     Chat(-1001443115288, 'BROTHERS OFERTAS OFICIAL'),
]

class _State:
    _instance = None
    _telegram_filter: TelegramFilter
    _chat_id: None | int

    def __init__(self) -> None:
        self._telegram_filter = TelegramFilter(_words, _chats)
        self._chat_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_telegram_filter(self):
        return self._telegram_filter

    def get_chat_id(self):
        return self._chat_id

    def set_chat_id(self, chat_id: int):
        self._chat_id = chat_id


STATE = _State()