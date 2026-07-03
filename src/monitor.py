from telethon import TelegramClient, events
from bot.bot import send_message
from config.config import API_HASH, API_ID, CANAIS_ALVO, PALAVRAS_CHAVE
from config.state import TELEGRAM_FILTER
from utils import send_notification
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info(f"Palavras sendo monitoradas: {PALAVRAS_CHAVE}\n")
logger.info(f"Canais sendo monitorados: {CANAIS_ALVO}\n")

client = TelegramClient('sessao_monitor', API_ID, API_HASH)

@client.on(events.NewMessage(chats=CANAIS_ALVO))
async def monitorador(event):
    try:
        texto_mensagem: str = event.message.text

        if not texto_mensagem:
            return

        if not event.chat:
            return

        for palavra in TELEGRAM_FILTER.get_words():
            if palavra in texto_mensagem.lower():
                logger.info(f"Palavra encontrada no canal {event.chat.title}!")
                
                link_mensagem = f"https://t.me/{event.chat.username}/{event.message.id}" if event.chat.username else "Canal Privado"
                alerta = f"🚨 **Palavra-chave detectada! ({palavra})** \n\nCanal: {event.chat.title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
                
                await send_message(alerta)
                send_notification(alerta, palavra)
                break

    except Exception as e:
        logger.exception(e)


logger.info("Monitor iniciado... Pressione Ctrl+C para parar.")