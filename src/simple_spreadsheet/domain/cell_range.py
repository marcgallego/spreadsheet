from .functions import Argument
from .coordinates import Coordinates


class CellRange(Argument):
    def __init__(self, start: Coordinates, end: Coordinates) -> None:
        min_row = min(start.row, end.row)
        max_row = max(start.row, end.row)

        min_col = min(start.col, end.col)
        max_col = max(start.col, end.col)

        self._top_left_corner = Coordinates(min_row, min_col)
        self._bottom_right_corner = Coordinates(max_row, max_col)

        self._coords_in_range: list[Coordinates] = self._list_coords_in_range()

    def __repr__(self) -> str:
        return f'{self._top_left_corner}:{self._bottom_right_corner}'

    def _list_coords_in_range(self) -> list[Coordinates]:
        coords = []
        for row in range(self._top_left_corner.row, self._bottom_right_corner.row + 1):
            for col in range(self._top_left_corner.col, self._bottom_right_corner.col + 1):
                coords.append(Coordinates(row, col))
        return coords

    def get_coords(self) -> list[Coordinates]:
        return self._coords_in_range

    def evaluate_arg(self, spreadsheet) -> list[float]:
        values = []
        coords_list = self.get_coords()
        for coords in coords_list:
            cell = spreadsheet.get_cell(coords)
            values.append(cell.get_value_as_float())
        return values

    def get_dependencies(self) -> set[Coordinates]:
        return set(self._coords_in_range)
