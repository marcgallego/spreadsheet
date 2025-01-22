from typing import Union
from simple_spreadsheet.domain.coordinates import Coordinates

type Token = Union[str, float, Coordinates]

FUNCTIONS = frozenset({'SUMA', 'PROMEDIO', 'MAX', 'MIN'})

PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
}
OPERATORS = frozenset(PRECEDENCE.keys())
UNARY_OPERATORS = frozenset({'+', '-'})  # Only used for numbers

DECIMAL_SEPARATOR = '.'
RANGE_SEPARATOR = ':'
PARAM_SEPARATOR = ';'
SEPARATORS = frozenset({RANGE_SEPARATOR, PARAM_SEPARATOR})

OPENING_PARENTHESIS = '('
CLOSING_PARENTHESIS = ')'
PARENTHESES = frozenset({OPENING_PARENTHESIS, CLOSING_PARENTHESIS})

SPECIAL_CHARS = OPERATORS | SEPARATORS | PARENTHESES
