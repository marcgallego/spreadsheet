from ..formula_components import FormulaComponent
from ..operators import BinaryOperator
from .visitor import Visitor
from .consts import PRECEDENCE


class Converter(Visitor):

    def __init__(self) -> None:
        self._output: list[FormulaComponent] = []
        self._stack: list[FormulaComponent] = []
        self._precedence = PRECEDENCE
        self._opening_parenthesis = '('

    def _should_pop_operator(self, operator: FormulaComponent) -> bool:
        """Determines if an operator should be popped from the stack based on precedence."""
        return (
            self._stack and
            isinstance(self._stack[-1], BinaryOperator) and
            self._precedence.get(
                self._stack[-1].symbol, 0) >= self._precedence.get(operator.symbol, 0)
        )

    def _pop_until(self, stop_symbol: str) -> None:
        """Pops elements from the stack until a specific symbol is encountered."""
        while self._stack and self._stack[-1].symbol != stop_symbol:
            self._output.append(self._stack.pop())
        if self._stack and self._stack[-1].symbol == stop_symbol:
            self._stack.pop()

    def visit_operand(self, operand: FormulaComponent) -> None:
        self._output.append(operand)

    def visit_operator(self, operator: FormulaComponent) -> None:
        while (self._stack and isinstance(self._stack[-1], BinaryOperator) and
               self._precedence.get(self._stack[-1].symbol, 0) >= self._precedence.get(operator.symbol, 0)):
            self._output.append(self._stack.pop())
        self._stack.append(operator)

    def visit_opening_parenthesis(self, parenthesis: FormulaComponent) -> None:
        self._stack.append(parenthesis)

    def visit_closing_parenthesis(self, _: FormulaComponent) -> None:
        self._pop_until(self._opening_parenthesis)

    def infix_to_postfix(self, components: list[FormulaComponent]) -> list[FormulaComponent]:
        """Converts a list of Components in infix order to postfix order."""
        self._output = []
        self._stack = []

        for component in components:
            component.accept(self)

        while self._stack:
            self._output.append(self._stack.pop())

        return self._output
