from usecase.controller import Controller
from domain.contents import Number
from domain.formula_evaluation.tokenizer import Tokenizer


def main() -> None:
    print('Simple Spreadsheet')
    controller = Controller()
    controller.spreadsheet.edit_cell('A1', Number(10))
    print(controller.spreadsheet.get_cell('A1').get_value())

    tk = Tokenizer()
    print(tk.tokenize('SUMA(a1:B2) + .21 + -12.1000 - promedio(C3;D4)'))


if __name__ == '__main__':
    main()
