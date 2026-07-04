def format_words_list(words: list[str]):
    return "".join(f"<b>{index}</b> - {word}\n" for index, word in enumerate(words))
