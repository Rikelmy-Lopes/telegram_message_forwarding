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

TELEGRAM_FILTER = TelegramFilter(_words, _chats)
CHAT_ID = None