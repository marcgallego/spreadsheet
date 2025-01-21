from abc import abstractmethod
import os

from textual.app import ComposeResult
from textual.widgets import Button, Static, Input, Label
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


class EnterPathDialog(ModalScreen[str]):
    """Abstract base class for file path dialog screens."""

    BINDINGS = [("escape", "cancel", "Cancel")]

    CSS = """
    #dialog {
        padding: 1 2;
        background: $surface;
        border: thick $primary;
        min-width: 40;
        min-height: 40;
    }

    #input-container {
        layout: vertical;
        padding: 1;
        margin: 1;
    }
    
    #status {
        height: 1;
        color: $error;
    }
    
    #path-input {
        margin: 1;
    }
    
    Button {
        margin: 1;
        width: 20;
    }

    #button-container {
        layout: horizontal;
        align-horizontal: center;
        margin-top: 1;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self._title_text = "Enter File Path:"
        self._action_button_text = "Confirm"
        self._placeholder_text = "Enter path..."
        self._status_text = ""

    def compose(self) -> ComposeResult:
        with Container(id="dialog"):
            with Container(id="input-container"):
                yield Label(self._title_text)
                yield Input(placeholder=self._placeholder_text, id="path-input")
                yield Label(self._status_text, id="status")
                yield Label("Current directory: " + os.getcwd())
                with Container(id="button-container"):
                    yield Button(self._action_button_text, variant="primary", id="save")
                    yield Button("Cancel", variant="error", id="cancel")

    def action_cancel(self) -> None:
        self.dismiss(None)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "cancel":
            self.dismiss(None)
        elif event.button.id == "save":
            path_input = self.query_one("#path-input", Input)
            status_label = self.query_one("#status", Label)
            path = path_input.value.strip()

            if self._validate_path(path, status_label):
                self.dismiss(path)

    @abstractmethod
    def _validate_path(self, path: str, status_label: Label) -> bool:
        """Validate the entered path according to dialog-specific rules."""
        pass


class SaveDialog(EnterPathDialog):
    """Dialog for saving files with .s2v extension."""

    def __init__(self) -> None:
        super().__init__()
        self._title_text = "Enter path to save spreadsheet:"
        self._action_button_text = "Save"
        self._placeholder_text = "path/to/spreadsheet.s2v"

    def _validate_path(self, path: str, status_label: Label) -> bool:
        if not path:
            status_label.update("Please input a path")
            return False

        # Check for valid filename
        filename = os.path.basename(path)
        name_without_ext = os.path.splitext(filename)[0]

        if not filename or filename == '.s2v':
            status_label.styles.color = "yellow"
            status_label.update("Please enter a valid filename")
            return False

        if not name_without_ext:
            status_label.styles.color = "yellow"
            status_label.update("Filename cannot be empty")
            return False

        if not path.endswith(".s2v"):
            status_label.styles.color = "yellow"
            status_label.update("File must have .s2v extension")
            return False

        if os.path.isdir(path):
            status_label.styles.color = "yellow"
            status_label.update("Path cannot be a directory")
            return False

        status_label.update("")  # Clear any error messages
        return True


class LoadDialog(EnterPathDialog):
    """Dialog for loading existing .s2v files."""

    def __init__(self) -> None:
        super().__init__()
        self._title_text = "Select spreadsheet to load:"
        self._action_button_text = "Load"
        self._placeholder_text = "path/to/existing_spreadsheet.s2v"
        self._status_text = "Note: Loading a new spreadsheet will overwrite the current one."

    def _validate_path(self, path: str, status_label: Label) -> bool:
        if not path:
            status_label.update("Please input a path")
            return False

        if not os.path.exists(path):
            status_label.styles.color = "red"
            status_label.update("The path you indicated does not exist.")
            return False

        if os.path.isdir(path):
            status_label.styles.color = "yellow"
            status_label.update(
                "The path you indicated is a directory, not a file.")
            return False

        if not path.endswith(".s2v"):
            status_label.styles.color = "yellow"
            status_label.update("The file you indicated is not a .s2v file")
            return False

        return True
