import re
from .consts import NUM_ROWS, NUM_COLS

ABC_LEN = 26


class Column:
    @staticmethod
    def number_from_letters(letters: str) -> int:
        num = 0
        for i, char in enumerate(reversed(letters)):
            num += (ord(char) - ord('A') + 1) * (ABC_LEN ** i)
        return num - 1

    @staticmethod
    def letters_from_number(num: int) -> str:
        letters = ''
        num += 1
        while num:
            num -= 1
            letters = chr(num % ABC_LEN + ord('A')) + letters
            num //= ABC_LEN
        return letters


class Coordinates:
    def __init__(self, row: int, col: int) -> None:
        self._row = row
        self._col = col
        self._is_in_range()
        self._id = self._parse_indices(row, col)

    def __repr__(self) -> str:
        return self._id

    @classmethod
    def from_id(cls, cell_id: str) -> 'Coordinates':
        if not isinstance(cell_id, str):
            raise TypeError(f"Expected cell_id to be a string, got {
                            type(cell_id).__name__}")
        cell_id = cell_id.upper()
        cls.is_valid_id(cell_id)
        row, col = cls.parse_id(cell_id)
        return cls(row, col)

    @staticmethod
    def is_valid_id(cell_id: str) -> None:
        if not re.match(r'^[A-Z]+[0-9]+$', cell_id):
            raise ValueError(f'Invalid cell ID ({cell_id})')

    @staticmethod
    def parse_id(cell_id: str) -> tuple[int, int]:
        col_str = ''.join(filter(str.isalpha, cell_id))
        row_str = ''.join(filter(str.isdigit, cell_id))

        row = int(row_str) - 1
        col = Column.number_from_letters(col_str)

        return row, col

    def _is_in_range(self) -> None:
        if not (0 <= self._row < NUM_ROWS and 0 <= self._col < NUM_COLS):
            raise ValueError('Cell out of range')

    def _parse_indices(self, row: int, col: int) -> str:
        return Column.letters_from_number(col) + str(row + 1)

    def get_id(self) -> str:
        return self.id

    def get_indices(self) -> tuple[int, int]:
        return self._row, self._col

    @property
    def row(self) -> int:
        """Returns the row index (zero-based)."""
        return self._row

    @property
    def col(self) -> int:
        """Returns the column index (zero-based)."""
        return self._col
