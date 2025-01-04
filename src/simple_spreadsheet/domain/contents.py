from abc import ABC, abstractmethod


class Content(ABC):
    @abstractmethod
    def set_value(self) -> None:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass


class Formula(Content):
    def __init__(self, expression: str) -> None:
        self.expression = expression
        self.postfix = None
        self.value = None

    def __str__(self) -> str:
        return '=' + self.expression

    def set_value(self, expression: str) -> None:
        self.expression = expression

    def get_value(self) -> float:
        return self.value


class Number(Content):
    def __init__(self, value: float) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def set_value(self, value: float) -> None:
        self.value = value

    def get_value(self) -> float:
        return self.value


class Text(Content):
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def set_value(self, value: str) -> None:
        self.value = value

    def get_value(self) -> float:
        return float(self.value)
