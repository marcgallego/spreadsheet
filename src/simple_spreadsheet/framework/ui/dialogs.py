from textual.app import ComposeResult
from textual.widgets import Button, Static
from textual.screen import ModalScreen
from textual.containers import Container


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
