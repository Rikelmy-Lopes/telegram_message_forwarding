
class Chat:
    id: int
    name: str

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name