from ..spreadsheet import Spreadsheet
from ..formula_components import FormulaComponent
from .visitor import Visitor


class PostfixEvaluator(Visitor):
    def __init__(self, spreadsheet: Spreadsheet) -> None:
        self._stack = []
        self._spreadsheet = spreadsheet

    def visit_operand(self, operand) -> None:
        self._stack.append(operand)

    def visit_operator(self, operator) -> None:
        operand2 = self._stack.pop()
        operand1 = self._stack.pop()
        result = operator.operate(operand1, operand2, self._spreadsheet)
        self._stack.append(result)

    def visit_opening_parenthesis(self, _) -> None:
        raise ValueError("Invalid postfix expression.")

    def visit_closing_parenthesis(self, _) -> None:
        raise ValueError("Invalid postfix expression.")

    def evaluate(self, postfix: list[FormulaComponent]) -> float:
        self._stack.clear()
        for component in postfix:
            component.accept(self)

        if len(self._stack) != 1:
            raise ValueError("Invalid postfix expression.")

        return self._stack.pop().evaluate(self._spreadsheet)
