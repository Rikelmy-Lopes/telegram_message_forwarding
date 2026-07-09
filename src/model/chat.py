
class Chat:
    _id: int
    _name: str

    def __init__(self, id: int, name: str) -> None:
        self._id = id
        self._name = name

    def get_id(self) -> int:
        return self._id

    def get_name(self) -> str:
        return self._name