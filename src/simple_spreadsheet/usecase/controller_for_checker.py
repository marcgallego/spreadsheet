
from simple_spreadsheet.domain.spreadsheet import Spreadsheet
from simple_spreadsheet.domain.coordinates import Coordinates
from simple_spreadsheet.domain.contents import ContentFactory, ContentType
from simple_spreadsheet.domain.formula_evaluation import FormulaEvaluator
from simple_spreadsheet.domain.update_manager import UpdateManager

from tests.automatic_grader.usecasesmarker import ISpreadsheetControllerForChecker

# TODO: revisar si es llançen les excepcions de tests


class ControllerForChecker(ISpreadsheetControllerForChecker):
    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()
        self._update_manager = UpdateManager()

    def _recompute_cells(self, cells: list[Coordinates]) -> None:
        for cell in cells:
            content = self._spreadsheet.get_cell(cell).get_content()
            if content.type == ContentType.FORMULA:
                self._formula_evaluator.evaluate(content, self._spreadsheet)
                self._spreadsheet.set_content(cell, content)

                dependants = self._update_manager.get_dependents(cell)
                self._recompute_cells(dependants)

    def _create_and_assign_content(self, coords: Coordinates, value: str) -> None:
        new_content = ContentFactory.create(value)
        dependencies = None
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
            dependencies = new_content.get_dependencies()
        self._update_manager.has_circular_dependency(coords, dependencies)
        self._spreadsheet.set_content(coords, new_content)
        self._update_manager.set_dependencies(coords, dependencies)
        self._recompute_cells(self._update_manager.get_dependents(coords))

    def set_cell_content(self, coord, str_content) -> None:
        coords = Coordinates.from_id(coord)
        self._create_and_assign_content(coords, str_content)

    def get_cell_content_as_float(self, coord) -> float:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_value_as_float()

    def get_cell_content_as_string(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_value_as_str()

    def get_cell_formula_expression(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_content()
