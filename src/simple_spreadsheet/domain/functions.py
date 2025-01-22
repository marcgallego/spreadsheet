from abc import ABC, abstractmethod

from .formula_component import Operand


class Argument(ABC):
    @abstractmethod
    def evaluate_arg(self, spreadsheet: 'Spreadsheet') -> list[float]:
        pass

    @abstractmethod
    def get_dependencies(self) -> set:
        pass


class Function(Operand, Argument):
    def __init__(self, args: list[Argument]) -> None:
        self._args = args
        self._validate_args()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__.upper()}{self._args}"

    def _validate_args(self) -> None:
        if not self._args:
            raise ValueError("Function must have at least one argument")

    def _filter_nones(self, values: list[float]) -> list[float]:
        return [v for v in values if v is not None]

    def _evaluate_argument(self, arg: Argument, spreadsheet: 'Spreadsheet') -> list[float]:
        """Evaluates an argument and returns numeric values, excluding `None`."""
        return self._filter_nones(arg.evaluate_arg(spreadsheet))

    def _get_values(self, spreadsheet: 'Spreadsheet') -> list[float]:
        """Evaluates all arguments and combines valid values."""
        values = []
        for arg in self._args:
            values.extend(self._evaluate_argument(arg, spreadsheet))
        return values

    @abstractmethod
    def evaluate(self, spreadsheet: 'Spreadsheet') -> float:
        pass

    def evaluate_arg(self, spreadsheet: 'Spreadsheet') -> list[float]:
        return [self.evaluate(spreadsheet)]

    def get_dependencies(self) -> set:
        dependencies = set()
        for arg in self._args:
            dependencies.update(arg.get_dependencies())
        return dependencies


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
    def evaluate(self, spreadsheet: 'Spreadsheet') -> float:
        return sum(self._get_values(spreadsheet))


class Min(Function):
    def evaluate(self, spreadsheet: 'Spreadsheet') -> float:
        values = self._get_values(spreadsheet)
        return min(values, default=0.0)


class Max(Function):
    def evaluate(self, spreadsheet: 'Spreadsheet') -> float:
        values = self._get_values(spreadsheet)
        return max(values, default=0.0)


class Average(Function):
    def evaluate(self, spreadsheet: 'Spreadsheet') -> float:
        values = self._get_values(spreadsheet)
        return sum(values) / len(values) if values else 0.0
