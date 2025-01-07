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
        self._ui = UserInterface(self._spreadsheet)

        self.edit_cell('A1', 'Prova')
        self.edit_cell('A5', '5')
        self.edit_cell('A6', 10)
        self.edit_cell('A7', 15)
        self.edit_cell('A8', 20)
        self.edit_cell('A9', 25)
        self.edit_cell('A10', 30)
        self.edit_cell('B5', '=SUMA(A5:A10)+10')

        self._ui.run()

    def edit_cell(self, cell_id: str, value: str) -> None:
        new_content = ContentFactory.create(value)
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
        self._spreadsheet.set_content(cell_id, new_content)
        # TODO: self._ui.update()
