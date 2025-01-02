from domain.coordinates import Coordinates
from domain.formula_evaluation.consts import Token, OPERATORS, UNARY_OPERATORS, SEPARATORS, FUNCTIONS


class FormulaSyntaxError(Exception):
    """Custom exception for formula syntax errors."""
    pass


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

    def _is_operator(self, token) -> bool:
        """Returns True if the token is an operator."""
        return token in self.__operators

    def _is_separator(self, token) -> bool:
        """Returns True if the token is a separator."""
        return token in self.__separators

    def _is_range_separator(self, token) -> bool:
        """Returns True if the token is a range separator."""
        return token == ':'

    def _validate_function(self, idx) -> int:
        """Validates a function token."""
        tokens = self.__tokens
        function = tokens[idx]
        n = len(tokens)
        if idx + 1 >= n or tokens[idx + 1] != '(':
            raise FormulaSyntaxError(
                f"Function '{function}' must be followed by '('")
        idx += 2

        num_args = 0
        last_element = 'separator'
        while idx < n and tokens[idx] != ')':
            if self._is_function(tokens[idx]):
                idx = self._validate_function(idx) - 1
                last_element = 'function'
            elif self._is_number(tokens[idx]):
                if last_element != 'separator':
                    raise FormulaSyntaxError(
                        f"Number at position {idx} must be preceded by a separator")
                num_args += 1
                last_element = 'number'
            elif self._is_cell_reference(tokens[idx]):
                if last_element != 'separator':
                    raise FormulaSyntaxError(
                        f"Cell reference at position {idx} must be preceded by a separator")
                num_args += 1
                last_element = 'cell reference'
            elif tokens[idx] == ';':
                last_element = 'separator'
            elif tokens[idx] == ':':
                if last_element != 'cell reference' or \
                        (idx + 1 >= n or not self._is_cell_reference(tokens[idx + 1])):
                    raise FormulaSyntaxError(
                        f"Range ':' must be between two cell references (position {idx})")
                if idx + 2 < n and tokens[idx + 2] == ':':
                    raise FormulaSyntaxError(
                        f"Multiple range separators at position {idx}")
                idx += 1
                last_element = 'cell range'
            idx += 1

        if idx >= n or tokens[idx] != ')':
            raise FormulaSyntaxError(
                f"Function '{function}' must end with ')'")

        if num_args == 0:
            raise FormulaSyntaxError(
                f"Function '{function}' must have at least one argument")

        return idx + 1

    def _validate_closing_parenthesis(self) -> None:
        """Validates a closing parenthesis."""
        if not self.__stack or self.__stack.pop() != '(':
            raise FormulaSyntaxError("Unmatched closing parenthesis")

    def _validate_operand(self, expect_operand) -> None:
        """Validates if an operand is allowed in the current context."""
        if not expect_operand:
            raise FormulaSyntaxError("Operand not allowed in this position")

    def _validate_operator(self, token, expect_operand) -> None:
        """Validates an operator token."""
        if token in self.__unary_operators and expect_operand:
            return  # Unary operator is valid in this case
        if expect_operand:
            raise FormulaSyntaxError(
                f"Operator '{token}' not allowed without preceding operand")

    def _validate_separator(self, index, tokens) -> None:
        """Validates a separator token."""
        if index == 0 or tokens[index - 1] in {'(', *self.__operators}:
            raise FormulaSyntaxError("Separator must follow an operand")
        if index + 1 >= len(tokens) or tokens[index + 1] in {')', *self.__operators}:
            raise FormulaSyntaxError("Separator must precede an operand")

    def _validate_range(self, tokens, index) -> None:
        """Validates a range (e.g., A1:A2)."""
        if index == 0 or index + 1 >= len(tokens):
            raise FormulaSyntaxError(
                f"Range separator ':' at position {index} is invalid")
        if not self._is_cell_reference(tokens[index - 1]) or not self._is_cell_reference(tokens[index + 1]):
            raise FormulaSyntaxError(
                f"Range ':' must be between two cell references (position {index})")

    def _validate_final_state(self, expect_operand) -> None:
        """Validates the final state of the formula."""
        if self.__stack:
            raise FormulaSyntaxError("Unmatched opening parenthesis")
        if expect_operand:
            raise FormulaSyntaxError(
                "Formula cannot end with an operator or incomplete expression")

    def has_syntax_error(self, tokens: list[Token]) -> None:
        """
        Validates the given tokenized formula.
        Raises FormulaSyntaxError if invalid.
        """
        self.__tokens = tokens
        self.__stack.clear()

        n = len(tokens)
        print(n)
        i = 0
        while i < n:
            if self._is_function(tokens[i]):
                i = self._validate_function(i)
                print('Function validated')
                print(i)
