
from .tokenizer import Tokenizer
from .validator import Validator
from .parser import Parser
from .converter import Converter
from .postfix_evaluator import PostfixEvaluator

from ..contents import Formula
from ..formula_components import FormulaComponent
from ..spreadsheet import Spreadsheet


class FormulaEvaluator:
    def __init__(self) -> None:
        self._tokenizer = Tokenizer()
        self._validator = Validator()
        self._parser = Parser()
        self._converter = Converter()

    def get_postfix(self, formula: Formula) -> list[FormulaComponent]:
        postfix = formula.get_postfix()
        if postfix is None:
            expression = formula.expression[1:]  # remove '='
            tokens = self._tokenizer.tokenize(expression)
            self._validator.has_syntax_error(tokens)
            components = self._parser.tokens_to_components(tokens)
            postfix = self._converter.infix_to_postfix(components)
            formula.set_postfix(postfix)

        return postfix

    def evaluate(self, formula: Formula, spreadsheet: Spreadsheet) -> None:
        postfix = self.get_postfix(formula)
        value = PostfixEvaluator(spreadsheet).evaluate(postfix)
        formula.set_value(value)
