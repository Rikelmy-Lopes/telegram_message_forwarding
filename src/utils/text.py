

from model.chat import Chat
from model.word_filter import WordFilter


def format_text_list(texts: list[str]):
    return "".join(f"<b>{index}</b> - {text}\n" for index, text in enumerate(texts))


def format_chat_list(chats: list[Chat], use_id: bool = False):
    return "".join(f"<b>{chat.get_id() if use_id else index}</b> - {chat.get_name()}\n" for index, chat in enumerate(chats))

def format_chat_list_with_exclusion(chats: list[Chat], current_chat_ids: set[int]) -> str:
    return "".join(
        f"<b>{index}</b> - <s>{chat.get_name()}</s>\n" 
        if chat.get_id() in current_chat_ids else 
        f"<b>{index}</b> - {chat.get_name()}\n"
        for index, chat in enumerate(chats)
    )


def separate_message(message: str):
    word_filters: list[WordFilter] = []

    for filter in message.split(';'):
        if '+' in filter:
            f = [v.strip() for v in filter.split('+')]
            word_filters.append(WordFilter(f))
        else:
            word_filters.append(WordFilter(filter.strip()))

    return word_filters

