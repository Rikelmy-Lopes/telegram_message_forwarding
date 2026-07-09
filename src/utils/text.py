from client.utils.chat import Chat

def format_text_list(texts: list[str]):
    return "".join(f"<b>{index}</b> - {text}\n" for index, text in enumerate(texts))


def format_chat_list(chats: list[Chat], use_id: bool = False):
    return "".join(f"<b>{chat.get_id() if use_id else index}</b> - {chat.get_name()}\n" for index, chat in enumerate(chats))