from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .formula_evaluation.visitor import Visitor


class FormulaComponent(ABC):
    """Base class for formula components."""

    @abstractmethod
    def accept(self, visitor: 'Visitor') -> None:
        pass

    def get_dependencies(self) -> set:
        return set()


class Operand(FormulaComponent):
    """Base class for formula operands."""

    @abstractmethod
    def evaluate(self) -> float:
        pass

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_operand(self)


class Parenthesis(FormulaComponent):
    """Base class for parenthesis."""
    _symbol: str

    def __repr__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> str:
        return self._symbol


class OpeningParenthesis(Parenthesis):
    def __init__(self) -> None:
        self._symbol = '('

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_opening_parenthesis(self)


class ClosingParenthesis(Parenthesis):
    def __init__(self) -> None:
        self._symbol = ')'

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_closing_parenthesis(self)
