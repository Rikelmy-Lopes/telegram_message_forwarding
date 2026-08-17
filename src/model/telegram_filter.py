from pydantic import BaseModel
from model.chat import Chat
from model.word_filter import WordFilter

_FILE_NAME = 'telegram_filter.json'

class TelegramFilter(BaseModel):
    word_filters: list[WordFilter]
    chats: list[Chat]
    chat_ids: set[int]

    def __init__(self, word_filters: list[WordFilter] = [], chats: list[Chat] = [], chat_ids: set[int] = set(), **kwargs) -> None:
        super().__init__(word_filters=word_filters, chats=chats, chat_ids=chat_ids, **kwargs)
        self._update_chat_ids()


    def add_word_filters(self, word_filters: list[WordFilter]):
        for word_filter in word_filters:

            if word_filter not in self.word_filters:
                self.word_filters.append(word_filter)
        
        self.word_filters = sorted(self.word_filters)


    def add_chats(self, chats: list[Chat]):
        for chat in chats:
            if self._is_chat_added(chat): 
                continue

            self.chats.append(chat)
            self.chat_ids.add(chat.get_id())


    def delete_word_filters(self, indexs: list[int]) -> list[WordFilter]:
        removed: list[WordFilter] = []

        for index in sorted(indexs, reverse=True):
            removed.append(self.word_filters.pop(index))

        self.word_filters = sorted(self.word_filters)
        return removed
            

    def delete_chats(self, indexs: list[int]) -> list[Chat]:
        removed: list[Chat] = []

        for index in sorted(indexs, reverse=True):
            temp_chat = self.chats.pop(index)
            self.chat_ids.remove(temp_chat.get_id())

            removed.append(temp_chat)

        return removed

    def _is_chat_added(self, other_chat: Chat) -> bool:
        return other_chat.get_id() in self.chat_ids

    def _update_chat_ids(self) -> None:
        self.chat_ids = set(map(lambda chat: chat.get_id(), self.chats))

    def get_word_filters(self) -> list[WordFilter]:
        return self.word_filters

    def get_chats(self) -> list[Chat]:
        return self.chats

    def get_chats_id(self) -> set[int]:
        return self.chat_ids

    def save(self):
        with open(_FILE_NAME, 'w') as f:
            f.write(self.model_dump_json(ensure_ascii=True, indent=4))

    @classmethod
    def load(cls, word_filters: list[WordFilter] = [], chats: list[Chat] = []) :
        try:
            with open(_FILE_NAME, 'r', encoding='utf-8') as f:
                data = f.read()

                return cls.model_validate_json(data)
        except FileNotFoundError:
            return cls(word_filters, chats)
    