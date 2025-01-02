from domain.coordinates import Coordinates
from domain.formula_evaluation.consts import Token, OPERATORS, UNARY_OPERATORS, SEPARATORS, FUNCTIONS


class FormulaSyntaxError(Exception):
    """Custom exception for formula syntax errors."""
    pass


class Parser:
    def __init__(self) -> None:
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

    def _validate_function(self, tokens, index) -> None:
        """Validates a function token."""
        if index + 1 >= len(tokens) or tokens[index + 1] != '(':
            raise FormulaSyntaxError(
                f"Function '{tokens[index]}' must be followed by '('")

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
        self.__stack.clear()
        expect_operand = True

        for i, token in enumerate(tokens):
            if self._is_function(token):
                self._validate_function(tokens, i)
                expect_operand = True
            elif token == '(':
                self.__stack.append(token)
                expect_operand = True
            elif token == ')':
                self._validate_closing_parenthesis()
                expect_operand = False
            elif self._is_cell_reference(token) or self._is_number(token):
                self._validate_operand(expect_operand)
                expect_operand = False
            elif self._is_operator(token):
                self._validate_operator(token, expect_operand)
                expect_operand = True
            elif self._is_separator(token):
                self._validate_separator(i, tokens)
            else:
                raise FormulaSyntaxError(f"Unexpected token: {token}")

        self._validate_final_state(expect_operand)
