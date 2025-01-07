from .tokenizer import Tokenizer
from .validator import Validator
from .parser import Parser
from .postfix_evaluator import PostfixEvaluator

from ..spreadsheet import Spreadsheet


class FormulaEvaluator:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()
        self._validator = Validator()
        self._parser = Parser()
        self._postfix_evaluator = PostfixEvaluator()

    def evaluate(self, formula: str, spreadsheet: Spreadsheet) -> float:
        tokens = self._tokenizer.tokenize(formula)
        print(tokens)
        self._validator.has_syntax_error(tokens)
        components = self._parser.tokens_to_components(tokens)
        print(components)
        postfix = self._parser.infix_to_postfix(components)
        print(postfix)
        result = self._postfix_evaluator.evaluate(postfix, spreadsheet)
        print(result)
