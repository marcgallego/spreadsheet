from abc import ABC, abstractmethod
from enum import Enum, auto

from .formula_component import FormulaComponent, ComponentType
from .coordinates import Coordinates


class ContentType(Enum):
    TEXT = auto()
    NUMBER = auto()
    FORMULA = auto()


class Content(ABC):
    _type: ContentType

    @abstractmethod
    def set_value(self) -> None:
        pass

    @abstractmethod
    def get_value_as_float(self) -> float:
        pass

    def get_value_as_str(self) -> str:
        return str(self._value)

    @property
    def type(self) -> ContentType:
        return self._type


class ContentFactory():
    @staticmethod
    def create(value: str | int | float) -> Content:
        if isinstance(value, str) and value.startswith('='):
            return Formula(value)
        if isinstance(value, int) or isinstance(value, float):
            return Number(value)
        return Text(value)


class Formula(Content):
    _type = ContentType.FORMULA

    def __init__(self, expression: str) -> None:
        if not isinstance(expression, str):
            raise ValueError('Expression must be a string')

        self._expression = expression[1:]
        self._postfix = None
        self._value = None

    def __str__(self) -> str:
        return '=' + self._expression

    def set_expression(self, expression: str) -> None:
        self._expression = expression

    def get_expression(self) -> str:
        return self._expression

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
            if not isinstance(component, float) and component.get_type() == ComponentType.OPERAND:
                dependencies.update(component.get_dependencies())

        return dependencies

    # TODO: caldrà implementar un mètode per a gravar com a fitxer


class Number(Content):
    _type = ContentType.NUMBER

    def __init__(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise ValueError('Value must be a number')
        self._value = float(value)

    def __str__(self) -> str:
        return str(self._value)

    def set_value(self, value: float) -> None:
        self._value = value

    def get_value_as_float(self) -> float:
        return self._value


class Text(Content):
    _type = ContentType.TEXT

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
            return 0.0
        try:
            return float(self._value)
        except:
            raise ValueError('Some text cannot be converted to float')
