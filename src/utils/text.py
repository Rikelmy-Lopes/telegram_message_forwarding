import re
from model.chat import Chat
from model.word_filter import WordFilter


def format_word_filter(word_filters: list[WordFilter]):
    return "".join(
        f"<b>{index}</b> - {text.get_value()}\n"
        if isinstance(text.get_value(), str) else
        f"<b>{index}</b> - [{", ".join(text.get_value())}]\n"
        for index, text in enumerate(word_filters))


def format_chat_list(chats: list[Chat], use_id: bool = False):
    return "".join(f"<b>{chat.get_id() if use_id else index}</b> - {chat.get_name()}\n" for index, chat in enumerate(chats))


def format_chat_list_with_exclusion(chats: list[Chat], current_chat_ids: set[int]) -> str:
    return "".join(
        f"<b>{index}</b> - <s>{chat.get_name()}</s>\n" 
        if chat.get_id() in current_chat_ids else 
        f"<b>{index}</b> - {chat.get_name()}\n"
        for index, chat in enumerate(chats)
    )


def parse_word_filters(message: str):
    operator = '+'
    word_filters: list[WordFilter] = []

    for filter in message.strip().split(';'):
        if operator in filter:
            word_filter_list = [v.strip().lower() for v in filter.split('+') if v.strip()]
            word_filters.append(WordFilter(word_filter_list[0] if len(word_filter_list) == 1 else word_filter_list))
        else:
            word_filters.append(WordFilter(filter.strip().lower()))

    return word_filters


def create_regex_whole_word(word: str):
    pattern = rf'(?<!\S){re.escape(word)}(?!\S)'

    return re.compile(pattern, re.IGNORECASE)


def contains_word(word: str, text: str):
    return bool(re.search(create_regex_whole_word(word), text))