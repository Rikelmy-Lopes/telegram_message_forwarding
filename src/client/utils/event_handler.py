
def update_event_handler(callback, event):
    from client.telegram_client import telegram_client
    
    telegram_client.remove_event_handler(callback, event)

    telegram_client.add_event_handler(callback, event)