import asyncio
import logging
from time import perf_counter
from telethon import events
from bot.messages.message import send_message
from config.state import STATE
from utils.text import contains_word
# from utils import send_notification

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_TELEGRAM_FILTER = STATE.get_telegram_filter()

async def on_new_messages(event: events.NewMessage.Event):
    try:
        start = perf_counter()
        texto_mensagem: str = event.message.text

        if not texto_mensagem:
            return
        
        chat_title = event.chat.title if event.chat and event.chat.title else 'Chat Desconhecido'
        message_id = event.message.id
        texto_comparacao = texto_mensagem.lower()

        for word_filter in _TELEGRAM_FILTER.get_word_filters():
            value = word_filter.get_value()

            words = [value] if isinstance(value, str) else value

            is_all_finded = all(contains_word(word, texto_comparacao) for word in words)

            if is_all_finded:
                words_str = value if isinstance(value, str) else ', '.join(value)

                logger.info(f"Palavra encontrada no chat {chat_title} - ({words_str})!")
                    
                link_mensagem = f"https://t.me/{event.chat.username}/{message_id}" if event.chat and event.chat.username else "Chat Privado"
                alerta = f"🚨 <b>Palavra-chave detectada! ({words_str})</b> \n\nChat: {chat_title}\nTexto: {texto_mensagem}\nLink: {link_mensagem}"
                    
                asyncio.create_task(send_message(alerta))
                # await send_message(alerta)
                # send_notification(alerta, palavra)
                break


        end = perf_counter()

        print(f"Tempo execução: {(end - start) * 1000:.2f}ms")

    except Exception as e:
        logger.error(e)
