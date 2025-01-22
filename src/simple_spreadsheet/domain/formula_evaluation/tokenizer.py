from typing import Union
from simple_spreadsheet.domain.coordinates import Coordinates
from .consts import Token, DECIMAL_SEPARATOR, SPECIAL_CHARS, FUNCTIONS


class Tokenizer:
    def __init__(self) -> None:
        self._tokens: list[Token] = []
        self._decimal_separator = DECIMAL_SEPARATOR
        self._special_chars = SPECIAL_CHARS
        self._functions = FUNCTIONS

    def _is_valid_numeric_char(self, char: str) -> bool:
        """Checks if a character is a digit or the decimal separator."""
        return char.isdigit() or char == self._decimal_separator

    def _extract_number(self, expression: str, start_index: int) -> tuple[float, int]:
        """Extracts a numeric token from the expression."""
        num = ''
        decimal_separator_seen = False
        n = len(expression)
        i = start_index
        while i < n and self._is_valid_numeric_char(expression[i]):
            if expression[i] == self._decimal_separator:
                if decimal_separator_seen:
                    raise ValueError(
                        'A number contains multiple decimal separators')
                decimal_separator_seen = True
            num += expression[i]
            i += 1
        return float(num), i

    def _extract_cell_or_function(self, expression: str, start_index: int) -> tuple[Union[str, Coordinates], int]:
        """Extracts a cell reference or function from the expression."""
        var = ''
        n = len(expression)
        i = start_index
        while i < n and (expression[i].isalpha() or expression[i].isdigit()):
            var += expression[i]
            i += 1

        if var.isalpha():  # All alphabetic characters
            upper_var = var.upper()
            if upper_var in self._functions:
                return upper_var, i
            raise ValueError(
                f'Invalid function "{var}" at position {start_index}')
        return Coordinates.from_id(var), i

    def tokenize(self, expression: str) -> list[Token]:
        """Tokenizes the given mathematical expression."""
        self._tokens = []
        n = len(expression)
        i = 0

        while i < n:
            char = expression[i]
            if char.isspace():
                i += 1
            elif self._is_valid_numeric_char(char):  # Handle numbers
                num, i = self._extract_number(expression, i)
                self._tokens.append(num)
            elif char.isalpha():  # Handle cells and functions
                var, i = self._extract_cell_or_function(expression, i)
                self._tokens.append(var)
            elif char in self._special_chars:  # Handle operators and delimiters
                self._tokens.append(char)
                i += 1
            else:  # Invalid character
                raise ValueError(f'Invalid character "{char}" at position {i}')

        return self._tokens

    def get_tokens(self) -> list[Union[str, float, Coordinates]]:
        """Returns the tokens generated by the last call to tokenize."""
        return self._tokens
