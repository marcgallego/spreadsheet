from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Input, Button, Static, Header
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.containers import Container
from textual import work

from simple_spreadsheet.domain.coordinates import Coordinates


class ConfirmDialog(ModalScreen):
    """Simple confirmation dialog."""

    DEFAULT_CSS = """
    ConfirmDialog {
        align: center middle;
    }

    #dialog-container {
        grid-size: 1;
        padding: 1 2;
        width: 60;
        height: auto;
        background: $surface;
        border: thick $primary 80%;
        border-radius: 1;
    }

    #question {
        height: 3;
        width: 100%;
        content-align: center middle;
        padding: 1;
    }

    #button-container {
        height: 3;
        align: center middle;
        layout: horizontal;
        padding: 0 1 1 1;
    }

    Button {
        margin: 0 1;
        min-width: 10;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Static(
                "Are you sure you want to create a new spreadsheet?\nAll unsaved data will be lost.",
                id="question"
            ),
            Container(
                Button("Yes", id="yes", variant="primary"),
                Button("No", id="no", variant="error"),
                id="button-container"
            ),
            id="dialog-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class Grid(DataTable):
    def __init__(self, controller) -> None:
        self.controller = controller
        self.spreadsheet = controller._spreadsheet
        super().__init__(zebra_stripes=True)
        self.selected_cell = None

    def refresh_grid(self) -> None:
        """Refresh the entire grid content."""
        self.clear()

        cols = self.spreadsheet.get_columns()
        self.add_columns("", *cols)
        self.fixed_columns = 1

        rows = self.spreadsheet.get_rows()
        vals = self.spreadsheet.get_all_values()

        for i, row_name in enumerate(rows):
            row_vals = vals[i]
            self.add_row(row_name, *row_vals, key=row_name)

    def compose(self) -> ComposeResult:
        self.refresh_grid()
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
    TITLE = "Simple spreadsheet"

    CSS = """
    Screen {
        background: $surface;
    }

    Header {
        background: $primary;
        color: $text;
        height: 1;
        content-align: center middle;
        text-align: center;
    }

    Grid {
        height: 1fr;
        min-height: 0;
    }

    Input {
        dock: bottom;
        height: 3;
        margin: 0 0 1 0;
        border: solid $primary;
        background: $surface;
    }

    Footer {
        dock: bottom;
        background: $primary;
        color: $text;
        padding: 0 1;
        height: 1;
    }

    DataTable > .datatable--header {
        background: $primary-darken-2;
        color: $text;
        text-style: bold;
    }

    DataTable > .datatable--hover {
        background: $accent-darken-2;
    }

    DataTable > .datatable--cursor {
        background: $accent;
        color: $text;
    }

    DataTable > .datatable--fixed {
        background: $primary-darken-1;
        color: $text;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "create", "New spreadsheet", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.grid = Grid(controller)
        self.text_input = Input(placeholder="Edit cell")

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.grid
        yield self.text_input
        yield Footer(show_command_palette=False)

    @work
    async def action_create(self) -> None:
        """Handle the create action with confirmation."""
        dialog = ConfirmDialog()
        if await self.push_screen_wait(dialog):
            self.controller.create_new_spreadsheet()
            self.grid.spreadsheet = self.controller._spreadsheet
            self.grid.refresh_grid()
            self.text_input.value = ""
            self.refresh()

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
