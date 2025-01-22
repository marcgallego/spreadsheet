from abc import ABC, abstractmethod

from .formula_component import FormulaComponent, ComponentType
from .coordinates import Coordinates


class Content(ABC):
    """Base class for cell contents."""

    @abstractmethod
    def set_value(self) -> None:
        pass

    @abstractmethod
    def get_value_as_float(self) -> float:
        pass

    def get_value_as_str(self) -> str:
        return str(self._value)

    def is_formula(self) -> bool:
        return False


class ContentFactory():
    @staticmethod
    def create(value: str | int | float) -> Content:
        if isinstance(value, str) and value.startswith('='):
            return Formula(value)
        try:
            return Number(value)
        except ValueError:
            return Text(value)


class Formula(Content):
    def __init__(self, expression: str) -> None:
        if not isinstance(expression, str):
            raise ValueError('Expression must be a string')

        self._expression = expression[1:]
        self._postfix = None
        self._value = None

    def set_expression(self, expression: str) -> None:
        self._expression = expression

    @property
    def expression(self) -> str:
        return '=' + self._expression

    def __str__(self) -> str:
        return self.expression

    def set_postfix(self, postfix: list[FormulaComponent]) -> None:
        self._postfix = postfix

    def get_postfix(self) -> list[FormulaComponent]:
        return self._postfix

    def set_value(self, value: float) -> None:
        self._value = value

    def get_value_as_float(self) -> float:
        return self._value

    def get_dependencies(self) -> set[Coordinates]:
        dependencies = set()
        for component in self._postfix:
            if component.get_type() == ComponentType.OPERAND:
                dependencies.update(component.get_dependencies())

        return dependencies

    def is_formula(self) -> bool:
        return True


class Number(Content, FormulaComponent):
    _type = ComponentType.OPERAND

    def __init__(self, value: float | int | str) -> None:
        self._value = float(value)

    def __str__(self) -> str:
        return str(self._value)

    def set_value(self, value: float) -> None:
        self._value = value

    def get_value_as_float(self) -> float:
        return self._value

    def get_dependencies(self) -> set[Coordinates]:
        return set()


class Text(Content):
    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError('Value must be a string')
        self._value = value

    def __str__(self) -> str:
        return self._value

    def set_value(self, value: str) -> None:
        self._value = value

    def get_value_as_float(self) -> float:
        if not self._value:
            return None
        try:
            return float(self._value)
        except:
            raise ValueError(
                f'("{self._value}") is of type text and cannot be converted to float')
