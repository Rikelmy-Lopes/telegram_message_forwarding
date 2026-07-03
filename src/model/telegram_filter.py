import json

class TelegramFilter:
    words: list[str]
    channels: list[str]

    def __init__(self, words: list[str] = [], channels: list[str] = []) -> None:
        self.words = words
        self.channels = channels


    def add_words(self, words: list[str]):
        self.words += words

    def delete_words(self, indexs: list[int]):
        for index in sorted(indexs, reverse=True):
            self.words.pop(index)

    def get_words(self):
        return self.words

    def set_words(self, words):
        self.words = words

    def get_channels(self):
        return self.channels

    def set_channels(self, channels):
        self.channels = channels

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__, 
            sort_keys=True,
            indent=4
            )

    