from abc import abstractmethod

from .formula_component import FormulaComponent, ComponentType


class Operand(FormulaComponent):
    """Base class for formula operands."""
    _type = ComponentType.OPERAND

    @abstractmethod
    def evaluate(self) -> float:
        pass

    @abstractmethod
    def get_dependencies(self) -> set:
        pass

    def accept(self, visitor: 'Visitor') -> None:
        visitor.visit_operand(self)
