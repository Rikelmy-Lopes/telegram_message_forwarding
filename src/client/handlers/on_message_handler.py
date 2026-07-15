import logging
from telethon import events
from bot.messages.message import send_message
from config.state import STATE
# from utils import send_notification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_TELEGRAM_FILTER = STATE.get_telegram_filter()

async def on_new_messages(event: events.NewMessage.Event):
    try:
        texto_mensagem: str = event.message.text

        if not texto_mensagem:
            return
        
        chat_title = event.chat.title if event.chat and event.chat.title else 'Chat Desconhecido'
        message_id = event.message.id
        texto_comparacao = texto_mensagem.lower()

        for word_filter in _TELEGRAM_FILTER.get_words():
            value = word_filter.get_value()

            if isinstance(value, str):
                if value in texto_comparacao:
                    logger.info(f"Palavra encontrada no chat {chat_title} - ({value})!")
                    
                    link_mensagem = f"https://t.me/{event.chat.username}/{message_id}" if event.chat and event.chat.username else "Chat Privado"
                    alerta = f"🚨 <b>Palavra-chave detectada! ({value})</b> \n\nChat: {chat_title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
                    
                    await send_message(alerta)
                    # send_notification(alerta, palavra)
                    break
            else:
                if all(word in texto_comparacao for word in value):
                    logger.info(f"Palavra encontrada no chat {chat_title} - ({','.join(value)})!")
                    
                    link_mensagem = f"https://t.me/{event.chat.username}/{message_id}" if event.chat and event.chat.username else "Chat Privado"
                    alerta = f"🚨 <b>Palavra-chave detectada! ({','.join(value)})</b> \n\nChat: {chat_title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
                    
                    await send_message(alerta)
                    # send_notification(alerta, palavra)
                    break

    except Exception as e:
        logger.error(e)
