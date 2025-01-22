from ..formula_component import FormulaComponent, ComponentType
from ..operators import BinaryOperator
from .visitor import Visitor
from .consts import PRECEDENCE, OPENING_PARENTHESIS


class Converter():

    def __init__(self) -> None:
        self._precedence = PRECEDENCE
        self._opening_parenthesis = OPENING_PARENTHESIS

    def infix_to_postfix(self, components: list[FormulaComponent]) -> list[FormulaComponent]:
        """Converts a list of Components in infix order to postfix order."""
        output = []
        stack = []
        precedence = self._precedence

        for component in components:
            component_type = component.type

            if component_type == ComponentType.OPERAND:
                output.append(component)
            elif component_type == ComponentType.OPERATOR:
                while (stack and isinstance(stack[-1], BinaryOperator) and
                       precedence.get(stack[-1].symbol, 0) >= precedence.get(component.symbol, 0)):
                    output.append(stack.pop())
                stack.append(component)
            elif component_type == ComponentType.OPENING_PARENTHESIS:
                stack.append(component)
            elif component_type == ComponentType.CLOSING_PARENTHESIS:
                while stack and stack[-1].symbol != self._opening_parenthesis:
                    output.append(stack.pop())
                if stack and stack[-1].symbol == self._opening_parenthesis:
                    stack.pop()

        while stack:
            output.append(stack.pop())

        return output
