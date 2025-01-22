from functools import singledispatchmethod

from ..domain.spreadsheet import Spreadsheet
from ..domain.coordinates import Coordinates
from ..domain.contents import ContentFactory
from ..domain.formula_evaluation import FormulaEvaluator
from ..domain.dependency_manager import DependencyManager
from ..framework.ui import UserInterface
from ..framework.file_manager import FileManager


class Controller:

    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()
        self._deps_manager = DependencyManager()
        self._file_manager = FileManager()
        self._ui = UserInterface(self)
        self._ui.run()

    def create_new_spreadsheet(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._deps_manager = DependencyManager()

    def _recompute_cells(self, cells: list[Coordinates]) -> None:
        for cell in cells:
            content = self._spreadsheet.get_cell(cell).get_content()
            if content.is_formula():
                self._formula_evaluator.evaluate(content, self._spreadsheet)
                self._spreadsheet.set_content(cell, content)
                self._ui.update_cell_view(cell, content.get_value_as_str())
                dependants = self._deps_manager.get_dependents(cell)
                self._recompute_cells(dependants)

    def _create_and_assign_content(self, coords: Coordinates, value: str) -> None:
        new_content = ContentFactory.create(value)
        dependencies = None
        if new_content.is_formula():
            self._formula_evaluator.get_postfix(new_content)
            dependencies = new_content.get_dependencies()
            self._deps_manager.has_circular_dependency(coords, dependencies)
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
        self._spreadsheet.set_content(coords, new_content)
        self._deps_manager.set_dependencies(coords, dependencies)
        self._recompute_cells(self._deps_manager.get_dependents(coords))

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

    def save_spreadsheet(self, file_path: str) -> None:
        self._file_manager.save(self._spreadsheet, file_path)

    def load_spreadsheet(self, file_path: str) -> None:
        spreadsheet, coords_with_formulas = self._file_manager.read(file_path)
        self._formula_evaluator = FormulaEvaluator()
        self._deps_manager = DependencyManager()
        self._spreadsheet = spreadsheet
        self._recompute_cells(coords_with_formulas)

    @property
    def spreadsheet(self) -> Spreadsheet:
        return self._spreadsheet
