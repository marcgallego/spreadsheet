from functools import singledispatchmethod

from domain.spreadsheet import Spreadsheet
from domain.contents import ContentFactory, ContentType
from domain.formula_evaluation import FormulaEvaluator
from framework.ui import UserInterface

# TODO: update formulas automatically when a cell is edited
# TODO: detect circular references


class Controller:

    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()
        self._ui = UserInterface(self)

        self.edit_cell(1, 1, 'Prova')
        self.edit_cell(1, 2, '5')
        self.edit_cell(2, 2, 10)
        self.edit_cell(3, 2, 15)
        self.edit_cell(4, 2, 20)
        self.edit_cell(5, 2, 25)
        self.edit_cell(6, 2, 30)
        self.edit_cell(7, 2, '=SUMA(A5:A10)+10')

        self._ui.run()

    def edit_cell(self, row, col, value: str) -> None:
        new_content = ContentFactory.create(value)
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
        self._spreadsheet.set_content(row, col, new_content)
        # TODO: self._ui.update()
