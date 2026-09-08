import logging
from telethon import events
from bot.messages.message import send_message
from config.state import STATE
from utils.text import contains_word, normalize_text

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


_TELEGRAM_FILTER = STATE.get_telegram_filter()

async def on_new_messages(event: events.NewMessage.Event):
    try:
        text_message: str = event.message.text

        if not text_message:
            return
        
        chat_title = event.chat.title if event.chat and event.chat.title else 'Chat Desconhecido'
        message_id = event.message.id

        comparison_text = normalize_text(text_message, True)

        for word_filter in _TELEGRAM_FILTER.get_word_filters():
            words = word_filter.get_value()

            is_all_finded = all(contains_word(word, comparison_text) for word in words)

            if is_all_finded:
                words_str = ', '.join(words)

                logger.info(f"Palavra encontrada no chat {chat_title} - ({words_str})!")
                    
                link_mensagem = f"https://t.me/{event.chat.username}/{message_id}" if event.chat and event.chat.username else "Chat Privado"
                alert_message = f"🚨 <b>Palavra-chave detectada! ({words_str})</b> \n\nChat: {chat_title}\nTexto:\n{text_message}\n\nLink da mensagem: {link_mensagem}"
            
                await send_message(alert_message)
                break

    except Exception as e:
        logger.error(e)
