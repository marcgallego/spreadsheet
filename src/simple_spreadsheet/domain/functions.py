from typing import Union
from abc import ABC, abstractmethod

from domain.cell import Cell
from domain.cell_range import CellRange

# TODO: Cell or Coordinates?
type Argument = Union[Cell, CellRange, float]


class Function(ABC):
    @abstractmethod
    def evaluate(self) -> float:
        pass


class Sum(Function):
    def __init__(self, args: list[Argument]) -> None:
        self._args: list[Argument] = args

    def evaluate(self) -> float:
        result = 0
        for arg in self._args:
            if isinstance(arg, Cell):
                result += arg.get_value()
            elif isinstance(arg, float):
                result += arg
            elif isinstance(arg, CellRange):
                # TODO: implement this
                pass
        return result
