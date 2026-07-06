

def format_text_list(texts: list[str]):
    return "".join(f"<b>{index}</b> - {text}\n" for index, text in enumerate(texts))
