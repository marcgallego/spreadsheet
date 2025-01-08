from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Input
from textual.binding import Binding

from simple_spreadsheet.domain.coordinates import Coordinates


class Grid(DataTable):
    def __init__(self, controller) -> None:
        self.controller = controller
        self.spreadsheet = controller._spreadsheet
        super().__init__(zebra_stripes=True)
        self.selected_cell = None

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

    def on_data_table_cell_highlighted(self, message) -> None:
        ui_coords = message.coordinate
        if ui_coords.column == 0:  # Ignore row names
            return
        self.selected_cell = Coordinates(ui_coords.row, ui_coords.column - 1)
        cell = self.spreadsheet.get_cell(self.selected_cell)

        content = cell.get_content()
        self.app.text_input.value = str(content) if content is not None else ""

    def on_data_table_cell_selected(self, _) -> None:
        self.app.text_input.focus()


class UserInterface(App):
    """App to display an Excel-like grid in Textual."""

    CSS = """
    Grid {
        height: 1fr;
        min-height: 0;
    }

    Input {
        dock: bottom;
        height: auto;
        margin: 0 0 1 0;
        border: solid green;
    }

    Footer {
        dock: bottom;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.grid = Grid(controller)
        self.text_input = Input(placeholder="Edit cell")

    def compose(self) -> ComposeResult:
        yield self.grid
        yield self.text_input
        yield Footer(show_command_palette=False)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle when the input field is submitted."""
        if self.grid.selected_cell is not None:
            # Ensure we're working with string values
            new_value = message.value

            # Update the spreadsheet
            self.controller.edit_cell(
                self.grid.selected_cell.row,
                self.grid.selected_cell.col,
                new_value
            )

            display_value = self.controller._spreadsheet.get_cell(
                self.grid.selected_cell).get_raw_value()

            # Update the grid display
            self.grid.update_cell_at(
                (self.grid.selected_cell.row,
                 self.grid.selected_cell.col + 1),
                display_value,
                update_width=True
            )

            # unselect the cell
            self.grid.selected_cell = None
            self.grid.focus()

            # TODO: deal with empty "" and how values are converted to Content
        else:
            self.text_input.value = ""
            self.grid.focus()
