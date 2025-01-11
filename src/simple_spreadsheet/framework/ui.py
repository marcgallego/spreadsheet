from textual.app import App, ComposeResult
from textual.widgets import DataTable, Footer, Input, Button, Static, Header
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.containers import Container
from textual import work

from simple_spreadsheet.domain.coordinates import Coordinates


class ConfirmDialog(ModalScreen[bool]):
    """A custom confirmation dialog."""
    DEFAULT_CSS = """
    #dialog {
        padding: 1 2;
        background: $surface;
        border: thick $primary;
        min-width: 40;
        height: auto;
    }

    #question {
        padding: 1 0;
    }

    #buttons {
        layout: horizontal;
        align-horizontal: center;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Container(
            Static(
                "Are you sure you want to create a new spreadsheet?\nAll unsaved data will be lost.", id="question"),
            Container(
                Button("Yes", variant="primary", id="yes"),
                Button("No", variant="error", id="no"),
                id="buttons",
            ),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)


class Grid(DataTable):
    def __init__(self, controller) -> None:
        self.controller = controller
        super().__init__(zebra_stripes=True)
        self.selected_cell = None

    def refresh_grid(self) -> None:
        """Refresh the entire grid content."""
        self.clear()

        cols = self.controller.spreadsheet.get_columns()
        self.add_columns("", *cols)
        self.fixed_columns = 1

        rows = self.controller.spreadsheet.get_rows()
        vals = self.controller.spreadsheet.get_all_values()

        for i, row_name in enumerate(rows):
            row_vals = vals[i]
            self.add_row(row_name, *row_vals, key=row_name)

    def compose(self) -> ComposeResult:
        self.refresh_grid()
        yield from super().compose()

    def _prepare_to_edit(self, message: object) -> None:
        ui_coords = message.coordinate
        if ui_coords.column == 0:  # Ignore row names
            self.selected_cell = None
            self.app.text_input.value = ""
            return
        self.selected_cell = Coordinates(ui_coords.row, ui_coords.column - 1)
        cell = self.controller.spreadsheet.get_cell(self.selected_cell)

        content = cell.get_content()
        self.app.text_input.value = str(content) if content is not None else ""

    def on_data_table_cell_highlighted(self, message) -> None:
        self._prepare_to_edit(message)

    def on_data_table_cell_selected(self, message) -> None:
        self._prepare_to_edit(message)
        if self.selected_cell is not None:
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
        text-style: bold;
    }
    """

    BINDINGS = [
        Binding("ctrl+c", "create", "New spreadsheet", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("escape", "unfocus_input",
                "Exit cell editing mode", show=False),]

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
            self.grid.refresh_grid()
            self.text_input.value = ""
            self.refresh()

    def action_unfocus_input(self) -> None:
        """Handle unfocusing the input widget when 'esc' is pressed."""
        self.grid.selected_cell = None
        self.text_input.blur()
        self.grid.focus()

    def _handle_input(self, message: Input.Submitted) -> None:
        if self.grid.selected_cell is not None:
            # Ensure we're working with string values
            new_value = message.value

            # Update the spreadsheet
            self.controller.edit_cell(
                self.grid.selected_cell.row,
                self.grid.selected_cell.col,
                new_value
            )

            display_value = self.controller.spreadsheet.get_cell(
                self.grid.selected_cell).get_value_as_str()

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

    def on_input_submitted(self, message: Input.Submitted) -> None:
        """Handle when the input field is submitted."""
        try:
            self._handle_input(message)
        except Exception as e:
            self.app.notify(
                str(e),
                title="Ooops...",
                severity="error",
                timeout=None)

    def update_cell_view(self, coords: Coordinates, value: str) -> None:
        """Edit a cell in the spreadsheet."""
        position = (coords.row, coords.col+1)
        self.grid.update_cell_at(position, value, update_width=True)
