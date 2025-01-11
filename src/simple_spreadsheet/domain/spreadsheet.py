from functools import singledispatchmethod

from .cell import Cell
from .contents import Content, ContentType
from .coordinates import Coordinates, Column
from .cell_range import CellRange
from .consts import NUM_ROWS, NUM_COLS


class Spreadsheet:
    def __init__(self) -> None:
        self._cells = [[Cell() for _ in range(NUM_COLS)]
                       for _ in range(NUM_ROWS)]

        self._rows = [i + 1 for i in range(NUM_ROWS)]
        self._cols = self._generate_cols()

    def _generate_cols(self) -> list[str]:
        cols = []
        for i in range(NUM_COLS):
            col = Column.letters_from_number(i)
            cols.append(col)
        return cols

    def get_rows(self) -> list[int]:
        return self._rows

    def get_columns(self) -> list[str]:
        return self._cols

    @singledispatchmethod
    def get_cell(self, _) -> 'Cell':
        raise NotImplementedError("Unsupported type")

    @get_cell.register
    def _(self, coords: 'Coordinates') -> 'Cell':
        row, col = coords.get_indices()
        return self._cells[row][col]

    @get_cell.register
    def _(self, cell_id: str) -> 'Cell':
        coords = Coordinates.from_id(cell_id)
        return self.get_cell(coords)

    @get_cell.register
    def _(self, row: int, col: int) -> 'Cell':
        coords = Coordinates(row, col)
        return self.get_cell(coords)

    # TODO: rename
    def get_values(self, cell_range: CellRange) -> list[Content]:
        values = []
        coords_list = cell_range.get_coords()
        for coords in coords_list:
            cell = self.get_cell(coords)
            values.append(cell.get_value_as_float())
        return values

    # TODO: rename
    def get_all_values(self) -> list[list[Content]]:
        return [[cell.get_value_as_str() for cell in row] for row in self._cells]

    def set_content(self, coordinates, content: Content) -> None:
        if not isinstance(content, Content):
            raise TypeError(f"Invalid content type: {type(content)}")
        cell = self.get_cell(coordinates)
        cell.set_content(content)

    @property
    def cells(self) -> list[list[Cell]]:
        return self._cells
