import re
from .consts import NUM_ROWS, NUM_COLS

ABC_LEN = 26


class Coordinates:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col
        self.is_in_range()
        self.id = self.parse_indices(row, col)

    @classmethod
    def from_id(cls, cell_id: str) -> 'Coordinates':
        cell_id = cell_id.upper()
        cls.is_valid_id(cell_id)
        row, col = cls.parse_id(cell_id)
        return cls(row, col)

    @staticmethod
    def parse_id(cell_id) -> tuple[int, int]:
        row_str = ''.join(filter(str.isalpha, cell_id))

        row = 0
        for i, char in enumerate(reversed(row_str)):
            row += (ord(char) - ord('A') + 1) * (ABC_LEN ** i)

        col_str = ''.join(filter(str.isdigit, cell_id))
        col = int(col_str) - 1

        return row, col

    @staticmethod
    def is_valid_id(cell_id) -> None:
        if not re.match(r'^[A-Z]+[0-9]+$', cell_id):
            raise ValueError('Invalid cell id')

    def __str__(self) -> str:
        return self.id + f'({self.row}, {self.col})'

    def parse_indices(self, row: int, col: int) -> str:
        row_str = ''
        while row:
            row -= 1
            row_str = chr(row % ABC_LEN + ord('A')) + row_str
            row //= ABC_LEN

        return row_str + str(col + 1)

    def is_in_range(self) -> None:
        if not (0 <= self.row < NUM_ROWS and 0 <= self.col < NUM_COLS):
            raise ValueError('Cell out of range')

    def get_id(self) -> str:
        return self.id

    def get_indices(self) -> tuple[int, int]:
        return self.row, self.col
