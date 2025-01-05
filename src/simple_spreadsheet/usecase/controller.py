from domain.spreadsheet import Spreadsheet
from domain.contents import Number
from framework.ui import UserInterface


class Controller:
    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()
        self._spreadsheet.edit_cell('A1', Number(5))
        self._ui = UserInterface(self._spreadsheet)
        self._ui.run()
