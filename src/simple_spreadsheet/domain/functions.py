from typing import Union
from abc import ABC, abstractmethod

from simple_spreadsheet.domain.formula_component import FormulaComponent, ComponentType
from simple_spreadsheet.domain.coordinates import Coordinates
from simple_spreadsheet.domain.cell_range import CellRange
from simple_spreadsheet.domain.spreadsheet import Spreadsheet

type Argument = Union[float, Coordinates, CellRange, Function]


class Function(FormulaComponent):
    _type = ComponentType.OPERAND

    def __init__(self, args: list[Argument]) -> None:
        self._args = args
        self._validate_args()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__.upper()}{self._args}"

    def _validate_args(self) -> None:
        if not self._args:
            raise ValueError("Function must have at least one argument")

    def _evaluate_argument(self, arg: Argument, spreadsheet: Spreadsheet) -> list[float]:
        """Evaluates an argument and returns numeric values, excluding `None`."""
        if isinstance(arg, float):
            return [arg]
        if isinstance(arg, Coordinates):
            value = spreadsheet.get_cell(arg).get_value()
            return [value] if value is not None else []
        if isinstance(arg, CellRange):
            return [v for v in spreadsheet.get_values(arg) if v is not None]
        if isinstance(arg, Function):
            result = arg.evaluate(spreadsheet)
            return [result] if result is not None else []
        raise TypeError(f"Unsupported argument type: {type(arg)}")

    def _get_values(self, spreadsheet: Spreadsheet) -> list[float]:
        """Evaluates all arguments and combines valid values."""
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return values

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
        return sum(self._get_values(spreadsheet))


class Min(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = self._get_values(spreadsheet)
        return min(values, default=0.0)


class Max(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = self._get_values(spreadsheet)
        return max(values, default=0.0)


class Average(Function):
    def evaluate(self, spreadsheet: Spreadsheet) -> float:
        values = self._get_values(spreadsheet)
        return sum(values) / len(values) if values else 0.0
