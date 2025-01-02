from domain.coordinates import Coordinates
from domain.formula_evaluation.consts import Token, OPERATORS, FUNCTIONS


class Parser:
    def __init__(self) -> None:
        self.__operators = OPERATORS
        self.__functions = FUNCTIONS

    def _is_cell_reference(self, token) -> bool:
        """Returns True if the token is a cell reference."""
        return isinstance(token, Coordinates)

    def _is_number(self, token) -> bool:
        """Returns True if the token is a numeric value."""
        return isinstance(token, float)

    def _is_operator(self, token) -> bool:
        """Returns True if the token is an operator."""
        return token in self.__operators

    def _is_function(self, token) -> bool:
        """Returns True if the token is a function."""
        return token in self.__functions

    def has_syntax_error(self, tokens: list[Token]) -> None:
        """Checks if the given tokens have a syntax error."""
        n = len(tokens)
        if n == 0:
            return
        return
