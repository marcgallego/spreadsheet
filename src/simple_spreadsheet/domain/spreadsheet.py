from .cell import Cell
from .contents import Content
from .coordinates import Coordinates
from .cell_range import CellRange
from .consts import NUM_ROWS, NUM_COLS


class Spreadsheet:
    def __init__(self) -> None:
        self.cells = [[Cell() for _ in range(NUM_COLS)]
                      for _ in range(NUM_ROWS)]

    def get_cell_from_coords(self, coords: Coordinates) -> Cell:
        row, col = coords.get_indices()
        return self.cells[row][col]

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

    def edit_cell(self, cell_id: str, content: Content) -> None:
        cell = self.get_cell(cell_id)
        cell.set_value(content)
