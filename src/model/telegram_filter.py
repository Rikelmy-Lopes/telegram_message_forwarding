import json
from client.utils.chat import Chat

class TelegramFilter:
    _words: list[str]
    _chats: list[Chat]
    _chat_ids: list[int]

    def __init__(self, words: list[str] = [], chats: list[Chat] = []) -> None:
        self._words = words
        self._chats = chats
        self._update_chat_ids()


    def add_words(self, words: list[str]):
        for word in words:
            if word not in self._words:
                self._words.append(word)


    def add_chats(self, chats: list[Chat]):
        for chat in chats:
            if self._is_chat_added(chat): 
                continue

            self._chats.append(chat)
        
        self._update_chat_ids()


    def delete_words(self, indexs: list[int]) -> list[str]:
        removed: list[str] = []

        for index in sorted(indexs, reverse=True):
            removed.append(self._words.pop(index))

        return removed
            

    def delete_chats(self, indexs: list[int]) -> list[Chat]:
        removed: list[Chat] = []

        for index in sorted(indexs, reverse=True):
            removed.append(self._chats.pop(index))

        if removed:
            self._update_chat_ids()

        return removed

    def _is_chat_added(self, other_chat: Chat) -> bool:
        return any(chat.get_id() == other_chat.get_id() for chat in self._chats)

    def _update_chat_ids(self) -> None:
        self._chat_ids = list(map(lambda chat: chat.get_id(), self._chats))

    def get_words(self) -> list[str]:
        return self._words

    def get_chats(self) -> list[Chat]:
        return self._chats

    def get_chats_id(self) -> list[int]:
        return self._chat_ids

    def to_json(self) -> str:
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4
            )
    