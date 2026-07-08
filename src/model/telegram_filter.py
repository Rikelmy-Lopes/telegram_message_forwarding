import json
from client.utils.chat import Chat

class TelegramFilter:
    words: list[str]
    chats: list[Chat]

    def __init__(self, words: list[str] = [], chats: list[Chat] = []) -> None:
        self.words = words
        self.chats = chats


    def add_words(self, words: list[str]):
        for word in words:
            if word not in self.words:
                self.words.append(word)

    def add_chats(self, chats: list[Chat]):
        for chat in chats:
            if not self._is_chat_add(chat):
                self.chats.append(chat)

    def delete_words(self, indexs: list[int]) -> list[str]:
        removed = []

        for index in sorted(indexs, reverse=True):
            removed.append(self.words.pop(index))

        return removed
            

    def delete_chats(self, indexs: list[int]) -> list[str]:
        removed = []

        for index in sorted(indexs, reverse=True):
            removed.append(self.chats.pop(index))

        return removed

    def get_words(self):
        return self.words

    def set_words(self, words):
        self.words = words

    def get_chats(self):
        return self.chats

    def set_chats(self, chats):
        self.chats = chats

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4
            )

    def _is_chat_add(self, other_chat: Chat) -> bool:
        for chat in self.chats:
            if chat.get_id() == other_chat.get_id():
                return True
        
        return False
    