from functools import singledispatchmethod

from domain.spreadsheet import Spreadsheet
from domain.coordinates import Coordinates
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

        self.edit_cell('A1', 'Prova')
        self.edit_cell('B2', '5')
        self.edit_cell('B3', 10)
        self.edit_cell('B4', 15)
        self.edit_cell('B5', 20)
        self.edit_cell('B6', 25)
        self.edit_cell('B7', 30)
        self.edit_cell('B10', '=SUMA(A5:A10)+10')

        self._ui.run()

    def _create_and_assign_content(self, coords: Coordinates, value: str) -> None:
        new_content = ContentFactory.create(value)
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
        self._spreadsheet.set_content(coords, new_content)

    @singledispatchmethod
    def edit_cell(self, _) -> None:
        raise NotImplementedError("Unsupported type")

    @edit_cell.register
    def _(self, cell_id: str, value: str) -> None:
        coords = Coordinates.from_id(cell_id)
        self._create_and_assign_content(coords, value)

    @edit_cell.register
    def _(self, row: int, col: int, value: str) -> None:
        coords = Coordinates(row, col)
        self._create_and_assign_content(coords, value)
