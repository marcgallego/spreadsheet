import numpy as np

from .cell import Cell
from .contents import Content

NUM_ROWS = 1_000
NUM_COLS = 1_000


class Spreadsheet:
    def __init__(self) -> None:
        self.cells = np.empty((NUM_ROWS, NUM_COLS), dtype=Cell)
        print(self.cells)

    def edit_cell(self, cell_id: str, content: Content) -> None:
        self.cells[cell_id] = content
