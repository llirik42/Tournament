from typing import Protocol

Graph = dict[int, list[int]]

Chain = list[int]


class Strategy(Protocol):
    __name__: str

    def __call__(self, graph: Graph) -> list[Chain]:
        ...
