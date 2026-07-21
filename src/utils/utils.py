import logging
import os
from telegram.error import NetworkError, TelegramError
from winotify import Notification

logger = logging.getLogger(__name__)

def get_env(var_name: str):
    value = os.getenv(var_name)

    if value and value.strip():
        return value.strip()
    else:
        logger.error(f"Environment variable '{var_name}' does not exist or is empty!")
        raise RuntimeError(f"Environment variable '{var_name}' does not exist or is empty!")



def send_notification(msg: str, palavra: str):
    notificacao = Notification(
        app_id="message_forwarding",
        title=f"Produto em Promoção! Encontrado: ({palavra})",
        msg=msg,
        duration="short"
    )
    notificacao.show()


def error_handler(error: TelegramError):
    if isinstance(error, NetworkError):
        logger.error(f"Error while polling updates: {error.message}")
    else:
        logger.exception(error)