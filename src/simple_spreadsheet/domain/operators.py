from typing import Union
from abc import abstractmethod

from .formula_component import FormulaComponent, ComponentType
from .coordinates import Coordinates
from .functions import Function
from .spreadsheet import Spreadsheet

type Operand = Union[float, Coordinates, Function]


class BinaryOperator(FormulaComponent):
    _symbol: str
    _type = ComponentType.OPERATOR

    @abstractmethod
    def _compute(self, left_value: float, right_value: float) -> float:
        """Perform the binary operation on evaluated operands."""
        pass

    def operate(self, left: Operand, right: Operand, spreadsheet: Spreadsheet) -> float:
        """Validate and evaluate operands, then compute the result."""
        self._validate_operands(left, right)
        left_value = self._evaluate_operand(left, spreadsheet)
        right_value = self._evaluate_operand(right, spreadsheet)
        return self._compute(left_value, right_value)

    def _is_valid_operand(self, operand: Operand) -> bool:
        return isinstance(operand, (float, Coordinates, Function))

    def _validate_operands(self, left: Operand, right: Operand) -> None:
        if not self._is_valid_operand(left):
            raise TypeError(f"Invalid operand type: {type(left)}")
        if not self._is_valid_operand(right):
            raise TypeError(f"Invalid operand type: {type(right)}")

    def _evaluate_operand(self, operand: Operand, spreadsheet: Spreadsheet) -> float:
        if isinstance(operand, float):
            return operand
        if isinstance(operand, Coordinates):
            val = spreadsheet.get_cell(operand).get_value()
            return val if val is not None else 0.0
        if isinstance(operand, Function):
            return operand.evaluate(spreadsheet)
        raise TypeError(f"Unexpected operand type: {type(operand)}")

    def __repr__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> str:
        return self._symbol


class BinaryOperatorFactory:
    @staticmethod
    def create(symbol: str) -> BinaryOperator:
        if symbol == '+':
            return Plus()
        if symbol == '-':
            return Minus()
        if symbol == '*':
            return Multiply()
        if symbol == '/':
            return Divide()
        raise ValueError(f"Unsupported operator: {symbol}")


class Plus(BinaryOperator):
    _symbol = '+'

    def _compute(self, left_value: float, right_value: float) -> float:
        return left_value + right_value


class Minus(BinaryOperator):
    _symbol = '-'

    def _compute(self, left_value: float, right_value: float) -> float:
        return left_value - right_value


class Multiply(BinaryOperator):
    _symbol = '*'

    def _compute(self, left_value: float, right_value: float) -> float:
        return left_value * right_value


class Divide(BinaryOperator):
    _symbol = '/'

    def _compute(self, left_value: float, right_value: float) -> float:
        if right_value == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return left_value / right_value
