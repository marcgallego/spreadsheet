from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer
from textual.binding import Binding


class Grid(DataTable):
    def __init__(self, spreadsheet) -> None:
        self.spreadsheet = spreadsheet
        super().__init__(zebra_stripes=True)

    def compose(self) -> ComposeResult:
        cols = self.spreadsheet.get_columns()
        self.add_columns("", *cols)
        self.fixed_columns = 1

        rows = self.spreadsheet.get_rows()
        vals = self.spreadsheet.get_all_values()

        for i, row_name in enumerate(rows):
            row_vals = vals[i]
            self.add_row(row_name, *row_vals, key=row_name)

        yield from super().compose()

    def on_data_table_cell_selected(self, message) -> None:
        ui_coords = message.coordinate
        row, col = ui_coords.row, ui_coords.column - 1
        cell = self.spreadsheet.get_cell(row, col)

        raise NotImplementedError(cell.get_content())


class UserInterface(App):
    """App to display an Excel-like grid in Textual."""

    BINDINGS = [
        Binding("e", "edit_cell", "Edit cell", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self, spreadsheet) -> None:
        super().__init__()  # Initialize the base class
        self.grid = Grid(spreadsheet)

    def compose(self) -> ComposeResult:
        # Compose the grid and the footer
        yield self.grid
        yield Footer()
