from ..domain.spreadsheet import Spreadsheet
from ..domain.contents import ContentFactory
from ..domain.coordinates import Coordinates


class SavingSpreadsheetException(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)

    def __init__(self, msg) -> None:
        Exception.__init__(self, msg)


class ReadingSpreadsheetException(Exception):
    def __init__(self) -> None:
        Exception.__init__(self)

    def __init__(self, msg) -> None:
        Exception.__init__(self, msg)


class FileManager:
    def read(self, file_path: str) -> Spreadsheet:
        """Reads the content of a file and returns a Spreadsheet object."""
        try:
            spreadsheet = Spreadsheet()
            coords_with_formulas: list[Coordinates] = []
            with open(file_path, "r") as file:
                for row_index, line in enumerate(file):
                    row = line.strip().split(";")
                    for col_index, cell_data in enumerate(row):
                        if cell_data != "":
                            coords = Coordinates(row_index, col_index)
                            if cell_data[0] == '=':
                                cell_data = cell_data.replace(",", ";")
                                coords_with_formulas.append(coords)
                            content = ContentFactory.create(cell_data)
                            spreadsheet.set_content(coords, content)
            return spreadsheet, coords_with_formulas
        except Exception as e:
            raise ReadingSpreadsheetException(str(e))

    def _write_file(self, file_path: str, output: list[list[str]]) -> None:
        """Writes the processed content to a file."""
        with open(file_path, "w") as file:
            for row in output:
                file.write(";".join(row) + "\n")

    def save(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        """Saves a Spreadsheet object to a file."""
        try:
            cells = spreadsheet.cells
            output = []
            last_non_empty_row = -1

            for row_index, row in enumerate(cells):
                row_output = []
                last_non_empty_col = -1

                for col_index, cell in enumerate(row):
                    cell_output = cell.get_value_to_dump()
                    row_output.append(cell_output)
                    if cell_output != "":
                        last_non_empty_col = col_index

                # Trim to the last non-empty column
                if last_non_empty_col >= 0:
                    row_output = row_output[:last_non_empty_col + 1]
                    last_non_empty_row = row_index
                else:
                    row_output = []  # Skip empty rows

                output.append(row_output)

            # Trim to the last non-empty row
            output = output[:last_non_empty_row + 1]
            self._write_file(file_path, output)
        except Exception as e:
            raise SavingSpreadsheetException(str(e))
