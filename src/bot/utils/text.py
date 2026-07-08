

from client.utils.chat import Chat


def format_text_list(texts: list[str]):
    return "".join(f"<b>{index}</b> - {text}\n" for index, text in enumerate(texts))


def format_chat_list(chats: list[Chat]):
    return "".join(f"<b>{index}</b> - {chat.get_name()}\n" for index, chat in enumerate(chats))