
from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    name: str

    def __init__(self, id: int, name: str, **kwargs) -> None:
        super().__init__(id=id, name=name, **kwargs)

    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name