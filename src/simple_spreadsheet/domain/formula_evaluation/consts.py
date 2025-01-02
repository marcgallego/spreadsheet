from typing import Union
from domain.coordinates import Coordinates

type Token = Union[str, float, Coordinates]

OPERATORS = {'+', '-', '*', '/'}
DELIMITERS = {'(', ')', ':', ';'}
OPERATORS_AND_DELIMITERS = OPERATORS.union(DELIMITERS)
FUNCTIONS = {'SUMA', 'PROMEDIO', 'MAX', 'MIN'}
DECIMAL_SEPARATOR = '.'
