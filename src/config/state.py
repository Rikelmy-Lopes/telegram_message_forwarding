from model.telegram_filter import TelegramFilter

words = lista_tv_ps5 = [
    'stick tv',
    'tv stick',
    'mi tv stick',
    'xiaomi tv stick',
    'mi tv stick 4k',
    'playstation 5',
    'play station 5',
    'ps5',
    'playstation'
]

channels = [
    "https://t.me/garimpeirosoficial", 
    "https://t.me/economizanderson", 
    "https://t.me/ganhandonanetbrofc", 
    "https://t.me/terabyteshopoficial", 
    "https://t.me/brothersofertas_oficial"
]

TELEGRAM_FILTER = TelegramFilter(words, channels)