from domain.spreadsheet import Spreadsheet
from domain.contents import ContentFactory
from framework.ui import UserInterface


class Controller:
    def __init__(self) -> None:
        self._spreadsheet = Spreadsheet()

        self._spreadsheet.edit_cell('A1', ContentFactory.create('hola'))
        self._spreadsheet.edit_cell('B5', ContentFactory.create('5'))
        self._spreadsheet.edit_cell('C3', ContentFactory.create('=B5+5'))
        self._ui = UserInterface(self._spreadsheet)
        self._ui.run()
