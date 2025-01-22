from typing import Union
from simple_spreadsheet.domain.coordinates import Coordinates

type Token = Union[str, float, Coordinates]

FUNCTIONS = frozenset({'SUMA', 'PROMEDIO', 'MAX', 'MIN'})

OPERATORS = frozenset({'+', '-', '*', '/'})
UNARY_OPERATORS = {'+', '-'}  # Only used for numbers

DECIMAL_SEPARATOR = '.'
RANGE_SEPARATOR = ':'
PARAM_SEPARATOR = ';'
SEPARATORS = frozenset({RANGE_SEPARATOR, PARAM_SEPARATOR})

DELIMITERS = frozenset({'(', ')'})

SPECIAL_CHARS = OPERATORS | SEPARATORS | DELIMITERS
