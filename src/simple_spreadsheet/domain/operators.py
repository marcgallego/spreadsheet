from abc import abstractmethod
from typing import TYPE_CHECKING

from .formula_components import FormulaComponent, Operand
from .contents import Number
from .spreadsheet import Spreadsheet

if TYPE_CHECKING:
    from .formula_evaluation.visitor import Visitor


class BinaryOperator(FormulaComponent):
    _symbol: str

    @abstractmethod
    def _compute(self, left_value: float, right_value: float) -> float:
        """Perform the binary operation on evaluated operands."""
        pass

    def operate(self, left: Operand, right: Operand, spreadsheet: Spreadsheet) -> Number:
        """Validate and evaluate operands, then compute the result."""
        self._validate_operands(left, right)
        left_value = self._evaluate_operand(left, spreadsheet)
        right_value = self._evaluate_operand(right, spreadsheet)
        return Number(self._compute(left_value, right_value))

    def _validate_operands(self, left: Operand, right: Operand) -> None:
        if not isinstance(left, Operand):
            raise TypeError(f"Invalid operand type: {type(left)}")
        if not isinstance(right, Operand):
            raise TypeError(f"Invalid operand type: {type(right)}")

    def _evaluate_operand(self, operand: Operand, spreadsheet: Spreadsheet) -> float:
        result = operand.evaluate(spreadsheet)
        return result if result is not None else 0.0

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_operator(self)

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
