from simple_spreadsheet.usecase.controller import Controller
from simple_spreadsheet.framework.ui import UserInterface


def main() -> None:
    controller = Controller()
    app = UserInterface(controller)
    app.run()


if __name__ == '__main__':
    main()
