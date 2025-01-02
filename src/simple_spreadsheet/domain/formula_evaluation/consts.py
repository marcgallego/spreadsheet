from typing import Union
from domain.coordinates import Coordinates

type Token = Union[str, float, Coordinates]

OPERATORS = {'+', '-', '*', '/'}
UNARY_OPERATORS = {'+', '-'}
RANGE_SEPARATOR = ':'
PARAM_SEPARATOR = ';'
SEPARATORS = {RANGE_SEPARATOR, PARAM_SEPARATOR}
DELIMITERS = {'(', ')', ':', ';'}  # TODO: fix duplicity
OPERATORS_AND_DELIMITERS = OPERATORS.union(DELIMITERS)
FUNCTIONS = {'SUMA', 'PROMEDIO', 'MAX', 'MIN'}
DECIMAL_SEPARATOR = '.'
