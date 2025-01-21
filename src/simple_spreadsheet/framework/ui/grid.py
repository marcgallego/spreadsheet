from textual.app import ComposeResult
from textual.widgets import DataTable


from simple_spreadsheet.domain.coordinates import Coordinates


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
