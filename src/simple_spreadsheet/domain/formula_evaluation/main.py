from .tokenizer import Tokenizer
from .validator import Validator
from .parser import Parser


class FormulaEvaluator:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()
        self._validator = Validator()
        self._parser = Parser()

    def evaluate(self, formula: str) -> float:
        tokens = self._tokenizer.tokenize(formula)
        print(tokens)
        self._validator.has_syntax_error(tokens)
        components = self._parser.tokens_to_components(tokens)
        print(components)
        postfix = self._parser.infix_to_postfix(components)
        print(postfix)
