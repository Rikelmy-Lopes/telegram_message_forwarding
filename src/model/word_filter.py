from pydantic import BaseModel


class WordFilter(BaseModel):
    value: list[str]
    order: int

    def __init__(self, value: list[str], order: int = -1, **kwargs) -> None:
        super().__init__(value=value, order=order, **kwargs)
        self.order =  1 if len(self.value) == 1 else -1


    def get_value(self):
        return self.value

    def __hash__(self) -> int:
        return hash(tuple(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WordFilter):
            return NotImplemented
        
        return self.value == other.value

    def __lt__(self, other: "WordFilter") -> bool:
        if not isinstance(other, WordFilter):
            return NotImplemented
        return self.order < other.order
    
