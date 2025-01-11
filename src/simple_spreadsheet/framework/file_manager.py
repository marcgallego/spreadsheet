from simple_spreadsheet.domain.spreadsheet import Spreadsheet
from simple_spreadsheet.domain.contents import ContentType


class FileManager:
    def read_file(self, file_path: str) -> Spreadsheet:
        with open(self.file_path, "r") as file:
            return file.read()

    def _get_content_to_dump(self, cell) -> str:
        if cell.get_content() is not None:

            content = cell.get_content()
            if content.type == ContentType.FORMULA:
                return content.expression.replace(';', ',')
            else:
                return content.get_value_as_str()
        else:
            return ""

    def _write_file(self, file_path: str, output: list[str]) -> None:
        with open(file_path, "w") as file:
            for row in output:
                file.write(";".join(row) + "\n")

    def save(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        cells = spreadsheet.cells
        output = []
        position_of_last_row = 0
        for row in cells:
            row_output = []
            position_of_last_col = -1
            for i, cell in enumerate(row):
                cell_output = self._get_content_to_dump(cell)
                row_output.append(cell_output)
                if cell_output != "":
                    position_of_last_col = i

            row_output = row_output[:position_of_last_col + 1]
            if position_of_last_col > 0:
                position_of_last_row += 1
            output.append(row_output)

        output = output[:position_of_last_row + 1]
        self._write_file(file_path, output)
