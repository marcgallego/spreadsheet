
from ..domain.spreadsheet import Spreadsheet
from ..domain.coordinates import Coordinates
from ..domain.contents import ContentFactory
from ..domain.formula_evaluation import FormulaEvaluator
from ..domain.dependency_manager import DependencyManager
from ..framework.file_manager import FileManager

from tests.automatic_grader.usecasesmarker import ISpreadsheetControllerForChecker
from tests.automatic_grader.entities.no_number_exception import NoNumberException


class ControllerForChecker(ISpreadsheetControllerForChecker):
    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()
        self._deps_manager = DependencyManager()
        self._file_manager = FileManager()

    def _recompute_cells(self, cells: list[Coordinates]) -> None:
        for cell in cells:
            content = self._spreadsheet.get_cell(cell).get_content()
            if content.is_formula():
                self._formula_evaluator.evaluate(content, self._spreadsheet)
                self._spreadsheet.set_content(cell, content)

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

    def set_cell_content(self, coord, str_content) -> None:
        coords = Coordinates.from_id(coord)
        self._create_and_assign_content(coords, str_content)

    def get_cell_content_as_float(self, coord) -> float:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        value = cell.get_value_as_float()
        if value is None:
            raise NoNumberException(f"Cell {coord} does not contain a number")
        return value

    def get_cell_content_as_string(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_value_as_str()

    def get_cell_formula_expression(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_content().expression

    def save_spreadsheet_to_file(self, s_name_in_user_dir) -> None:
        self._file_manager.save(self._spreadsheet, s_name_in_user_dir)

    def load_spreadsheet_from_file(self, s_name_in_user_dir) -> None:
        spreadsheet, coords_with_formulas = self._file_manager.read(
            s_name_in_user_dir)
        self._formula_evaluator = FormulaEvaluator()
        self._deps_manager = DependencyManager()
        self._spreadsheet = spreadsheet
        self._recompute_cells(coords_with_formulas)
