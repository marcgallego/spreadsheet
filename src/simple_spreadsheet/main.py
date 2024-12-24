from usecase.controller import Controller
from domain.contents import Number


def main() -> None:
    print('Simple Spreadsheet')
    controller = Controller()
    controller.spreadsheet.edit_cell('A1', Number(10))
    print(controller.spreadsheet.get_cell('A1').get_value())


if __name__ == '__main__':
    main()
