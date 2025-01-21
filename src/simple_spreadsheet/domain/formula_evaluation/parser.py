from typing import Union, List

from ..formula_component import ComponentType, OpeningParenthesis, ClosingParenthesis
from ..functions import Function, FunctionFactory
from ..cell_range import CellRange
from ..operators import BinaryOperatorFactory, BinaryOperator
from ..coordinates import Coordinates
from .consts import OPERATORS, UNARY_OPERATORS, FUNCTIONS, RANGE_SEPARATOR, PARAM_SEPARATOR

type Component = Union[float, Coordinates, Function, BinaryOperator]


class Parser:
    """Parser to convert tokenized formulas into Components and generate postfix expressions."""

    def __init__(self) -> None:
        self._operators = OPERATORS
        self._unary_operators = UNARY_OPERATORS
        self._functions = FUNCTIONS
        self._range_separator = RANGE_SEPARATOR
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
                if token == '-':
                    args.append(-next_token)
                else:
                    args.append(next_token)
                i += 2
            elif isinstance(token, float):
                args.append(token)
                i += 1
            else:  # Token is a cell reference (Coordinates)
                if tokens[i + 1] == self._range_separator:
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
        # TODO: unary operators not supported
        components = []

        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in self._functions:
                function, i = self.parse_function(tokens, i)
                components.append(function)
            elif token in self._operators:
                components.append(BinaryOperatorFactory.create(token))
                i += 1
            elif token == "(":
                components.append(OpeningParenthesis())
                i += 1
            elif token == ")":
                components.append(ClosingParenthesis())
                i += 1
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
            # TODO: float will be Number in the future, so this will need to be updated
            component_type = component.get_type() if not isinstance(
                component, float) else ComponentType.OPERAND

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
                while stack and stack[-1].symbol != "(":
                    output.append(stack.pop())
                if stack and stack[-1].symbol == "(":
                    stack.pop()

        while stack:
            output.append(stack.pop())

        return output
