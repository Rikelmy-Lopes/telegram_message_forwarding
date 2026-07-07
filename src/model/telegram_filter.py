import json

class TelegramFilter:
    words: list[str]
    channels: list[str]

    def __init__(self, words: list[str] = [], channels: list[str] = []) -> None:
        self.words = words
        self.channels = channels


    def add_words(self, words: list[str]):
        self.words += words

    def add_channels(self, channels: list[str]):
        self.channels += channels

    def delete_words(self, indexs: list[int]) -> list[str]:
        removed = []

        for index in sorted(indexs, reverse=True):
            removed.append(self.words.pop(index))

        return removed
            

    def delete_channels(self, indexs: list[int]) -> list[str]:
        removed = []

        for index in sorted(indexs, reverse=True):
            removed.append(self.channels.pop(index))

        return removed

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

    