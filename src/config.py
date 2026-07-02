from utils import get_env

API_ID = int(get_env("API_ID"))
API_HASH = get_env("API_HASH")
PALAVRAS_CHAVE = [p.strip().lower() for p in get_env("PALAVRAS_CHAVES").split(";")]
CANAIS_ALVO = [p.strip() for p in get_env("CANAIS_ALVO").split(";")]
TOKEN = get_env("BOT_TOKEN")
CHAT_ID = get_env("CHAT_ID")