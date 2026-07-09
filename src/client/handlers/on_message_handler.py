import logging

from telethon import events
from bot.messages.message import send_message
from config.state import STATE
# from utils import send_notification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def on_new_messages(event: events.NewMessage.Event):
    try:
        texto_mensagem: str = event.message.text

        if not texto_mensagem:
            return
        
        chat_title = event.chat.title if event.chat and event.chat.title else 'Chat Desconhecido'
        message_id = event.message.id

        for palavra in STATE.get_telegram_filter().get_words():
            if palavra in texto_mensagem.lower():
                logger.info(f"Palavra encontrada no canal {chat_title} - ({palavra})!")
                
                link_mensagem = f"https://t.me/{event.chat.username}/{message_id}" if event.chat and event.chat.username else "Canal Privado"
                alerta = f"🚨 <b>Palavra-chave detectada! ({palavra})</b> \n\nCanal: {chat_title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
                
                await send_message(alerta)
                # send_notification(alerta, palavra)
                break

    except Exception as e:
        logger.exception(e)
