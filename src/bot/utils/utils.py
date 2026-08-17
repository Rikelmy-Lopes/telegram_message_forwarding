

def get_valid_indexs(text: str | None, target_list: list) -> list[int]:
    if not text:
        return []
    
    indexs = [int(i.strip()) for i in text.split(';') if i.strip().isdigit()]
    return [i for i in indexs if i >= 0 and i < len(target_list)]
