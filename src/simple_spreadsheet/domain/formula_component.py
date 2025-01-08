from abc import ABC
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

    def get_type(self) -> str:
        """Return the type of the component."""
        return self._type


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
