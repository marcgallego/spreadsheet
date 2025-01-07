from typing import Union
from simple_spreadsheet.domain.coordinates import Coordinates

type Token = Union[str, float, Coordinates]

FUNCTIONS = {'SUMA', 'PROMEDIO', 'MAX', 'MIN'}

OPERATORS = {'+', '-', '*', '/'}
UNARY_OPERATORS = {'+', '-'}

DECIMAL_SEPARATOR = '.'
RANGE_SEPARATOR = ':'
PARAM_SEPARATOR = ';'
SEPARATORS = {RANGE_SEPARATOR, PARAM_SEPARATOR}

DELIMITERS = {'(', ')'}

SPECIAL_CHARS = OPERATORS | SEPARATORS | DELIMITERS
