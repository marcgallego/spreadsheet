from enum import Enum, auto
from typing import Union, List

from ..functions import Function, FunctionFactory
from ..cell_range import CellRange
from .consts import OPERATORS, UNARY_OPERATORS, FUNCTIONS, RANGE_SEPARATOR, PARAM_SEPARATOR


class ComponentType(Enum):
    """Types of components in a formula."""
    OPERATOR = auto() # Binary operators
    OPERAND = auto() # Number, cell reference, or function


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
        self._unary_operators = UNARY_OPERATORS
        self._functions = FUNCTIONS
        self._precedence = {
            "*": 2, "/": 2,
            "+": 1, "-": 1,
        }

    def parse_function(self, tokens: List[str], position: int) -> tuple[Function, int]:
        """Parses a function call and returns a Function object."""
        function_name = tokens[position]
        args = []
        i = position + 2  # Skip the function name and "("
        n = len(tokens)

        is_function_complete = False
        while i < n and not is_function_complete:
            token = tokens[i]
            if token == ")":
                is_function_complete = True
                i += 1
            elif token == PARAM_SEPARATOR:
                i += 1
            elif token in self._functions:
                arg, i = self.parse_function(tokens, i)
                args.append(arg)
            elif token in self._unary_operators:
                next_token = tokens[i + 1]
                if token == "-":
                    args.append(-next_token)
                else:
                    args.append(next_token)
                i += 2
            elif isinstance(token, float):
                args.append(token)
                i += 1
            else:  # Token is a cell reference (Coordinates)
                if tokens[i + 1] == RANGE_SEPARATOR:
                    range_end = tokens[i + 2]
                    args.append(CellRange(token, range_end))
                    i += 3
                else:
                    args.append(token)
                    i += 1

        function = FunctionFactory.create(function_name, args)
        return function, i

    def tokens_to_components(self, tokens: List[str]) -> List[Component]:
        """Converts a list of tokens into Component objects."""
        components = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self._functions:
                function, i = self.parse_function(tokens, i)
                components.append(function)
            else:
                components.append(token)
                i += 1

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
