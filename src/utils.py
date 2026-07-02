import os
from dotenv import load_dotenv
from winotify import Notification
load_dotenv()

def get_env(var_name: str):
    value = os.getenv(var_name)

    if value:
        return value
    else:
        raise RuntimeError("f{var_name} does not exist")



def send_notification(msg: str, palavra: str):
    notificacao = Notification(
        app_id="message_forwarding",
        title=f"Produto em Promoção! Encontrado: ({palavra})",
        msg=msg,
        duration="short"
    )
    notificacao.show()