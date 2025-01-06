from enum import Enum, auto
from typing import Optional
from domain.coordinates import Coordinates
from .consts import Token, OPERATORS, UNARY_OPERATORS, SEPARATORS, FUNCTIONS, RANGE_SEPARATOR, PARAM_SEPARATOR


class FormulaTokenType(Enum):
    """Types of tokens in a formula expression."""
    OPERAND = auto()
    UNARY_OPERATOR = auto()
    BINARY_OPERATOR = auto()
    PARENTHESIS = auto()


class FunctionTokenType(Enum):
    """Types of tokens within a function call."""
    FUNCTION = auto()
    UNARY_OPERATOR = auto()
    NUMBER = auto()
    CELL_REFERENCE = auto()
    CELL_RANGE = auto()
    SEPARATOR = auto()


class Validator:
    """Validator for spreadsheet formulas with support for functions, ranges, and operators."""

    def __init__(self) -> None:
        self._tokens: list[Token] = []
        self._pos: int = 0
        # Using frozen sets for immutable constant collections
        self._operators = frozenset(OPERATORS)
        self._unary_operators = frozenset(UNARY_OPERATORS)
        self._separators = frozenset(SEPARATORS)
        self._functions = frozenset(FUNCTIONS)
        self._range_separator = RANGE_SEPARATOR
        self._param_separator = PARAM_SEPARATOR

    def _is_token_type(self, token: Token, collection: frozenset) -> bool:
        """Generic token type checker."""
        return token in collection

    def _is_function(self, token: Token) -> bool:
        """Check if token is a function name."""
        return self._is_token_type(token, self._functions)

    def _is_cell_reference(self, token: Token) -> bool:
        """Check if token is a cell reference."""
        return isinstance(token, Coordinates)

    def _is_number(self, token: Token) -> bool:
        """Check if token is a numeric value."""
        return isinstance(token, float)

    def _is_operator(self, token: Token) -> bool:
        """Check if token is an operator."""
        return self._is_token_type(token, self._operators)

    def _can_be_unary_operator(self, token: Token) -> bool:
        """Check if token can be used as a unary operator."""
        return self._is_token_type(token, self._unary_operators)

    def _is_separator(self, token: Token) -> bool:
        """Check if token is an argument separator."""
        return self._is_token_type(token, self._separators)

    def _peek(self) -> Optional[Token]:
        """Look at current token without consuming it."""
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self) -> Optional[Token]:
        """Consume and return current token."""
        token = self._peek()
        if token is not None:
            self._pos += 1
        return token

    def _validate_range(self, last_element: FunctionTokenType) -> None:
        """Validate a cell range expression (e.g., A1:A2)."""
        if self._pos == 0 or self._pos >= len(self._tokens):
            raise SyntaxError(
                f"Invalid range separator at position {self._pos}")

        if last_element != FunctionTokenType.CELL_REFERENCE:
            raise SyntaxError(
                f"Range must be preceded by a cell reference (position {self._pos})")

        next_token = self._peek()
        if not self._is_cell_reference(next_token):
            raise SyntaxError(
                f"Range must be followed by a cell reference (position {self._pos})")

        self._consume()

    def _parse_function_arguments(self) -> int:
        """Parse function arguments and return count."""
        num_args = 0
        last_element = FunctionTokenType.SEPARATOR

        while (token := self._peek()) is not None and token != ')':
            if token == self._param_separator:
                if last_element == FunctionTokenType.SEPARATOR:
                    raise SyntaxError(
                        f"Invalid separator at position {self._pos}")
                self._consume()
                last_element = FunctionTokenType.SEPARATOR
            else:
                if self._is_function(token):
                    self._parse_function()
                    last_element = FunctionTokenType.FUNCTION
                elif self._can_be_unary_operator(token):
                    if last_element != FunctionTokenType.SEPARATOR:
                        raise SyntaxError(
                            f"Unary operator must be preceded by a separator at position {self._pos}")
                    self._consume()
                    last_element = FunctionTokenType.UNARY_OPERATOR
                    if not self._is_number(self._peek()):
                        raise SyntaxError(
                            f"Inside functions, unary operators must be followed by a number at position {self._pos}")
                elif self._is_number(token):
                    if last_element != FunctionTokenType.SEPARATOR and last_element != FunctionTokenType.UNARY_OPERATOR:
                        raise SyntaxError(
                            f"Number must be preceded by a separator at position {self._pos}")
                    self._consume()
                    num_args += 1
                    last_element = FunctionTokenType.NUMBER
                elif self._is_cell_reference(token):
                    if last_element != FunctionTokenType.SEPARATOR:
                        raise SyntaxError(
                            f"Cell reference must be preceded by a separator at position {self._pos}")
                    self._consume()
                    num_args += 1
                    last_element = FunctionTokenType.CELL_REFERENCE

                    if self._peek() == self._range_separator:
                        self._consume()
                        self._validate_range(last_element)
                        last_element = FunctionTokenType.CELL_RANGE
                else:
                    raise SyntaxError(f"Unexpected token '{
                                      token}' at position {self._pos}")

        return num_args

    def _parse_function(self) -> None:
        """Parse a function call including its arguments."""
        function_name = self._consume()

        if self._peek() != '(':
            raise SyntaxError(
                f"Function '{function_name}' must be followed by '('")
        self._consume()

        num_args = self._parse_function_arguments()

        if self._peek() != ')':
            raise SyntaxError(
                f"Function '{function_name}' missing closing parenthesis")
        self._consume()

        if num_args == 0:
            raise SyntaxError(
                f"Function '{function_name}' requires at least one argument")

    def _parse_primary(self) -> None:
        """Parse primary expressions (numbers, cell refs, functions, parenthesized expressions)."""
        if (token := self._peek()) is None:
            raise SyntaxError("Unexpected end of formula")

        if self._is_number(token) or self._is_cell_reference(token):
            self._consume()
            return

        if self._is_function(token):
            self._parse_function()
            return

        if token == '(':
            self._consume()
            self._parse_expression()

            if self._peek() != ')':
                raise SyntaxError(
                    f"Missing closing parenthesis at position {self._pos}")
            self._consume()
            return

        raise SyntaxError(f"Unexpected token '{
                          token}' at position {self._pos}")

    def _parse_unary(self) -> None:
        """Parse unary operators, supporting multiple consecutive unary operators."""
        unary_count = 0

        while (token := self._peek()) and self._can_be_unary_operator(token):
            self._consume()
            unary_count += 1

        # After consuming all unary operators, process the primary expression.
        self._parse_primary()

    def _parse_binary_operation(self) -> None:
        """Parse binary operations with operator precedence."""
        self._parse_unary()

        while (op := self._peek()) is not None and self._is_operator(op):
            self._consume()
            self._parse_unary()

    def _parse_expression(self) -> None:
        """Parse a complete expression."""
        self._parse_binary_operation()

    def has_syntax_error(self, tokens: list[Token]) -> None:
        """
        Validate the given tokenized formula.
        Raises SyntaxError if invalid.
        """
        if not tokens:
            raise SyntaxError("Empty formula")

        self._tokens = tokens
        self._pos = 0

        try:
            self._parse_expression()

            if self._peek() is not None:
                raise SyntaxError(f"Unexpected token '{
                                  self._peek()}' at position {self._pos}")

        except SyntaxError:
            raise
        except Exception as e:
            raise SyntaxError(f"Invalid formula: {str(e)}")
