
from simple_spreadsheet.domain.spreadsheet import Spreadsheet
from simple_spreadsheet.domain.coordinates import Coordinates
from simple_spreadsheet.domain.contents import ContentFactory, ContentType
from simple_spreadsheet.domain.formula_evaluation import FormulaEvaluator
from simple_spreadsheet.framework.ui import UserInterface

from tests.automatic_grader.usecasesmarker import ISpreadsheetControllerForChecker

# TODO: update formulas automatically when a cell is edited
# TODO: detect circular references


class ControllerForChecker(ISpreadsheetControllerForChecker):
    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._formula_evaluator = FormulaEvaluator()

    def _create_and_assign_content(self, coords: Coordinates, value: str) -> None:
        new_content = ContentFactory.create(value)
        if new_content.type == ContentType.FORMULA:
            self._formula_evaluator.evaluate(new_content, self._spreadsheet)
        self._spreadsheet.set_content(coords, new_content)

    def set_cell_content(self, coord, str_content) -> None:
        coords = Coordinates.from_id(coord)
        self._create_and_assign_content(coords, str_content)

    def get_cell_content_as_float(self, coord) -> float:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_value()

    def get_cell_content_as_str(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_raw_value()

    def get_cell_formula_expression(self, coord) -> str:
        coords = Coordinates.from_id(coord)
        cell = self._spreadsheet.get_cell(coords)
        return cell.get_content()
