from abc import ABC, abstractmethod

from ..formula_components import FormulaComponent


class Visitor(ABC):
    @abstractmethod
    def visit_operand(self, operand: FormulaComponent) -> None:
        pass

    @abstractmethod
    def visit_operator(self, operator: FormulaComponent) -> None:
        pass

    @abstractmethod
    def visit_opening_parenthesis(self, opening_parenthesis: FormulaComponent) -> None:
        pass

    @abstractmethod
    def visit_closing_parenthesis(self, closing_parenthesis: FormulaComponent) -> None:
        pass
