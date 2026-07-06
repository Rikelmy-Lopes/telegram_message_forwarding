import logging
from bot.messages.message import send_message
from config.state import TELEGRAM_FILTER
# from utils import send_notification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def on_new_messages(event):
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
                # send_notification(alerta, palavra)
                break

    except Exception as e:
        logger.exception(e)


def update_on_new_messages_handler(event):
    from client.telegram_client import telegram_client
    
    telegram_client.remove_event_handler(on_new_messages, event)

    telegram_client.add_event_handler(on_new_messages, event)