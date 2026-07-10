import json

from model.chat import Chat

class TelegramFilter:
    _words: list[str]
    _chats: list[Chat]
    _chat_ids: set[int]

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
            self._chat_ids.add(chat.get_id())


    def delete_words(self, indexs: list[int]) -> list[str]:
        removed: list[str] = []

        for index in sorted(indexs, reverse=True):
            removed.append(self._words.pop(index))

        return removed
            

    def delete_chats(self, indexs: list[int]) -> list[Chat]:
        removed: list[Chat] = []

        for index in sorted(indexs, reverse=True):
            temp_chat = self._chats.pop(index)
            self._chat_ids.remove(temp_chat.get_id())

            removed.append(temp_chat)

        return removed

    def _is_chat_added(self, other_chat: Chat) -> bool:
        return other_chat.get_id() in self._chat_ids

    def _update_chat_ids(self) -> None:
        self._chat_ids = set(map(lambda chat: chat.get_id(), self._chats))

    def get_words(self) -> list[str]:
        return self._words

    def get_chats(self) -> list[Chat]:
        return self._chats

    def get_chats_id(self) -> set[int]:
        return self._chat_ids

    def to_json(self) -> str:
        return json.dumps(
            self,
            default=lambda o: list(o) if isinstance(o, set) else o.__dict__, 
            sort_keys=True,
            indent=4
            )
    