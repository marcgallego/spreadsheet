from functools import singledispatchmethod

from simple_spreadsheet.domain.spreadsheet import Spreadsheet
from simple_spreadsheet.domain.coordinates import Coordinates
from simple_spreadsheet.domain.contents import ContentFactory, ContentType
from simple_spreadsheet.framework.ui import UserInterface
from simple_spreadsheet.domain.formula_evaluation import FormulaEvaluator
from simple_spreadsheet.domain.update_manager import UpdateManager

# TODO: update formulas automatically when a cell is edited
# TODO: detect circular references


class Controller:

    def __init__(self) -> None:
        self._update_manager = UpdateManager()
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()
        self._ui = UserInterface(self)

        self.edit_cell('A1', 'Prova')
        self.edit_cell('B2', '5')
        self.edit_cell('B3', 10)
        self.edit_cell('B4', 15)
        self.edit_cell('B10', '=PROMEDIO(B2:B7)')
        self.edit_cell('B5', 20)
        self.edit_cell('B6', 25)
        self.edit_cell('B11', '=MAX(B2:B7)')
        self.edit_cell('B12', '=MIN(B2:B7)')
        self.edit_cell('B13', '=SUMA(B10:B12)')

        # TODO: posar negreta a l'eix de les columnes
        self._ui.run()

    def create_new_spreadsheet(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._update_manager = UpdateManager()

    def _recompute_cells(self, cells: list[Coordinates]) -> None:
        for cell in cells:
            content = self._spreadsheet.get_cell(cell).get_content()
            if content.type == ContentType.FORMULA:
                self._formula_evaluator.evaluate(content, self._spreadsheet)
                self._spreadsheet.set_content(cell, content)
                # TODO: try is just while testing
                try:
                    self._ui.update_cell_view(cell, content.get_raw_value())
                except:
                    pass
                dependants = self._update_manager.get_dependents(cell)
                self._recompute_cells(dependants)

    def _create_and_assign_content(self, coords: Coordinates, value: str) -> None:
        new_content = ContentFactory.create(value)
        dependencies = None
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
            dependencies = new_content.get_dependencies()
        self._spreadsheet.set_content(coords, new_content)
        self._update_manager.set_dependencies(coords, dependencies)
        self._recompute_cells(self._update_manager.get_dependents(coords))

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

    @property
    def spreadsheet(self) -> Spreadsheet:
        return self._spreadsheet
