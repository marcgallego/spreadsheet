from enum import Enum, auto
from typing import Union, List

from .consts import OPERATORS


class ComponentType(Enum):
    """Types of components in a formula."""
    OPERATOR = auto()
    OPERAND = auto()


class Component:
    """Base class representing a component in a formula."""

    def __init__(self, value: str, component_type: ComponentType) -> None:
        self.value = value
        self.component_type = component_type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"


class Operator(Component):
    """Represents an operator in a formula."""

    def __init__(self, value: str) -> None:
        super().__init__(value, ComponentType.OPERATOR)


class Operand(Component):
    """Represents an operand in a formula."""

    def __init__(self, value: Union[str, float]) -> None:
        super().__init__(value, ComponentType.OPERAND)


class Parser:
    """Parser to convert tokenized formulas into Components and generate postfix expressions."""

    def __init__(self) -> None:
        self._operators = OPERATORS
        self._precedence = {
            "*": 2, "/": 2,
            "+": 1, "-": 1,
        }

    def tokens_to_components(self, tokens: List[str]) -> List[Component]:
        """Converts a list of tokens into Component objects."""
        components = []

        for token in tokens:
            if token in self._operators:
                components.append(Operator(token))
            else:
                components.append(Operand(token))

        return components

    def infix_to_postfix(self, components: List[Component]) -> List[Component]:
        """Converts a list of Components in infix order to postfix order."""
        output = []
        stack = []
        precedence = self._precedence

        for component in components:
            if component.component_type == ComponentType.OPERAND:
                output.append(component)
            elif component.component_type == ComponentType.OPERATOR:
                while (stack and
                       isinstance(stack[-1], Operator) and
                       precedence.get(stack[-1].value, 0) >= precedence.get(component.value, 0)):
                    output.append(stack.pop())
                stack.append(component)
            elif component.value == "(":
                stack.append(component)
            elif component.value == ")":
                while stack and stack[-1].value != "(":
                    output.append(stack.pop())
                if stack and stack[-1].value == "(":
                    stack.pop()

        while stack:
            output.append(stack.pop())

        return output
