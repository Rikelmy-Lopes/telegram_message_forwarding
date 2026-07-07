from client.client import telegram_client
from client.handlers.on_message_handler import on_new_messages

def update_on_new_messages_handler(event):
    telegram_client.remove_event_handler(on_new_messages, event)

    telegram_client.add_event_handler(on_new_messages, event)