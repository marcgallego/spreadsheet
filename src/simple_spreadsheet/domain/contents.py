from abc import ABC, abstractmethod


class Content(ABC):
    @abstractmethod
    def set_value(self) -> None:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass

    def get_raw_value(self) -> float | str:
        return self.value


class ContentFactory():
    @staticmethod
    def create(value: str | int | float) -> Content:
        if isinstance(value, str) and value.startswith('='):
            return Formula(value)
        if isinstance(value, int) or isinstance(value, float):
            return Number(value)
        return Text(value)


class Formula(Content):
    def __init__(self, expression: str) -> None:
        self.expression = expression[1:] if \
            expression.startswith('=') else expression
        self.postfix = None
        self.value = None

    def __str__(self) -> str:
        return '=' + self.expression

    def set_value(self, expression: str) -> None:
        self.expression = expression

    def get_value(self) -> float:
        return self.value


class Number(Content):
    def __init__(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise ValueError('Value must be a number')
        self.value = float(value)

    def __str__(self) -> str:
        return str(self.value)

    def set_value(self, value: float) -> None:
        self.value = value

    def get_value(self) -> float:
        return self.value


class Text(Content):
    def __init__(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError('Value must be a string')
        self.value = value

    def __str__(self) -> str:
        return self.value

    def set_value(self, value: str) -> None:
        self.value = value

    def get_value(self) -> float:
        return float(self.value)
