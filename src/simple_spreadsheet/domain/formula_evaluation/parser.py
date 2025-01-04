from enum import Enum

from domain.coordinates import Coordinates
from domain.formula_evaluation.consts import Token, OPERATORS, UNARY_OPERATORS, SEPARATORS, FUNCTIONS


class FormulaTokenType(Enum):
    OPERAND = 0
    UNARY_OPERATOR = 1
    BINARY_OPERATOR = 2
    PARENTHESIS = 3


class FunctionTokenType(Enum):
    FUNCTION = 0
    NUMBER = 1
    CELL_REFERENCE = 2
    CELL_RANGE = 3
    SEPARATOR = 4


class Parser:
    def __init__(self) -> None:
        self.__tokens: list[Token] = []
        self.__stack: list[str] = []
        self.__operators = OPERATORS
        self.__unary_operators = UNARY_OPERATORS
        self.__separators = SEPARATORS
        self.__functions = FUNCTIONS

    def _is_function(self, token) -> bool:
        """Returns True if the token is a function."""
        return token in self.__functions

    def _is_cell_reference(self, token) -> bool:
        """Returns True if the token is a cell reference."""
        return isinstance(token, Coordinates)

    def _is_number(self, token) -> bool:
        """Returns True if the token is a numeric value."""
        return isinstance(token, float)

    def _is_operand(self, token) -> bool:
        """Returns True if the token is an operand."""
        return self._is_number(token) or self._is_cell_reference(token) or self._is_function(token)

    def _is_operator(self, token) -> bool:
        """Returns True if the token is an operator."""
        return token in self.__operators

    def _is_separator(self, token) -> bool:
        """Returns True if the token is a separator."""
        return token in self.__separators

    def _is_range_separator(self, token) -> bool:
        """Returns True if the token is a range separator."""
        return token == ':'

    def _validate_range(self, idx: int, last_element: FunctionTokenType) -> None:
        """Validates a range (e.g., A1:A2)."""
        tokens = self.__tokens
        if idx == 0 or idx + 1 >= len(tokens):
            raise SyntaxError(
                f"Range separator ':' at position {idx} is invalid")
        if last_element != FunctionTokenType.CELL_REFERENCE:
            raise SyntaxError(
                f"Range ':' must be preceded by a cell reference (position {idx})")
        if not self._is_cell_reference(tokens[idx + 1]):
            raise SyntaxError(
                f"Range ':' must be followed by a cell reference (position {idx})")

    def _validate_function(self, idx: int) -> int:
        """Validates a function token and returns the index after validation."""
        tokens: list[Token] = self.__tokens
        function: str = tokens[idx]
        n: int = len(tokens)

        if idx + 1 >= n or tokens[idx + 1] != '(':
            raise SyntaxError(f"Function '{function}' must be followed by '('")
        idx += 2  # Move past the opening parenthesis

        num_args: int = 0
        last_element: FunctionTokenType = FunctionTokenType.SEPARATOR

        while idx < n and tokens[idx] != ')':
            token = tokens[idx]
            if self._is_function(token):
                idx = self._validate_function(idx) - 1
                last_element = FunctionTokenType.FUNCTION
            elif self._is_number(token):
                if last_element != FunctionTokenType.SEPARATOR:
                    raise SyntaxError(f"Number at position {idx} \
                                        must be preceded by a separator")
                num_args += 1
                last_element = FunctionTokenType.NUMBER
            elif self._is_cell_reference(token):
                if last_element != FunctionTokenType.SEPARATOR:
                    raise SyntaxError(
                        f"Cell reference at position {idx} \
                          must be preceded by a separator")
                num_args += 1
                last_element = FunctionTokenType.CELL_REFERENCE
            elif token == ';':
                if last_element == FunctionTokenType.SEPARATOR:
                    raise SyntaxError(
                        f"Separator ';' at position {idx} must follow an operand")
                last_element = FunctionTokenType.SEPARATOR
            elif token == ':':
                self._validate_range(idx, last_element)
                last_element = FunctionTokenType.CELL_RANGE
                idx += 1
            idx += 1

        if idx >= n or tokens[idx] != ')':
            raise SyntaxError(
                f"'{function}' must end with ')'")

        if num_args == 0:
            raise SyntaxError(
                f"'{function}' must have at least one argument")

        return idx + 1  # Return position after the closing parenthesis

    def _validate_closing_parenthesis(self) -> None:
        """Validates a closing parenthesis."""
        if not self.__stack or self.__stack.pop() != '(':
            raise SyntaxError("Unmatched closing parenthesis")

    def _validate_operand(self, expect_operand) -> None:
        """Validates if an operand is allowed in the current context."""
        if not expect_operand:
            raise SyntaxError("Operand not allowed in this position")

    def _validate_operator(self, token, expect_operand) -> None:
        """Validates an operator token."""
        if token in self.__unary_operators and expect_operand:
            return  # Unary operator is valid in this case
        if expect_operand:
            raise SyntaxError(
                f"Operator '{token}' not allowed without preceding operand")

    def _validate_separator(self, index, tokens) -> None:
        """Validates a separator token."""
        if index == 0 or tokens[index - 1] in {'(', *self.__operators}:
            raise SyntaxError("Separator must follow an operand")
        if index + 1 >= len(tokens) or tokens[index + 1] in {')', *self.__operators}:
            raise SyntaxError("Separator must precede an operand")

    def _validate_final_state(self, expect_operand) -> None:
        """Validates the final state of the formula."""
        if self.__stack:
            raise SyntaxError("Unmatched opening parenthesis")
        if expect_operand:
            raise SyntaxError(
                "Formula cannot end with an operator or incomplete expression")

    def has_syntax_error(self, tokens: list[Token]) -> None:
        """
        Validates the given tokenized formula.
        Raises SyntaxError if invalid.
        """
        self.__tokens = tokens
        self.__stack.clear()

        n = len(tokens)
        i = 0

        last_element: FormulaTokenType = None

        while i < n:
            if self._is_function(tokens[i]):
                i = self._validate_function(i)
                last_element = FormulaTokenType.OPERAND
