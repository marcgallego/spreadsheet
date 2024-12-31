from typing import Union
from domain.coordinates import Coordinates

OPERATORS_AND_DELIMITERS = ['+', '-', '*', '/', '(', ')', ':', ';']
FORMULAS = ['SUMA', 'PROMEDIO', 'MAX', 'MIN']
DECIMAL_SEPARATOR = '.'


class Tokenizer:
    def __init__(self) -> None:
        self.__tokens = []

    def _preprocess(self, expression) -> str:
        expression = expression.replace(' ', '')
        return expression

    def _is_digit_or_separator(self, char) -> bool:
        return char.isdigit() or char == DECIMAL_SEPARATOR

    def tokenize(self, expression) -> list[Union[str, Coordinates]]:
        self.__tokens = []
        expression = self._preprocess(expression)
        n = len(expression)
        i = 0
        while i < n:
            if expression[i].isdigit():
                num = ''
                while i < n and self._is_digit_or_separator(expression[i]):
                    if expression[i] == DECIMAL_SEPARATOR and DECIMAL_SEPARATOR in num:
                        raise ValueError(
                            f'Invalid number in expression (position {i})')
                    num += expression[i]
                    i += 1
                self.__tokens.append(num)
            elif expression[i].isalpha():
                var = ''
                while i < n and (expression[i].isalpha() or expression[i].isdigit()):
                    var += expression[i]
                    i += 1
                if var.isalpha():
                    if var.upper() in FORMULAS:
                        self.__tokens.append(var.upper())
                    else:
                        raise ValueError(
                            f'Invalid formula "{var}" in expression')
                else:
                    self.__tokens.append(Coordinates.from_id(var))
            elif expression[i] in OPERATORS_AND_DELIMITERS:
                self.__tokens.append(expression[i])
                i += 1
            else:
                char = expression[i]
                raise ValueError(f'Invalid character "{char}" in expression')
        return self.__tokens

    def get_tokens(self) -> list[Union[str, Coordinates]]:
        return self.__tokens
