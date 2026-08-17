import logging
import os
from telegram.error import NetworkError, TelegramError

logger = logging.getLogger(__name__)

def get_env(var_name: str):
    value = os.getenv(var_name)

    if value and value.strip():
        return value.strip()
    else:
        logger.error(f"Environment variable '{var_name}' does not exist or is empty!")
        raise RuntimeError(f"Environment variable '{var_name}' does not exist or is empty!")



def error_handler(error: TelegramError):
    if isinstance(error, NetworkError):
        logger.error(f"Error while polling updates: {error.message}")
    else:
        logger.exception(error)