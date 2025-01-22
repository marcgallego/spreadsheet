from ..formula_components import FormulaComponent, OpeningParenthesis, ClosingParenthesis
from ..functions import Function, FunctionFactory
from ..operators import BinaryOperatorFactory
from ..cell_range import CellRange
from ..contents import Number
from .consts import OPERATORS, FUNCTIONS, RANGE_SEPARATOR, PARAM_SEPARATOR, OPENING_PARENTHESIS, CLOSING_PARENTHESIS


class Parser():
    """Parser to convert tokenized formulas into Components and generate postfix expressions."""

    def __init__(self) -> None:
        self._operators = OPERATORS
        self._functions = FUNCTIONS
        self._range_separator = RANGE_SEPARATOR
        self._opening_parenthesis = OPENING_PARENTHESIS
        self._closing_parenthesis = CLOSING_PARENTHESIS

    def _parse_function(self, tokens: list[str], position: int) -> tuple[Function, int]:
        """Parses a function call and returns a Function object."""
        function_name = tokens[position]
        args = []
        i = position + 2  # Skip the function name and opening parenthesis
        n = len(tokens)

        is_function_complete = False
        while i < n and not is_function_complete:
            token = tokens[i]
            if token == self._closing_parenthesis:
                is_function_complete = True
                i += 1
            elif token == PARAM_SEPARATOR:
                i += 1
            elif token in self._functions:
                arg, i = self._parse_function(tokens, i)
                args.append(arg)
            elif isinstance(token, Number):
                args.append(token)
                i += 1
            else:  # Cell reference or range
                if i + 1 < n and tokens[i + 1] == self._range_separator:
                    range_end = tokens[i + 2]
                    args.append(CellRange(token, range_end))
                    i += 3
                else:
                    args.append(token)  # Cell reference
                    i += 1

        function = FunctionFactory.create(function_name, args)
        return function, i

    def tokens_to_components(self, tokens: list[str]) -> list[FormulaComponent]:
        """Converts a list of tokens into Component objects."""
        components = []
        i = 0

        while i < len(tokens):
            token = tokens[i]
            if token in self._functions:
                function, i = self._parse_function(tokens, i)
                components.append(function)
            elif token in self._operators:
                components.append(BinaryOperatorFactory.create(token))
                i += 1
            elif token == self._opening_parenthesis:
                components.append(OpeningParenthesis())
                i += 1
            elif token == self._closing_parenthesis:
                components.append(ClosingParenthesis())
                i += 1
            else:
                components.append(token)
                i += 1

        return components
