from ..spreadsheet import Spreadsheet
from ..functions import Function
from ..coordinates import Coordinates
from ..formula_component import ComponentType, FormulaComponent


class PostfixEvaluator:
    def evaluate(self, postfix: list[FormulaComponent], spreadsheet: Spreadsheet) -> float:
        stack = []
        for component in postfix:

            component_type = component.get_type() if not isinstance(
                component, float) else ComponentType.OPERAND

            if component_type == ComponentType.OPERAND:
                stack.append(component)
            elif component_type == ComponentType.OPERATOR:
                # Pop the required number of operands for the operator
                operand2 = stack.pop()
                operand1 = stack.pop()

                result = component.operate(operand1, operand2, spreadsheet)
                stack.append(result)

        if len(stack) != 1:
            raise ValueError(
                "Invalid postfix expression: stack does not contain exactly one element.")

        result = stack.pop()
        if isinstance(result, Function):
            return result.evaluate(spreadsheet)
        if isinstance(result, Coordinates):
            return spreadsheet.get_cell(result).get_value_as_float()

        return result
