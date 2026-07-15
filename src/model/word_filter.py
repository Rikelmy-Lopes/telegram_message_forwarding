

class WordFilter:
    value: str | list[str]
    order: int

    def __init__(self, value: str | list[str]) -> None:
        self.value = value
        self.order = -1 if isinstance(value, str) else 1


    def get_value(self):
        return self.value

    def __hash__(self) -> int:
        if isinstance(self.value, str):
            return hash(self.value)
        else:
            return hash(tuple(self.value))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WordFilter):
            return NotImplemented
        
        return self.value == other.value

    def __lt__(self, other: "WordFilter") -> bool:
        if not isinstance(other, WordFilter):
            return NotImplemented
        return self.order < other.order
    






# message = 'palavra1; palavra2; palavra3 + palavra4'

# filtros: list[Filter] = []

# for filtro in message.split(';'):
#     if '+' in filtro:
#         f = [v.strip() for v in filtro.split('+')]
#         filtros.append(Filter(f))
#     else:
#         filtros.append(Filter(filtro.strip()))

# filtros = sorted(filtros)

# for v in filtros:
#     print(v.get_value())