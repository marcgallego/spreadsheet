from .cell import Cell
from .contents import Content
from .coordinates import Coordinates
from .cell_range import CellRange
from .consts import NUM_ROWS, NUM_COLS, ABC_LEN


class Spreadsheet:
    def __init__(self) -> None:
        self._cells = [[Cell() for _ in range(NUM_COLS)]
                       for _ in range(NUM_ROWS)]

        self._rows = [i + 1 for i in range(NUM_ROWS)]
        self._cols = self._generate_cols()

    def _generate_cols(self) -> list[str]:
        cols = []
        for i in range(NUM_COLS):
            col = ""
            while i >= 0:
                col = chr(i % ABC_LEN + ord('A')) + col
                i = (i // ABC_LEN) - 1
            cols.append(col)
        return cols

    def get_rows(self) -> list[int]:
        return self._rows

    def get_columns(self) -> list[str]:
        return self._cols

    def get_cell_from_coords(self, coords: Coordinates) -> Cell:
        row, col = coords.get_indices()
        return self._cells[row][col]

    def get_cell(self, cell_id: str) -> Cell:
        coord = Coordinates.from_id(cell_id)
        return self.get_cell_from_coords(coord)

    def get_values(self, cell_range: CellRange) -> list[Content]:
        values = []
        coords_list = cell_range.get_coords()
        for coords in coords_list:
            cell = self.get_cell_from_coords(coords)
            values.append(cell.get_value())
        return values

    def get_all_values(self) -> list[list[Content]]:
        return [[cell.get_value() for cell in row] for row in self._cells]

    def edit_cell(self, cell_id: str, content: Content) -> None:
        if not isinstance(content, Content):
            raise TypeError(f"Invalid content type: {type(content)}")
        cell = self.get_cell(cell_id)
        cell.set_value(content)
