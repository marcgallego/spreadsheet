from textual.app import App, ComposeResult
from textual.widgets import DataTable


class UserInterface(App):
    """App to display an Excel-like grid in Textual."""

    def __init__(self, spreadsheet) -> None:
        self.spreadsheet = spreadsheet
        super().__init__()

    def compose(self) -> ComposeResult:
        table = DataTable(zebra_stripes=True)

        cols = self.spreadsheet.get_columns()
        table.add_columns("", *cols)

        rows = self.spreadsheet.get_rows()
        vals = self.spreadsheet.get_all_values()

        n = len(rows)
        for i in range(n):
            row_name = rows[i]
            row_vals = vals[i]
            table.add_row(row_name, *row_vals)

        yield table
