from abc import ABC, abstractmethod
from enum import Enum, auto


class ComponentType(Enum):
    """Types of components in a formula."""
    OPERATOR = auto()
    OPERAND = auto()
    OPENING_PARENTHESIS = auto()
    CLOSING_PARENTHESIS = auto()


class FormulaComponent(ABC):
    """Base class for formula components."""
    _type: ComponentType

    @property
    def type(self) -> ComponentType:
        return self._type


class Operand(FormulaComponent):
    """Base class for formula operands."""
    _type = ComponentType.OPERAND

    @abstractmethod
    def evaluate(self) -> float:
        pass

    @abstractmethod
    def get_dependencies(self) -> set:
        pass


class OpeningParenthesis(FormulaComponent):
    _type = ComponentType.OPENING_PARENTHESIS

    def __init__(self) -> None:
        self._symbol = '('

    def __repr__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> str:
        return self._symbol


class ClosingParenthesis(FormulaComponent):
    _type = ComponentType.CLOSING_PARENTHESIS

    def __init__(self) -> None:
        self._symbol = ')'

    def __repr__(self) -> str:
        return self._symbol

    @property
    def symbol(self) -> str:
        return self._symbol
