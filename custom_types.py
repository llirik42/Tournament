from typing import Callable

Graph = dict[int, list[int]]

Chain = list[int]

Strategy = Callable[[Graph], list[Chain]]
