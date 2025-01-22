from simple_spreadsheet.domain.spreadsheet import Spreadsheet
from simple_spreadsheet.domain.contents import ContentFactory
from simple_spreadsheet.domain.coordinates import Coordinates


class FileManager:
    def read(self, file_path: str) -> Spreadsheet:
        """Reads the content of a file and returns a Spreadsheet object."""
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

    def _get_content_to_dump(self, cell) -> str:
        """Converts a cell's content into a string for file saving."""
        content = cell.get_content()
        if content is not None:
            if content.is_formula():
                return content.expression.replace(";", ",")
            else:
                return content.get_value_as_str()
        return ''

    def _write_file(self, file_path: str, output: list[list[str]]) -> None:
        """Writes the processed content to a file."""
        with open(file_path, "w") as file:
            for row in output:
                file.write(";".join(row) + "\n")

    def save(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        """Saves a Spreadsheet object to a file."""
        cells = spreadsheet.cells
        output = []
        last_non_empty_row = -1

        for row_index, row in enumerate(cells):
            row_output = []
            last_non_empty_col = -1

            for col_index, cell in enumerate(row):
                cell_output = self._get_content_to_dump(cell)
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
