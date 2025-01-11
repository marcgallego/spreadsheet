
from .tokenizer import Tokenizer
from .validator import Validator
from .parser import Parser
from .postfix_evaluator import PostfixEvaluator

from ..contents import Formula
from ..spreadsheet import Spreadsheet


class FormulaEvaluator:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()
        self._validator = Validator()
        self._parser = Parser()
        self._postfix_evaluator = PostfixEvaluator()

    def evaluate(self, formula: Formula, spreadsheet: Spreadsheet) -> None:
        postfix = formula.get_postfix()
        if postfix is None:
            tokens = self._tokenizer.tokenize(formula.expression)
            self._validator.has_syntax_error(tokens)
            components = self._parser.tokens_to_components(tokens)
            postfix = self._parser.infix_to_postfix(components)
            formula.set_postfix(postfix)
        value = self._postfix_evaluator.evaluate(postfix, spreadsheet)
        formula.set_value(value)
