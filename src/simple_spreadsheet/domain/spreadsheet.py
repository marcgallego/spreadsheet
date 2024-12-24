import numpy as np

from .cell import Cell
from .contents import Content
from .coordinates import Coordinates
from .consts import NUM_ROWS, NUM_COLS


class Spreadsheet:
    def __init__(self) -> None:
        self.cells = np.empty((NUM_ROWS, NUM_COLS), dtype=Cell)

    def get_cell(self, cell_id: str) -> Cell:
        coord = Coordinates.from_id(cell_id)
        cell = self.cells[coord.get_indices()]
        if cell is None:
            cell = Cell(coord)
            self.cells[coord.get_indices()] = cell
        return self.cells[coord.get_indices()]

    def edit_cell(self, cell_id: str, content: Content) -> None:
        cell = self.get_cell(cell_id)
        cell.set_value(content)
