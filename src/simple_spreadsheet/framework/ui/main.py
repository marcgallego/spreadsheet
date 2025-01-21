from textual.app import App, ComposeResult
from textual.widgets import Footer, Input, Header
from textual.binding import Binding
from textual import work

from simple_spreadsheet.domain.coordinates import Coordinates
from .grid import Grid
from .dialogs import ConfirmDialog, SaveDialog, LoadDialog


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

    #cell-editor {
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
        Binding("ctrl+n", "create", "New spreadsheet", show=True),
        Binding("ctrl+s", "save", "Save as...", show=True),
        Binding("ctrl+o", "open", "Open...", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
        Binding("escape", "unfocus_input",
                "Exit cell editing mode", show=False)]

    def __init__(self, controller) -> None:
        super().__init__()
        self.controller = controller
        self.grid = Grid(controller)
        self.text_input = Input(placeholder="Edit cell", id="cell-editor")

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

    @work
    async def action_save(self) -> None:
        """Handle the save action."""
        save_dialog = SaveDialog()
        result = await self.push_screen_wait(save_dialog)
        if result is not None:
            self.controller.save_spreadsheet(result)
            file_name = result.split("/")[-1]
            self.notify(f"Spreadsheet saved as {file_name}",
                        title="Success!")

    @work
    async def action_open(self) -> None:
        """Handle the open action."""
        load_dialog = LoadDialog()
        file_path = await self.push_screen_wait(load_dialog)
        if file_path:
            self.controller.load_spreadsheet(file_path)
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
