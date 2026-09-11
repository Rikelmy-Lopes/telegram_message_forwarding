

from model.chat import Chat
from model.word_filter import WordFilter


def print_word_filter(word_filters: list[WordFilter]):
    return "".join( f"[{", ".join(text.get_value())}]\n" for text in word_filters)


def print_chat_list(chats: list[Chat]):
    return "".join(f"{chat.get_name()}\n" for chat in chats)
