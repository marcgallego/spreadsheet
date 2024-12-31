from typing import Union
from domain.coordinates import Coordinates

FORMULAS = ['SUMA', 'PROMEDIO', 'MAX', 'MIN']


class Tokenizer:
    def __init__(self) -> None:
        self.__tokens = []

    def _preprocess(self, expression) -> None:
        expression = expression.replace(' ', '')
        return expression

    def tokenize(self, expression) -> list[Union[str, Coordinates]]:
        self.__tokens = []
        expression = self._preprocess(expression)
        n = len(expression)
        i = 0
        while i < n:
            if expression[i].isdigit():
                num = ''
                while i < n and expression[i].isdigit():
                    num += expression[i]
                    i += 1
                self.__tokens.append(num)
            elif expression[i].isalpha():
                var = ''
                while i < n and expression[i].isalpha() or expression[i].isdigit():
                    var += expression[i]
                    i += 1
                if var.isalpha() and var.upper() in FORMULAS:
                    self.__tokens.append(var.upper())
                else:
                    self.__tokens.append(Coordinates.from_id(var))
            elif expression[i] in ['+', '-', '*', '/', '(', ')', ':', ';']:
                self.__tokens.append(expression[i])
                i += 1
            else:
                char = expression[i]
                raise ValueError(f'Invalid character "{char}" in expression')
        return self.__tokens

    def get_tokens(self) -> list[Union[str, Coordinates]]:
        return self.__tokens
