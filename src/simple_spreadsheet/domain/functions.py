from typing import Union
from abc import ABC, abstractmethod

from domain.formula_component import FormulaComponent, ComponentType
from domain.coordinates import Coordinates
from domain.cell_range import CellRange
from domain.spreadsheet import Spreadsheet

type Argument = Union[float, Coordinates, CellRange, Function]


class Function(FormulaComponent):
    _type = ComponentType.OPERAND

    def __init__(self, args: list[Argument]) -> None:
        self._args = args
        self._validate_args()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__.upper()}{self._args}"

    def _is_valid_argument(self, arg: Argument) -> bool:
        return isinstance(arg, (float, Coordinates, CellRange, Function))

    def _validate_args(self) -> None:
        if not self._args:
            raise ValueError("Function must have at least one argument")
        for arg in self._args:
            if not self._is_valid_argument(arg):
                raise TypeError(f"Invalid argument type: {type(arg)}")

    def _evaluate_argument(self, arg: Argument, spreadsheet: Spreadsheet) -> list[float]:
        """Evaluates a single argument and returns a list of values."""
        if isinstance(arg, float):
            return [arg]
        elif isinstance(arg, Coordinates):
            cell = spreadsheet.get_cell(arg)
            return [cell.get_value()]
        elif isinstance(arg, CellRange):
            return spreadsheet.get_values(arg)
        elif isinstance(arg, Function):
            return [arg.evaluate(spreadsheet)]
        raise TypeError(f"Unsupported argument type: {type(arg)}")

    @abstractmethod
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        pass


class FunctionFactory:
    @staticmethod
    def create(name: str, args: list[Argument]) -> Function:
        if name == 'SUMA':
            return Sum(args)
        if name == 'PROMEDIO':
            return Average(args)
        if name == 'MAX':
            return Max(args)
        if name == 'MIN':
            return Min(args)
        raise ValueError(f"Unsupported function: {name}")


class Sum(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return sum(values)


class Min(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return min(values)


class Max(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return max(values)


class Average(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return sum(values) / len(values)
