from usecase.controller import Controller
from domain.contents import Number
from domain.formula_evaluation import Tokenizer


def main() -> None:
    print('Simple Spreadsheet')
    controller = Controller()
    controller.spreadsheet.edit_cell('A1', Number(10))
    print(controller.spreadsheet.get_cell('A1').get_value())

    tk = Tokenizer()
    print(tk.tokenize('SUMA(A1:B2) + 1021 - PROMEDIO(C3;D4)'))


if __name__ == '__main__':
    main()
